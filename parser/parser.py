#!/bin/python3

from re import search
from sys import stderr
from json import dumps as to_json
from threading import Timer
from requests import post as post_request
from requests.exceptions import RequestException
from datetime import datetime, timedelta
from imaplib import IMAP4_SSL
from config import (DEBUG, HOST, USERNAME, PASSWORD, WAIT_FOR,
                    API_ENDPOINT, MAIL_FROM, AUTH_TOKEN,
                    MAX_WAITING_PERIOD, LOG_FILE, LOG_TIMESTAMP_FORMAT)

TIME_REGEXP = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}"
EVENT_REGEXP = r"\[[\w_^]+(-[\w_^]+)?\]"

wait_for = WAIT_FOR

def debug(*msgs, **kwargs):
    if DEBUG:
        print(*msgs, **kwargs)

def log(*msgs, **kwargs):
    timestamp = datetime.now().strftime(LOG_TIMESTAMP_FORMAT)
    message = "[{}] {}".format(timestamp, " ".join(msgs))

    if DEBUG or LOG_FILE == "":
        kwargs["file"] = stderr
        print(message, **kwargs)
    else:
        with open(LOG_FILE, 'w') as f:
            kwargs["file"] = f
            print(message, **kwargs)

def parse_messages(messages):
    data = []
    for message in messages:
        # Ignore message if needed information is missing
        try:
            time = search(TIME_REGEXP, message).group()
            event = search(EVENT_REGEXP, message).group()
        except AttributeError:
            continue

        # Unix epoch
        dt = datetime.strptime(time, "%d/%m/%Y %H:%M")
        epoch_start = datetime(1970, 1, 1)
        epoch = int((dt - epoch_start) / timedelta(seconds=1))

        # Remove [] to properly register the event
        args = event[1:-1].split("-")

        # Allow static events (no user_id) e.g. opening the door
        _dict = {"epoch": epoch,
                 "event": args[0]}
        if len(args) > 1:
            _dict["user_id"] = args[1]

        data += [_dict]

    return data

def fetch_new_emails(host, username, password):
    ids = []
    messages = []
    with IMAP4_SSL(host) as email:
        email.login(username, password)

        # Only mark as read in production to make debugging easier
        email.select(readonly=DEBUG)

        # Get unread e-mail ids sent from MyDenox to parse e-mails
        # (and mark as unread if it fails to save on the Server)
        _type, data = email.search(None,
                                   'ALL',
                                   '(UNSEEN)',
                                   '(FROM "{}")'.format(MAIL_FROM))
        ids = data[0].split()

        debug("{} e-mails to fetch.".format(len(ids)))
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
        log("Failed to mark {} e-mails as unread".format(len(ids)),
            "after reading them with IMAP and failing to save",
            "the parsed events in the DB.")

def work():
    global wait_for

    try:
        debug("Fetching new e-mails.")
        ids, messages = fetch_new_emails(HOST, USERNAME, PASSWORD)
        debug("Fetched e-mails.")
    except OSError:
        log("Failed to connect with e-mail server to parse MyDenox messages.")

        debug("Waiting for {} minutes before running again.".format(wait_for))
        Timer(60.0 * wait_for, work).start()
        return

    debug("Parsing messages.")
    data = parse_messages(messages)
    debug("Messages parsed.")

    request_data = to_json({"token": AUTH_TOKEN,
                            "data": data})
    debug("JSON: {}".format(request_data))

    try:
        debug("Connecting to Server to register parsed events.")
        response = post_request(API_ENDPOINT,
                                data=request_data)
        debug("Events registered.")

        received_wait_for = int(response.text)
        debug("Received {} (minutes) from the server,".format(received_wait_for),
              "to wait until next execution of this function.")
        if received_wait_for <= MAX_WAITING_PERIOD:
            wait_for = received_wait_for
        else:
            debug("Ignoring {} as it's bigger than waiting period limit ({}).".format(
                  received_wait_for,
                  MAX_WAITING_PERIOD))
    except RequestException:
        log("Failed to connect to Server,",
            "marking e-mails as unread." if not DEBUG else "\b\b.")

        if not DEBUG:
            mark_as_unread(HOST, USERNAME, PASSWORD, ids)
    except ValueError:
        log("Received {} from the Server,".format(response.text),
            "failed to convert to int to wait for (in minutes)")

    debug("Waiting for {} minutes before running again.".format(wait_for))
    Timer(60.0 * wait_for, work).start()

if __name__ == '__main__':
    work()
