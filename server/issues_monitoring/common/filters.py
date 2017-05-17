from datetime import datetime
from .. import app

@app.template_filter('data')
def data(timestamp):
    if timestamp in [None, ""]:
        return "-"
    timestamp = float(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

@app.template_filter('existe')
def existe(var):
    return var is not None

@app.template_filter('hora_min')
def hora_min(timestamp):
    if timestamp in [None, ""]:
        return "-"
    timestamp = float(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%H:%M")

@app.template_filter('user_ids')
def user_ids(usuarios):
    return [u.user_id for u in usuarios]

@app.template_filter('len')
def _len(l):
    return len(l)

@app.template_filter('bool')
def _bool(b):
    return {True: "Sim", False: "Não"}.get(b, "-")

@app.template_filter('int')
def _int(n):
    try:
        return int(n)
    except (ValueError, TypeError):
        return "-"
