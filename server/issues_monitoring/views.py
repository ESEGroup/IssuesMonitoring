from ..issues_monitoring import app, Config
from flask import render_template, request, redirect, url_for, session

@app.route('/')
def hello_world():
    print("Entrou")
    return 'Hello, World!'
