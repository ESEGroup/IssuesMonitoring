from datetime import datetime, timedelta
from .. import app

@app.template_filter('trans_evento')
def trans_evento(evento):
    return {"IN": "Entrada",
            "OUT": "Saída"}[evento.upper()]

@app.template_filter('data')
def data(timestamp):
    if timestamp in [None, ""]:
        return "-"
    timestamp = int(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")

@app.template_filter('data_segundos')
def data(timestamp):
    if timestamp in [None, ""]:
        return "-"
    timestamp = int(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")

@app.template_filter('hora_min')
def hora_min(timestamp):
    if timestamp in [None, ""]:
        return "-"
    timestamp = int(timestamp)
    return (datetime(1970, 1, 1) + timedelta(seconds=timestamp)).strftime("%H:%M")

@app.template_filter('dia_mes_ano')
def dia_mes_ano(timestamp):
    if timestamp in [None, ""]:
        return "-"
    timestamp = int(timestamp)
    return (datetime(1970, 1, 1) + timedelta(seconds=timestamp)).strftime("%d/%m/%Y")

@app.template_filter('existe')
def existe(var):
    return var is not None


@app.template_filter('user_ids')
def user_ids(usuarios):
    return [u.user_id for u in usuarios]

@app.template_filter('len')
def _len(l):
    return len(l)

@app.template_filter('enumerate')
def _enumerate(l):
    return enumerate(l)

@app.template_filter('bool')
def _bool(b):
    return {True: "Sim", False: "Não"}.get(b, "-")

@app.template_filter('int')
def _int(n):
    try:
        return int(n)
    except (ValueError, TypeError):
        return "-"

@app.template_filter('format_dia_url')
def format_dia_url(dia):
    return datetime.fromtimestamp(dia).strftime("%d-%m-%Y")

@app.template_filter('timestamp')
def timestamp(dia):
    return int(datetime.strptime(dia, "%d-%m-%Y").timestamp())
