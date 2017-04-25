from flask import request
from .. import app, Config, controllers

@app.route('/parser', methods=['POST'])
def parser():
    json = request.get_json()
    if json is not None:
        try:
            token = json['token']
            controllers.registrar_presenca(json['data'])
        except KeyError:
            pass
    else:
        print("Couldn't get json from POST request")
    return controllers.obter_intervalo_parser()
