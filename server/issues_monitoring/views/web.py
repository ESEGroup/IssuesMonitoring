from flask import render_template, request, redirect, url_for, session
from ..common.utils import autenticado
from .. import app, Config, controllers

@app.route('/')
def manage():
    #if not autenticado():
    #    redirect(url_for('login'))
    (nome_lab,
     endereco_lab,
     membros,
     intervalo_parser,
     intervalo_arduino,
     enderecos_mac) = controllers.obter_informacoes_lab()
    return render_template('manage.html',
                           nome_lab,
                           endereco_lab,
                           membros,
                           intervalo_parser,
                           intervalo_arduino
                           enderecos_mac)

@app.route('/', methods=["POST"])
def manage_post():
    if not autenticado():
        redirect(url_for('login'))
    user_id = session["id"]
    nome = request.form.get("nome-lab") or ""
    endereco = request.form.get("endereco-lab") or ""
    intervalo_parser = request.form.get("intervalo-parser")
    intervalo_arduino = request.form.get("intervalo-arduino")
    controllers.atualizar_informacoes_lab(user_id,
                                          nome,
                                          endereco,
                                          intervalo_parser,
                                          intevalo_arduino)
    return redirect(url_for("manage"))
    

@app.route('/login')
def login():
    if autenticado():
        return redirect(url_for('manage'))
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
        now = datetime.now().timestamp()
        session['expiration'] = now + Config.session_duration
    else:
        session.pop('id', None)
    return redirect(url_for('login'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro_usuario_sistema.html')

@app.route('/cadastro', methods=['POST'])
def cadastro_post():
    login = request.form.get('login')
    senha = request.form.get('senha')
    email = request.form.get('email')
    nome = request.form.get('nome')
    controllers.cadastrar_usuario_sistema(login, senha, email, nome)
    return redirect(url_for('login'))

@app.route('/cadastro-usuario-lab')
def cadastro_lab():
    return render_template('cadastro_usuario_lab.html')

@app.route('/cadastro-usuario-lab', methods=['POST'])
def cadastro_lab_post():
    user_id = request.form.get('user_id')
    nome = request.form.get('nome')
    email = request.form.get('email')
    controllers.cadastrar_usuario_lab(user_id, nome, email)
    return redirect(url_for('manage'))

@app.route('/robots.txt')
def robots_txt():
    return "User-Agent: *\nDisallow: /"
