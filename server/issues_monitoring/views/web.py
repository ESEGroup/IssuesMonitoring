from flask import render_template, request, redirect, url_for, session
from datetime import datetime
from ..common.utils import autenticado, admin_autenticado, hoje
from .. import app, Config, controllers

@app.route('/')
def root():
    if not autenticado():
        return redirect(url_for('login'))
    return redirect(url_for('gerenciar'))

@app.route('/gerenciar/')
def gerenciar():
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    admin = admin_autenticado()
    usuarios_sistema = controllers.obter_usuarios_sistema()
    usuarios_lab = controllers.obter_usuarios_laboratorios()
    laboratorios = controllers.obter_informacoes_labs()
    return render_template('gerenciar.html',
                           admin=admin,
                           usuarios_sistema=usuarios_sistema,
                           usuarios_lab=usuarios_lab,
                           laboratorios=laboratorios)

@app.route('/gerenciar', methods=["POST"])
def gerenciar_post():
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    lab_id = request.form.get("id-lab") or ''
    nome = request.form.get("nome-lab") or ''
    endereco = request.form.get("endereco-lab") or ''
    intervalo_parser = request.form.get("intervalo-parser") or ''
    intervalo_arduino = request.form.get("intervalo-arduino") or ''
    temp_min = request.form.get("temp-min") or ''
    temp_max = request.form.get("temp-max") or ''
    umid_min = request.form.get("umid-min") or ''
    umid_max = request.form.get("umid-max") or ''

    args = [lab_id, nome, endereco, intervalo_parser,
            intervalo_arduino, temp_min, temp_max, umid_min, umid_max]
    if "" not in args:
        controllers.atualizar_informacoes_lab(*args)

    kwargs = {"c" : "Informações atualizadas com sucesso!"}
    return redirect(url_for("gerenciar", **kwargs))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login/')
