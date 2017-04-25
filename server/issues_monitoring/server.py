from ..issues_monitoring import app, Config

app.run(host=Config.issues_monitoring.host, port=Config.issues_monitoring.port, debug=Config.debug)
