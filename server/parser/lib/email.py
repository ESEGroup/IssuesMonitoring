from .. import Config
from .log import debug, log
from imaplib import IMAP4_SSL

DEBUG = Config.debug
HOST = Config.imap_host.host
USERNAME = Config.email
PASSWORD = Config.email_password

class NoMessages(Exception):
    pass

def fetch_new_emails(host=HOST, username=USERNAME, password=PASSWORD):
    debug("Checking for unread e-mails.")
    ids = []
    messages = []
    email = IMAP4_SSL(host)
    email.login(username, password)

    # Only mark as read in production to make debugging easier
    email.select(readonly=DEBUG)

    # Get unread e-mail ids sent from MyDenox to parse messages
    # (and mark as unread if it fails to send events to the Server)
    _type, data = email.search(None,
                               'ALL',
                               '(UNSEEN)')
    ids = data[0].split()

    if len(ids) == 0:
        email.close()
        email.logout()
        raise NoMessages

    debug("Fetching {} new e-mails.".format(len(ids)))
    for num in ids:
        _type, data = email.fetch(num, '(RFC822)')
        messages += [data[0][1].decode('utf-8')]
    email.close()
    email.logout()

    debug("Fetched e-mails.")
    return ids, messages

def mark_as_unread(ids, host=HOST, username=USERNAME, password=PASSWORD):
    debug("Marking {} emails as unread.".format(len(ids)))
    try:
        with IMAP4_SSL(host) as email:
            email.login(username, password)
            email.select()
            for e_id in ids:
                email.store(e_id, '-FLAGS', '\Seen')
    except OSError:
        log("Failed to mark {} e-mails as unread".format(len(ids)))
