import sqlite3
from flask import redirect, url_for, render_template
from .. import app

@app.errorhandler(sqlite3.Error)
def db_error(error):
    return redirect(url_for('server_error'))

@app.route('/500')
def server_error():
    return render_template("500.html") , 500
