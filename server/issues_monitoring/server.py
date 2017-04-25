from ..issues_monitoring import app, Config
from . import views

app.run(host=Config.issues_monitoring.host, port=Config.issues_monitoring.port, debug=Config.debug)
