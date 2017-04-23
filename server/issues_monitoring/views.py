from ..issues_monitoring import app, Config
from flask import render_template, request, redirect, url_for, session

class Views:
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return 'Login Page!'

    @app.route('/parser', methods=['GET', 'POST'])
    def parser():
        if request.method == 'POST':
            json = request.args or request.form
            print (json)
            return "7"
        return "I can hear you!"
