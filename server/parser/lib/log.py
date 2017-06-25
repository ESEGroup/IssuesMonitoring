from sys import stderr
from datetime import datetime
from .. import Config

DEBUG = Config.debug
LOG_FILE = Config.log_file
LOG_TIMESTAMP_FORMAT = Config.log_timestamp_format

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
        with open(LOG_FILE, 'a') as f:
            kwargs["file"] = f
            print(message, **kwargs)
