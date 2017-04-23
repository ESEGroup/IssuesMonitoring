from ..issues_monitoring import app, Config
from flask import render_template, request, redirect, url_for, session

class Views:
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/login')
    def login():
        return 'Login Page!'

    @app.route('/parser')
    def parser():
        return 'Parser! :D'
