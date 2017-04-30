from datetime import datetime
from .. import app

@app.template_filter('data')
def data(timestamp):
    if timestamp is None:
        return "-"
    timestamp = float(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

@app.template_filter('bool')
def _bool(b):
    return {True: "Sim", False: "Não"}.get(b, "-")

@app.template_filter('int')
def _int(n):
    try:
        return int(n)
    except (ValueError, TypeError):
        return "-"
