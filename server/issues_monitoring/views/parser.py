from flask import request
from .. import app, Config

@app.route('/parser', methods=['POST'])
def parser():
    json = request.get_json()
    if json is not None:
        for entry in json['data']:
            print (entry)
    else:
        print("Couldn't get json from POST request")
    return "7"
