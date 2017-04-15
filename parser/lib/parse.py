from lib.log import debug
from re import search
from datetime import datetime, timedelta

TIME_REGEXP = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}"
EVENT_REGEXP = r"\[[^\W_]+(-[^\W_]+)?\]"

def parse_messages(messages):
    debug("Parsing messages.")
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

        # Remove [] from [EVENT-user_id] and split them to register
        args = event[1:-1].split("-")

        # Allow static events (no user_id) e.g. opening the door
        _dict = {"epoch": epoch,
                 "event": args[0]}
        if len(args) > 1:
            _dict["user_id"] = args[1]

        data += [_dict]

    debug("Messages parsed.")
    return data
