from .. import Config
from .log import debug
from re import search
from datetime import datetime

try:
    from server.issues_monitoring import controllers
except:
    from issues_monitoring import controllers

MAIL_FROM = Config.mydenox_email

TIME_REGEXP = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}"
EVENT_REGEXP = r"\[[^\W_]+(-[^\W_]+)?(-[^\W_]+)?\]"

def parse_messages(messages):
    debug("Parsing messages.")
    data = []
    
    for message in messages:
        # Test for MyDenox failure messages
        try:
            search(r"bateria interna", message).group()
            time = search(TIME_REGEXP, message).group()

            # Unix epoch
            dt = datetime.strptime(time, "%d/%m/%Y %H:%M")
            epoch = dt.timestamp()

            controllers.log_mydenox(
                    epoch,
                    "Aviso de falta de energia (utilizando bateria interna)",
                    "bateria")
            continue
        except AttributeError:
            pass

        try:
            search(r"Central Offline", message).group()
            time = search(TIME_REGEXP, message).group()

            # Unix epoch
            dt = datetime.strptime(time, "%d/%m/%Y %H:%M")
            epoch = dt.timestamp()
            controllers.log_mydenox(
                    epoch,
                    "Aviso de falta de conexão com a Internet",
                    "internet")
            continue
        except AttributeError:
            pass

        # Custom MyDenox events
        # Ignore message if needed information is missing
        try:
            search(r"From: {}".format(MAIL_FROM), message).group()
            time = search(TIME_REGEXP, message).group()
            event = search(EVENT_REGEXP, message).group()
        except AttributeError:
            continue

        # Unix epoch
        dt = datetime.strptime(time, "%d/%m/%Y %H:%M")
        epoch = dt.timestamp()

        # Remove [] from [EVENT-user_id-lab_id] and split them to register
        args = event[1:-1].split("-")

        # Allow static events (no user_id or lab_id) e.g. opening the door
        _dict = {"epoch": epoch,
                 "event": args[0]}
        n_args = len(args)
        if n_args > 1:
            _dict["user_id"] = args[1]
        if n_args == 3:
            _dict["lab_id"] = args[2]

        data += [_dict]
        controllers.log_mydenox(epoch, "OK", "ok")

    debug("Messages parsed.")
    return data
