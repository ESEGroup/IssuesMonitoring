from datetime import datetime, timedelta
from .. import app

app.jinja_env.filters["existe"] = lambda x: x is not None
app.jinja_env.filters["len"] = len
app.jinja_env.filters["enumerate"] = enumerate
app.jinja_env.filters["bool"] = lambda b: {True: "Sim", False: "Não"}.get(b, "-")
app.jinja_env.filters["trans_evento"] = lambda evento: {"IN": "Entrada", "OUT": "Saída"}[evento.upper()]

@app.template_filter("vazio")
def vazio(texto):
    if type(texto) not in [str, int]:
        return "-"
    return "-" if texto in [None, ""] else texto

@app.template_filter("max_len20")
def max_len20(text):
    return text[:20] + ("..." if len(text) > 20 else "")

@app.template_filter('format_dia_url')
def format_dia_url(dia):
    return datetime.fromtimestamp(dia).strftime("%d-%m-%Y")

@app.template_filter('timestamp')
def timestamp(dia):
    return int(datetime.strptime(dia, "%d-%m-%Y").timestamp())

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
    return datetime.fromtimestamp(timestamp).strftime("%H:%M")


@app.template_filter('dia_mes_ano')
def dia_mes_ano(timestamp):
    if timestamp in [None, ""]:
        return "-"
    timestamp = int(timestamp)
    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")

@app.template_filter('user_ids')
def user_ids(usuarios):
    return [u.user_id for u in usuarios]

@app.template_filter('int')
def _int(n):
    try:
        return int(n)
    except (ValueError, TypeError):
        return "-"
