from flask import request
from .. import app, Config, controllers

@app.route('/parser', methods=['POST'])
def parser():
    json = request.get_json()
    if json is not None:
        try:
            if json['token'] == Config.token_parser:
                controllers.registrar_presenca(json['data'])
            else:
                return "-1"
        except KeyError:
            pass
    else:
        print("Couldn't get json from POST request")
    return controllers.obter_intervalo_parser()
