from flask import render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from ..common.utils import autenticado, admin_autenticado, hoje
from .. import app, Config, controllers
from ..models import Laboratorio

@app.route('/')
def root():
    return redirect(url_for('laboratorios'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if autenticado():
        return redirect(url_for('laboratorios'))

    return render_template('login.html',
                           pagina='login',
                           admin=admin_autenticado())

@app.route('/login', methods=['POST'])
def login_post():
    if autenticado():
        return redirect(url_for('laboratorios'))

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
        session.clear()
        kwargs = {"e": "Usuário ou senha incorretos ou usuário não aprovado."}
    return redirect(url_for('login', **kwargs))

@app.route('/selecionar-laboratorio')
def laboratorios():
    if not autenticado():
        return redirect(url_for('login'))

    laboratorios = controllers.obter_informacoes_labs()
    return render_template('labs.html',
                           laboratorios=laboratorios,
                           admin=admin_autenticado(),
                           pagina='laboratorios')

    args = [id, nome, endereco, intervalo_parser, intervalo_arduino]
    if "" not in args:
        controllers.atualizar_informacoes_lab(*args)

    kwargs = {"c" : "Informações atualizadas com sucesso."}
    return redirect(url_for("laboratorio", id=id, nome=nome, **kwargs))

@app.route('/laboratorio/<id>/')
@app.route('/laboratorio/<id>/<nome>')
def laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    laboratorio = controllers.obter_laboratorio(id)
    return render_template('gerenciar.html',
                           laboratorio=laboratorio,
                           lab_id=laboratorio.id,
                           lab_nome=laboratorio.nome,
                           admin=admin_autenticado(),
                           pagina='gerenciar')

@app.route('/editar-laboratorio/<id>/')
@app.route('/editar-laboratorio/<id>/<nome>')
def editar_laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    laboratorio = controllers.obter_laboratorio(id)

    return render_template('editar_lab.html',
                           lab_id=id,
                           lab_nome=nome,
                           admin=admin_autenticado(),
                           pagina='editar_laboratorio',
                           laboratorio=laboratorio)

@app.route('/editar-laboratorio/<id>/', methods=["POST"])
@app.route('/editar-laboratorio/<id>/<nome>', methods=["POST"])
def editar_laboratorio_post(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    nome = request.form.get("nome") or ''
    endereco = request.form.get("endereco") or ' '
    intervalo_parser = request.form.get("intervalo-parser") or ''
    intervalo_arduino = request.form.get("intervalo-arduino") or ''

    args = [id, nome, endereco, intervalo_parser, intervalo_arduino]
    if "" not in args:
        if (endereco is ' '):
            args[2] = ''
        controllers.atualizar_informacoes_lab(*args)
        kwargs = {"c" : "Informações cadastrais atualizadas com sucesso."}
        return redirect(url_for("laboratorio", id=id, nome=nome, **kwargs))
    else:
        kwargs = {"e" : "Por favor, preencha todos os campos."}
        return redirect(url_for('zona_de_conforto', id=id, nome=nome, **kwargs))

@app.route('/zona-de-conforto/<id>/')
@app.route('/zona-de-conforto/<id>/<nome>')
def zona_de_conforto(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    zc = controllers.obter_zona_de_conforto(id)
    return render_template('alterar_zona_conforto.html',
                           lab_id=zc.lab_id,
                           lab_nome=zc.nome_laboratorio,
                           admin=admin_autenticado(),
                           pagina='zona_de_conforto',
                           zona_conforto=zc)

@app.route('/zona-de-conforto/<id>/', methods=["POST"])
@app.route('/zona-de-conforto/<id>/<nome>', methods=["POST"])
def zona_de_conforto_post(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    temp_min = request.form.get("temp-min") or ''
    temp_max = request.form.get("temp-max") or ''
    umid_min = request.form.get("umid-min") or ''
    umid_max = request.form.get("umid-max") or ''

    args = [temp_min, temp_max, umid_min, umid_max, id]
    if "" not in args:
        controllers.atualizar_zona_de_conforto(*args)
        kwargs = {"c" : "Zona de Conforto atualizada com sucesso."}
        return redirect(url_for("laboratorio", id=id, nome=nome, **kwargs))
    else:
        kwargs = {"e" : "Por favor, preencha todos os campos."}
        return redirect(url_for('zona_de_conforto', id=id, nome=nome, **kwargs))

@app.route('/usuarios-lab/<id>/')
@app.route('/usuarios-lab/<id>/<nome>')
def usuarios_laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    usuarios_laboratorio = controllers.obter_usuarios_laboratorio(id)

    usuarios_tmp = controllers.obter_usuarios_laboratorios()
    usuarios_lab_ids = [u.user_id for u in usuarios_laboratorio]
    usuarios = [usuario for usuario in usuarios_tmp if usuario.user_id not in usuarios_lab_ids]

    return render_template('lista_membros.html',
                           lab_id=id,
                           lab_nome=nome,
                           usuarios=usuarios,
                           usuarios_laboratorio=usuarios_laboratorio,
                           admin=admin_autenticado(),
                           pagina="usuarios_laboratorio")

@app.route('/cadastro-lab', methods=["POST"])
def cadastro_lab():
    if not admin_autenticado():
        return redirect(url_for('login'))

    nome = request.form.get("nome") or ""
    endereco = request.form.get("endereco") or " "
    intervalo_parser = request.form.get("intervalo-parser") or ""
    intervalo_arduino = request.form.get("intervalo-arduino") or ""
    temp_min = request.form.get("temp-min") or ""
    temp_max = request.form.get("temp-max") or ""
    umid_min = request.form.get("umid-min") or ""
    umid_max = request.form.get("umid-max") or ""
    args = [nome, endereco, intervalo_parser, intervalo_arduino,
            temp_min, temp_max, umid_min, umid_max]
    if "" not in args:
        if (endereco is " "):
            args[1] = ""
        controllers.cadastro_laboratorio(*args)
        kwargs = {"c" : "Laboratório cadastrado com sucesso."}
    else:
        kwargs = {"e" : "Por favor, lembre-se de preencher o nome do laboratório."}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro_usuario_sistema.html',
                           pagina='cadastro',
                           admin=admin_autenticado())

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
            kwargs = {"e": "Login ou e-mail já utilizados."}
            return redirect(url_for("cadastro", **kwargs))
    kwargs = {"c": "Usuário enviado para aprovação!"}
    return redirect(url_for('login', **kwargs))

@app.route('/aprovar-usuario-lab/<id>', methods=["POST"])
def aprovar_usuario_lab(id):
    if not admin_autenticado():
        return redirect(url_for('usuarios_laboratorio'))

    aprovar = request.form.get('aprovar') == 'true'
    controllers.aprovar_usuario_lab(id, aprovar)
    kwargs = {"c" : "Aprovação alterada com sucesso!"}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/adicionar-usuario-lab/<id>/', methods=["POST"])
@app.route('/adicionar-usuario-lab/<id>/<nome>', methods=["POST"])
def adicionar_usuario_lab(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login'))

    user_id = request.form.get('id-user') or ''
    if user_id != "":
        controllers.adicionar_usuario_lab(id, user_id)
        kwargs = {'c': "Usuário adicionado ao laboratório com sucesso."}
    else:
        kwargs = {'e': "Por favor, escolha um usuário."}

    return redirect(url_for('usuarios_laboratorio', id=id, nome=nome, **kwargs))

@app.route('/cadastro-usuario-lab')
def cadastro_usuario_lab():
    laboratorios = controllers.obter_laboratorios()
    if len(laboratorios) == 0:
        kwargs = {"e" : "Primeiro, cadastre um laboratório."}
        return redirect(url_for("laboratorios", _anchor="cadastrar", **kwargs))

    return render_template('cadastro_usuario_lab.html',
                           pagina='cadastro_usuario_lab',
                           admin=admin_autenticado(),
                           laboratorios=laboratorios)

@app.route('/cadastro-usuario-lab', methods=['POST'])
def cadastro_usuario_lab_post():
    lab_id = request.form.get('id-lab') or ''
    user_id = request.form.get('id-user') or ''
    nome = request.form.get('nome') or ''
    email = request.form.get('email') or ''
    args = [lab_id, user_id, nome, email]

    success = False
    if "" not in args:
        success = controllers.cadastro_usuario_lab(*args)

    if not success:
        kwargs = {"e": "Id de usuário já existente."}
    else:
        kwargs = {"c" : "Usuário cadastrado com sucesso."}

    if autenticado():
        url = 'laboratorio'
        kwargs['id'] = lab_id
    else:
        url = 'cadastro_usuario_lab'
    return redirect(url_for(url, **kwargs))

@app.route('/cadastro-equipamento', methods=["POST"])
def cadastro_equipamento():
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    lab_id = request.form.get('id-lab')
    temp_min = request.form.get('temp-min')
    temp_max = request.form.get('temp-max')
    MAC = request.form.get('endereco-mac')
    args = [lab_id, temp_min, temp_max, MAC]
    if "" not in args:
        controllers.cadastro_equipamento(*args)

    kwargs = {"c" : "Equipamento cadastrado com sucesso."}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/log-eventos/<id>/<nome>/')
def log_eventos_hoje(id, nome):
    _hoje = datetime.fromtimestamp(hoje()).strftime("%d-%m-%Y")
    return redirect(url_for('log_eventos',
                            id=id,
                            nome=nome,
                            dia=_hoje))

@app.route('/log-eventos/<id>/<nome>/<dia>')
def log_eventos(id, nome, dia):
    if not autenticado():
        return redirect(url_for('login'))

    usuarios_presentes = controllers.usuarios_presentes(id)

    dia = int(datetime.strptime(dia, "%d-%m-%Y").timestamp())
    log_eventos = controllers.log_eventos(id, dia)

    proximo_dia = controllers.data_proximo_evento_mydenox(id, dia)
    dia_anterior = controllers.data_evento_anterior_mydenox(id, dia)

    return render_template('log_presenca.html',
                           eventos=log_eventos,
                           proximo_dia=proximo_dia,
                           dia_anterior=dia_anterior,
                           usuarios_presentes=usuarios_presentes,
                           pagina='log_eventos',
                           admin=admin_autenticado(),
                           lab_id=id,
                           lab_nome=nome,
                           dia=dia)

@app.route('/aprovar-usuario')
def aprovar_usuario():
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    usuarios = controllers.obter_usuarios_sistema()
    return render_template('aprovar_usuario_sistema.html',
                           pagina='aprovar_usuario',
                           admin=True,
                           usuarios=usuarios)

@app.route('/aprovar-usuario/<id>', methods=["POST"])
def aprovar_usuario_post(id):
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    aprovar = request.form.get('aprovar') == 'true'
    controllers.aprovar_usuario(id, aprovar)

    if aprovar:
        kwargs = {"c": "Usuário aprovado com sucesso."}
    else:
        kwargs = {"c": "Aprovação do usuário removida com sucesso."}

    return redirect(url_for('laboratorios', **kwargs))

@app.route('/editar-status-admin/<id>', methods=["POST"])
def editar_status_administrador(id):
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    aprovar = request.form.get('aprovar') == 'true'
    controllers.editar_status_administrador(id, aprovar)

    kwargs = {"c": "Status de administrador alterado com sucesso."}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/equipamentos-lab/<id>/')
@app.route('/equipamentos-lab/<id>/<nome>')
def equipamentos_laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    return render_template('lista_equipamentos.html',
                           admin   = admin_autenticado(),
                           lab_id  = id,
                           lab_nome= nome,
                           pagina  = "equipamentos_laboratorio")

@app.route('/system-status')
def system_status():
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login."}
        return redirect(url_for('login', **kwargs))

    # pegar as infos do banco
    timestamp_parser = int(controllers.ultima_atualizacao_parser())
    tempos_arduinos  = controllers.ultima_atualizacao_arduino()
    agora = datetime.today()
    status_componente = "OK"
    dados = []

    # parsear as infos e preencher o dicionario com os dados
    if ((datetime.fromtimestamp(timestamp_parser)) <
        (agora - timedelta(minutes=controllers.obter_intervalo_parser()))):
        status_componente = "Fora do Ar"

    dados += [{"nome_componente"    : "Parser",
               "ultima_atualizacao" : timestamp_parser,
               "status"             : status_componente}]

    for lab_id in tempos_arduinos:
        status_componente = "OK"
        print(tempos_arduinos[lab_id])
        if ((datetime.fromtimestamp(int(tempos_arduinos[lab_id]))) <
            (agora - timedelta(minutes=Laboratorio.obter_intervalo_arduino(lab_id)))):
            print ("ENTROU")
            status_componente = "Fora do Ar"

        dados += [{"nome_componente"    : "Arduino - Lab " + str(lab_id),
                   "ultima_atualizacao" : int(tempos_arduinos[lab_id]),
                   "status"             : status_componente}]

    return render_template('system-status.html',
                            componentes = dados,
                            pagina = 'system-status')
@app.route('/robots.txt')
def robots_txt():
    return """User-Agent: *<br>\nDisallow: /"""
