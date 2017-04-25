from flask import render_template, request, redirect, url_for, session
from datetime import datetime
from .. import app, Config, controllers

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if controller.autenticado(session):
        return redirect(url_for('manage'))

    usuario = request.form.get('login') or ''
    senha = request.form.get('password') or ''
    if '' in [usuario, senha]:
        return redirect(url_for('login'))

    session['user_id'] = controllers.autenticar_usuario(usuario, senha)
    if session['user_id'] is not None:
        session['expiration'] = datetime.now().timestamp() + Config.session_duration
    else:
        session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro_usuario_lab.html')

@app.route('/cadastro', methods=['POST'])
def cadastro_post():
    pass

@app.route('/manage')
def manage():
    pass

@app.route('/robots.txt')
def robots_txt():
    return "User-Agent: *\nDisallow: /"
