#!/bin/python3

from re import search
from json import dumps as to_json
from threading import Timer
from requests import post as post_request
from requests.exceptions import RequestException
from datetime import datetime, timedelta
from imaplib import IMAP4_SSL
from config import (DEBUG, HOST, USERNAME, PASSWORD, WAIT_FOR,
                    API_ENDPOINT, MAIL_FROM, AUTH_TOKEN)

TIME_REGEXP = r"\d\d\/\d\d/\d\d\d\d\ \d\d:\d\d"
EVENT_REGEXP = r"\[[a-zA-Z0-9]+(-?[a-zA-Z0-9]+)?\]"

wait_for = WAIT_FOR # minutes

def parse_emails(messages):
    data = []
    for message in messages:
        # Ignore message if needed information is missing
        try:
            time = search(TIME_REGEXP, message).group()
            event = search(EVENT_REGEXP, message).group()
        except AttributeError:
            continue

        dt = datetime.strptime(time, "%d/%m/%Y %H:%M")
        epoch = int((dt - datetime(1970,1,1)) / timedelta(seconds=1))

        # Remove [] to properly register the event
        args = event[1:-1].split("-")

        _dict = {"epoch": epoch,
                 "event": args[0]}

        # Allow static events (no user_id) e.g. opening the door
        if len(args) > 1:
            _dict["user_id"] = args[1]

        data += [_dict]

    return data

def fetch_new_emails(host, username, password):
    messages = []
    with IMAP4_SSL(host) as email:
        email.login(username, password)

        # Only mark as read in production to make debugging easier
        email.select(readonly=DEBUG)

        # Get unread email ids sent from MyDenox to parse it
        # (and mark as unread if request to Server fails)
        _type, data = email.search(None,
                                   'ALL',
                                   '(UNSEEN)',
                                   '(FROM "{}")'.format(MAIL_FROM))
        ids = data[0].split()

        for num in ids:
            _type, data = email.fetch(num, '(RFC822)')
            messages += [data[0][1].decode('utf-8')]

    return ids, messages

def mark_as_unread(host, username, password, ids):
    try:
        with IMAP4_SSL(host) as email:
            email.login(username, password)
            email.select()
            for e_id in ids:
                email.store(e_id, '-FLAGS', '\Seen')
    except OSError:
        print("Failed to mark {} messages as unread".format(len(ids)),
              "after reading them with IMAP",
              "and failing to save in the DB")

def work():
    global wait_for
    try:
        ids, emails = fetch_new_emails(HOST, USERNAME, PASSWORD)
    except OSError:
        print("Failed to connect with email server to parse them")
        Timer(60.0 * wait_for, work).start()
        return

    data = parse_emails(emails)
    request_data = to_json({"token": AUTH_TOKEN,
                            "data": data})
    if DEBUG:
        print("JSON: {}".format(request_data))

    try:
        response = post_request(API_ENDPOINT,
                                data=request_data)
        wait_for = int(response.text)
    except RequestException:
        if not DEBUG:
            print("Failed to connect to server,",
                  "marking e-mails as unread")
            mark_as_unread(HOST, USERNAME, PASSWORD, ids)
    except ValueError:
        print("Received {} from the Server,".format(response.text),
              "failed to convert to int to wait for (in minutes)")

    Timer(60.0 * wait_for, work).start()

if __name__ == '__main__':
    work()