def login():
    if autenticado():
        return redirect(url_for('gerenciar'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if autenticado():
        return redirect(url_for('gerenciar'))

    usuario = request.form.get('login') or ''
    senha = request.form.get('senha') or ''
    if '' in [usuario, senha]:
        return redirect(url_for('login'))

    (session['id'],
     session['admin']) = controllers.autenticar(usuario, senha)

    if session['id'] is not None:
        now = int(datetime.now().timestamp())
        session['expiration'] = now + Config.session_duration
        kwargs = {}
    else:
        session.pop('id', None)
        kwargs = {"e": "Usuário ou senha incorretos ou usuário não aprovado"}
    return redirect(url_for('login', **kwargs))

@app.route('/cadastro-lab/')
def cadastro_lab():
    if not admin_autenticado():
        return redirect(url_for('login'))
    return render_template('cadastro_lab.html',
                           autenticado=autenticado())

@app.route('/cadastro-lab', methods=["POST"])
def cadastro_lab_post():
    if not admin_autenticado():
        return redirect(url_for('login'))

    nome = request.form.get("nome") or ""
    endereco = request.form.get("endereco") or ""
    intervalo_parser = request.form.get("intervalo-parser") or ""
    intervalo_arduino = request.form.get("intervalo-arduino") or ""
    temp_min = request.form.get("temp-min") or ""
    temp_max = request.form.get("temp-max") or ""
    umid_min = request.form.get("umid-min") or ""
    umid_max = request.form.get("umid-max") or ""
    args = [nome, endereco, intervalo_parser, intervalo_arduino,
            temp_min, temp_max, umid_min, umid_max]
    if "" not in args:
        controllers.cadastro_laboratorio(*args)

    kwargs = {"c" : "Laboratório cadastrado com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/cadastro/')
def cadastro():
    return render_template('cadastro_usuario_sistema.html',
                           autenticado=autenticado())

@app.route('/cadastro', methods=['POST'])
def cadastro_post():
    login = request.form.get('login') or ''
    senha = request.form.get('senha') or ''
    email = request.form.get('email') or ''
    nome = request.form.get('nome') or ''
    args = [login, senha, email, nome]

    if '' not in args:
        if not controllers.cadastro_usuario_sistema(login,
                                                     senha,
                                                     email,
                                                     nome):
            kwargs = {"e": "Login ou e-mail já utilizados"}
            return redirect(url_for("cadastro", **kwargs))
    kwargs = {"c": "Usuário enviado para aprovação!"}
    return redirect(url_for('login', **kwargs))

@app.route('/editar-status-administrador', methods=["POST"])
def editar_status_administrador():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    user_id = request.form.get('id-user')
    administrador = request.form.get('admin') == "1"
    controllers.editar_status_administrador(user_id, administrador)
    kwargs = {"c" : "Status de administrador alterado com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/editar-autorizacao-usuario', methods=["POST"])
def editar_autorizacao_usuario():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    user_id = request.form.get('id-user')
    aprovar = request.form.get('data') == "None"
    controllers.editar_autorizacao_usuario(user_id, aprovar)
    kwargs = {"c" : "Aprovação alterada com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/cadastro-usuario-lab/')
def cadastro_usuario_lab():
    laboratorios = controllers.obter_laboratorios()
    if len(laboratorios) == 0:
        kwargs = {"e" : "Primeiro, cadastre um laboratório"}
        return redirect(url_for("cadastro_lab", **kwargs))

    usuarios = controllers.obter_usuarios_laboratorios()
    return render_template('cadastro_usuario_lab.html',
                           laboratorios=laboratorios,
                           usuarios=usuarios,
                           admin=admin_autenticado(),
                           autenticado=autenticado())

@app.route('/adicionar-usuario-lab', methods=['POST'])
def adicionar_usuario_lab():
    lab_id = request.form.get('id-lab') or ''
    user_id = request.form.get('id-user') or ''
    if "" not in [lab_id, user_id]:
        controllers.adicionar_usuario_lab(lab_id, user_id)
        return redirect(url_for("gerenciar"))
    return redirect(url_for("cadastro_usuario_lab"))

@app.route('/cadastro-usuario-lab', methods=['POST'])
def cadastro_usuario_lab_post():
    lab_id = request.form.get('id-lab') or ''
    user_id = request.form.get('id-user') or ''
    nome = request.form.get('nome') or ''
    email = request.form.get('email') or ''

    aprovar = (admin_autenticado()
               and request.form.get('aprovar') == 'on')
    args = [lab_id, user_id, nome, email, aprovar]

    success = False
    if "" not in args:
        success = controllers.cadastro_usuario_lab(*args)

    if not success:
        kwargs = {"e": "Id de usuário já existe"}
    else:
        kwargs = {"c" : "Usuário cadastrado com sucesso!"}

    if autenticado():
        url = 'gerenciar'
    else:
        url = 'cadastro_usuario_lab'
    return redirect(url_for(url, **kwargs))

@app.route('/remover-usuario-lab', methods=["POST"])
def remover_usuario_lab():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    id_lab = request.form.get('id-lab')
    user_id = request.form.get('id-user')
    args = [id_lab, user_id]
    if "" not in args:
        controllers.remover_usuario_lab(*args)

    kwargs = {"c" : "Usuário removido com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/autorizar-usuario-lab', methods=["POST"])
def autorizar_usuario_lab():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    lab_id = request.form.get('id-lab')
    user_id = request.form.get('id-user')
    controllers.autorizar_usuario_lab(lab_id, user_id)
    kwargs = {"c" : "Usuário autorizado com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/cadastro-equipamento', methods=["POST"])
def cadastro_equipamento():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    lab_id = request.form.get('id-lab')
    temp_min = request.form.get('temp-min')
    temp_max = request.form.get('temp-max')
    MAC = request.form.get('endereco-mac')
    args = [lab_id, temp_min, temp_max, MAC]
    if "" not in args:
        controllers.cadastro_equipamento(*args)

    kwargs = {"c" : "Equipamento cadastrado com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/remover-equipamento', methods=["POST"])
def remover_equipamento():
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    _id = request.form.get('id-equipamento')
    if _id != "":
        controllers.remover_equipamento(_id)

    kwargs = {"c" : "Equipamento removido com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/<lab_id>/usuarios-presentes/')
def usuarios_presentes(lab_id):
    if not autenticado():
        return redirect(url_for('login'))

    usuarios_presentes = controllers.usuarios_presentes(lab_id)
    hoje_formatado = datetime.fromtimestamp(hoje()).strftime("%d-%m-%Y")
    return render_template('usuarios_presentes.html',
                           lab_id=lab_id,
                           hoje=hoje_formatado,
                           usuarios_presentes=usuarios_presentes)

@app.route('/<lab_id>/log-eventos/')
def log_eventos_hoje(lab_id):
    _hoje = datetime.fromtimestamp(hoje()).strftime("%d-%m-%Y")
    return redirect(url_for('log_eventos',
                            lab_id=lab_id,
                            dia=_hoje))

@app.route('/<lab_id>/log-eventos/<dia>/')
def log_eventos(lab_id, dia):
    if not autenticado():
        return redirect(url_for('login'))

    dia = int(datetime.strptime(dia, "%d-%m-%Y").timestamp())
    log_eventos = controllers.log_eventos(lab_id, dia)

    proximo_dia = controllers.data_proximo_evento_mydenox(lab_id, dia)
    dia_anterior = controllers.data_evento_anterior_mydenox(lab_id, dia)

    return render_template('logs_entrada_saida.html',
                           eventos=log_eventos,
                           proximo_dia=proximo_dia,
                           dia_anterior=dia_anterior,
                           lab_id=lab_id,
                           dia=dia)

@app.route('/usuarios-laboratorios/')
def usuarios_laboratorios():
    if not autenticado():
        return redirect(url_for('gerenciar'))

    usuarios = controllers.obter_usuarios_laboratorios()
    return render_template('usuarios_laboratorios.html',
                           usuarios=usuarios)

@app.route('/editar-usuario-lab/<user_id>/')
def editar_usuario_lab(user_id):
    if not autenticado():
        return redirect(url_for('gerenciar'))

    usuario = controllers.obter_usuario_lab(user_id)
    return render_template('editar_usuario_lab.html',
                           usuario=usuario,
                           admin=admin_autenticado())

@app.route('/editar-usuario-lab/<user_id>/', methods=["post"])
def editar_usuario_lab_post(user_id):
    if not autenticado():
        return redirect(url_for('gerenciar'))

    nome = request.form.get('nome') or ''
    email = request.form.get('email') or ''

    args = [user_id, nome, email]
    if "" not in args:
        controllers.editar_usuario_lab(*args)
    kwargs = {"c" : "Usuário editado com sucesso!"}
    return redirect(url_for('usuarios_laboratorios', **kwargs))

@app.route('/remover-usuario-lab/<user_id>/', methods=["POST"])
def remover_usuario_de_todos_labs(user_id):
    if not autenticado():
        return redirect(url_for('gerenciar'))

    controllers.remover_usuario_de_todos_labs(user_id)

    kwargs = {"c" : "Usuário removido com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/editar-usuario-sistema/<user_id>/')
def editar_usuario_sistema(user_id):
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    usuario = controllers.obter_usuario_sistema(user_id)
    return render_template("editar_usuario_sistema.html",
                           usuario=usuario)

@app.route('/editar-usuario-sistema/<user_id>/', methods=["POST"])
def editar_usuario_sistema_post(user_id):
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    login = request.form.get('login') or ''
    nome = request.form.get('nome') or ''
    email = request.form.get('email') or ''

    args = [user_id, login, nome, email]
    if "" not in args:
        controllers.editar_usuario_sistema(*args)

    kwargs = {"c" : "Usuário editado com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/remover-usuario-sistema/<user_id>/', methods=["POST"])
def remover_usuario_sistema(user_id):
    if not admin_autenticado():
        return redirect(url_for('gerenciar'))

    controllers.remover_usuario_sistema(user_id)

    kwargs = {"c" : "Usuário removido com sucesso!"}
    return redirect(url_for('gerenciar', **kwargs))

@app.route('/robots.txt')
def robots_txt():
    return """User-Agent: *<br>\nDisallow: /"""
