from flask import render_template, request, redirect, url_for, session
from .. import app, Config

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'Login Page!'

@app.route('/robots.txt')
def robots_txt():
    return "User-Agent: *\nDisallow: /"
