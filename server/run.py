from config import Config
from subprocess import Popen, DEVNULL

if __name__ == "__main__":
    if Config.debug:
        Popen(["env",
               "FLASK_APP=issues_monitoring/server.py",
               "flask",
               "run"]).wait()
    else:
        host = Config.issues_monitoring.host
        port = Config.issues_monitoring.port
        try:
            Popen(["gunicorn",
                   "issues_monitoring.server:app",
                   "-k",
                   "gevent",
                   "-b",
                   "{}:{}".format(host, port)]).wait()
        except KeyboardInterrupt:
            Popen("kill -9 $(ps aux | grep gunicorn | awk '{print $2}')",
                  shell = True)
