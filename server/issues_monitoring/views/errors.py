import sqlite3
from flask import redirect, url_for, render_template
from ..common.utils import autenticado, admin_autenticado
from .. import app

@app.errorhandler(sqlite3.Error)
def db_error(error):
    print(error)
    return render_template("500.html",
                            admin=admin_autenticado(),
                            autenticado=autenticado()) , 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html",
                            admin=admin_autenticado(),
                            autenticado=autenticado()) , 404

@app.route('/500')
@app.errorhandler(500)
def server_error():
    return render_template("500.html",
                            admin=admin_autenticado(),
                            autenticado=autenticado()) , 500
