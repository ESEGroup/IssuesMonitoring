from flask import render_template, request, redirect, url_for, session
from ..common.utils import autenticado
from .. import app, Config, controllers

@app.route('/')
def gerenciar():
    if not autenticado():
        redirect(url_for('login'))

    admin = session.get('admin') or False
    laboratorios = controllers.obter_informacoes_lab(session['user_id'])
    return render_template('gerenciar.html',
                           admin=admin,
                           laboratorios=laboratorios)

@app.route('/', methods=["POST"])
def gerenciar_post():
    if not autenticado():
        redirect(url_for('login'))

    user_id = session["id"]
    nome = request.form.get("nome-lab") or ""
    endereco = request.form.get("endereco-lab") or ""
    intervalo_parser = request.form.get("intervalo-parser") or ""
    intervalo_arduino = request.form.get("intervalo-arduino") or ""
    args = [user_id,
            nome,
            endereco,
            intervalo_parser,
            intervalo_arduino]
    if "" not in args:
        controllers.atualizar_informacoes_lab(*args)

    return redirect(url_for("gerenciar"))
 
@app.route('/registrar-equipamneto', methods=["POST"])
def registrar_equipamento():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    temp_min = request.form.get('temp-min')
    temp_max = request.form.get('temp-max')
    MAC = request.form.get('endereco-mac')
    args = [temp_min, temp_max, MAC]
    if "" not in args:
        controllers.registrar_equipamento(*args)

    return redirect(url_for('gerenciar'))

@app.route('/remover-equipamento', methods=["POST"])
def remover_equipamento():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    _id = request.form.get('equipamento-id')
    if _id != "":
        controllers.remover_equipamento(_id)
    return redirect(url_for('gerenciar'))

@app.route('/registrar-usuario-lab', methods=["POST"])
def registrar_usuario_lab():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    user_id = request.form.get('user_id') or ""
    nome = request.form.get('nome') or ""
    lab_id = request.form.get('laboratorio') or ""
    email = request.form.get('email') or ""
    aprovar = request.form.get('aprovar') or ""
    args = [lab_id, user_id, nome, email, aprovar]
    if "" not in args:
        controllers.cadastrar_usuario_lab(*args)

    return redirect(url_for('gerenciar'))

@app.route('/remover-usuario-lab', methods=["POST"])
def remover_usuario_lab():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    id_lab = request.form.get('id_lab')
    user_id = request.form.get('user_id')
    args = [id_lab, user_id]
    if "" not in args:
        controllers.remover_usuario_lab(*args)

    return redirect(url_for('gerenciar'))

@app.route('/login')
def login():
    if autenticado():
        return redirect(url_for('gerenciar'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if autenticado():
        return redirect(url_for('gerenciar'))

    usuario = request.form.get('login') or ''
    senha = request.form.get('password') or ''
    if '' in [usuario, senha]:
        return redirect(url_for('login'))

    (session['id'],
     session['admin']) = controllers.autenticar(usuario, senha)
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
    lab_id = request.form.get('laboratorio')
    user_id = request.form.get('user_id')
    nome = request.form.get('nome')
    email = request.form.get('email')
    controllers.cadastrar_usuario_lab(lab_id, user_id, nome, email)
    return redirect(url_for('gerenciar'))

@app.route('/robots.txt')
def robots_txt():
    return "User-Agent: *\nDisallow: /"
