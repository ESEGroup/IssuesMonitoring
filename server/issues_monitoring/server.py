from . import app, Config, views

if __name__ == "server.issues_monitoring.server":
    app.run(host=Config.issues_monitoring.host,
            port=Config.issues_monitoring.port,
            debug=Config.debug)
