from sys import stderr
from datetime import datetime
from config import DEBUG, LOG_FILE, LOG_TIMESTAMP_FORMAT

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
