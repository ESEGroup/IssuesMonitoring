from flask import render_template, request, redirect, url_for, session
from ..common.utils import autenticado
from .. import app, Config, controllers

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if autenticado():
        return redirect(url_for('manage'))

    usuario = request.form.get('login') or ''
    senha = request.form.get('password') or ''
    if '' in [usuario, senha]:
        return redirect(url_for('login'))

    session['id'] = controllers.autenticar(usuario, senha)
    if session['id'] is not None:
        session['expiration'] = datetime.now().timestamp() + Config.session_duration
    else:
        session.pop('id', None)
    return redirect(url_for('login'))

@app.route('/cadastro-usuario-lab')
def cadastro():
    return render_template('cadastro_usuario_lab.html')

@app.route('/cadastro-usuario-lab', methods=['POST'])
def cadastro_post():
    user_id = request.form.get('user_id')
    nome = request.form.get('nome')
    email = request.form.get('email')
    controllers.cadastrar_usuario_lab(user_id, nome, email)
    return redirect(url_for('home'))

@app.route('/manage')
def manage():
    pass

@app.route('/robots.txt')
def robots_txt():
    return "User-Agent: *\nDisallow: /"
