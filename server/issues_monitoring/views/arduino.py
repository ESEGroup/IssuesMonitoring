from flask import request
from .. import app, Config, controllers
from ..models import Laboratorio
import json
import sqlite3

@app.route('/arduino', methods=['POST'])
def arduino():
    j = request.get_json()
    if j is not None:
        try:
            lab_id = j["lab_id"]
            print(j)
            if (controllers.registrar_medidas(j)):
                return str(Laboratorio.obter_intervalo_arduino(lab_id))
            else:
                return "-1"
        except sqlite3.Error:
            return "-2"
        except KeyError:
            pass
    else:
        print("Couldn't get json from POST request")
    return "Couldn't get json from POST request"

@app.route('/arduino', methods=['GET'])
def arduino_get():
    json_str = request.args.get("json", None)
    if json_str is not None:
        j = json.loads(json_str)
        try:
            if (controllers.registrar_medidas(j)):
                lab_id = j["lab_id"]
                return str(Laboratorio.obter_intervalo_arduino(lab_id))
            else:
                return "-1"
        except sqlite3.Error:
            return "-2"
        except KeyError:
            pass
    return "OK" 
