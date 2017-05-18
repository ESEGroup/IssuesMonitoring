from flask import request
from .. import app, Config, controllers

@app.route('/arduino', methods=['POST'])
def arduino():
    json = request.get_json()
    if json is not None:
        try:
            if (controllers.registrar_medidas(json)):
                return "OK"
            else:
                return "NOK \_(-.-)_/"
        except sqlite3.Error:
            return "-2"
        except KeyError:
            pass
    else:
        print("Couldn't get json from POST request")
    return "Couldn't get json from POST request"

@app.route('/arduino', methods=['GET'])
def arduino_get():
    return controllers.listar_todos_mac_arduino()
