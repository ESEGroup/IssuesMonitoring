#!/bin/python3

from . import Config
from time     import sleep
from .lib.log   import debug, log
from .lib.email import fetch_new_emails, mark_as_unread, NoMessages
from .lib.parse import parse_messages

try:
    from ..issues_monitoring.controllers import (registrar_presenca,
                                                 registrar_log_parser)
except:
    from issues_monitoring.controllers import (registrar_presenca,
                                                 registrar_log_parser)

def work():
    DEBUG = Config.debug
    WAIT_FOR = Config.parser_default_delay
    MAX_WAITING_PERIOD = Config.parser_max_delay
    USERNAME = Config.email
    PASSWORD = Config.email_password
    wait_for = WAIT_FOR

    if "" in [USERNAME, PASSWORD]:
        log("Please provide the correct username and password to access the e-mail.")
        exit()

    while True:
        registrar_log_parser()
        try:
            ids, messages = fetch_new_emails()
        except OSError:
            log("Failed to connect with e-mail server to parse messages.")
            ids, messages = [], []
        except NoMessages:
            debug("No e-mails to parse. Update wait_for time")
            ids, messages = [], []
        except:
            log("Unexpected Error.")
            mark_as_unread(ids)
            ids, messages = [], []

        received_wait_for = -1
        try:
            data = parse_messages(messages)
            received_wait_for = registrar_presenca(data)
            debug("{} events registered.".format(len(data)))
        except:
            log("Unexpected Error.")
            mark_as_unread(ids)

        debug("Received {} (minutes) from the DB, "
              "to wait until next execution.".format(
              received_wait_for))

        if 0 < received_wait_for <= MAX_WAITING_PERIOD:
            wait_for = received_wait_for
        else:
            debug("Ignoring {} as it's not between 1 and {}".format(
                  received_wait_for,
                  MAX_WAITING_PERIOD))

        debug("Waiting for {} minutes before running again".format(
              wait_for))
        sleep(60 * wait_for)
