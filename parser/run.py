#!/bin/python3

from time     import sleep
from json     import dumps as to_json
from requests import post as post_request
from requests.exceptions import RequestException
from config   import (DEBUG, WAIT_FOR, API_ENDPOINT, AUTH_TOKEN,
                      MAX_WAITING_PERIOD, USERNAME, PASSWORD)
from lib.log   import debug, log
from lib.email import fetch_new_emails, mark_as_unread, NoMessages
from lib.parse import parse_messages

wait_for = WAIT_FOR

def work():
    global wait_for

    try:
        ids, messages = fetch_new_emails()
    except OSError:
        log("Failed to connect with e-mail server to parse messages.")
        return
    except NoMessages:
        debug("No e-mails to parse. Update wait_for time")
        response = post_request(API_ENDPOINT,
                                data="")
        try:
            received_wait_for = float(response.text)

            if received_wait_for == -1:
                log("Invalid token.")
                if not DEBUG:
                    mark_as_unread(ids)
                return
            elif received_wait_for == -2:
                log("Database error.")
                if not DEBUG:
                    mark_as_unread(ids)
                return

            debug("Received {} (minutes) from the server, "
                  "to wait until next execution.".format(
                  received_wait_for))

            if 0 < received_wait_for <= MAX_WAITING_PERIOD:
                wait_for = received_wait_for
            else:
                debug("Ignoring {} as it's not between 1 and {}".format(
                      received_wait_for,
                      MAX_WAITING_PERIOD))
        except RequestException:
            log("Failed to connect to Server")
            if not DEBUG:
                mark_as_unread(ids)
        except ValueError:
            log("Received {} from the Server, failed to convert to int "
                "to wait for (in minutes)".format(response.text))
        return
    except:
        log("Unexpected Error.")
        return

    data = parse_messages(messages)

    request_data = to_json({"token": AUTH_TOKEN,
                            "data": data})
    debug("JSON: {}".format(request_data))

    try:
        debug("Connecting to Server to register parsed events.")
        response = post_request(API_ENDPOINT,
                                headers={'Content-Type': 'application/json'},
                                data=request_data)
        debug("Events registered.")

        # Server returns wait_for until next run (in minutes)
        received_wait_for = float(response.text)

        if received_wait_for == -1:
            log("Invalid token.")
            if not DEBUG:
                mark_as_unread(ids)
            return
        elif received_wait_for == -2:
            log("Database error.")
            if not DEBUG:
                mark_as_unread(ids)
            return

        debug("Received {} (minutes) from the server, "
              "to wait until next execution.".format(
              received_wait_for))

        if 0 < received_wait_for <= MAX_WAITING_PERIOD:
            wait_for = received_wait_for
        else:
            debug("Ignoring {} as it's not between 1 and {}".format(
                  received_wait_for,
                  MAX_WAITING_PERIOD))
    except RequestException:
        log("Failed to connect to Server")
        if not DEBUG:
            mark_as_unread(ids)
    except ValueError:
        log("Received {} from the Server, failed to convert to int "
            "to wait for (in minutes)".format(response.text))

if __name__ == '__main__':
    if "" in [USERNAME, PASSWORD]:
        log("Please provide the correct username and password to access the e-mail.")
        exit()
    elif AUTH_TOKEN == "":
        print("Please change the AUTH_TOKEN at `config.py` (remember to update at the server too)")
        exit()

    try:
        while True:
            work()
            debug("Waiting for {} minutes before running again".format(
                  wait_for))
            sleep(60 * wait_for)
    except KeyboardInterrupt:
        print("\n")
        exit()
