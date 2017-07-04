from os import getcwd, stat
from os.path import join
from flask          import render_template, request, redirect, url_for, session, Response
from werkzeug.datastructures import Headers
from datetime       import datetime, timedelta
from ..common.erros import NaoAutorizado, InformacoesIncorretas
from ..common.utils import (autenticado, admin_autenticado, hoje, agora,
                            get_interval_means, random_string)
from ..             import app, Config, controllers
import json
import pdfkit

class HeadlessPDFKit(pdfkit.PDFKit):
    def command(self, path=None):
        return ['xvfb-run', '--'] + super().command(path)

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
                           autenticado=autenticado(),
                           admin=admin_autenticado())

@app.route('/login', methods=['POST'])
def login_post():
    if autenticado():
        return redirect(url_for('laboratorios'))

    usuario = request.form.get('login') or ''
    senha = request.form.get('senha') or ''
    if '' in [usuario, senha]:
        kwargs = {"e": "Por favor preencha todos os campos"}
        return redirect(url_for('login', **kwargs))

    try:
        (session['id'],
         session['admin']) = controllers.autenticar(usuario, senha)
        now = int(datetime.now().timestamp())
        session['expiration'] = now + Config.session_duration
        kwargs = {}
    except NaoAutorizado:
        kwargs = {"e": "Usuário não autorizado"}
    except InformacoesIncorretas:
        kwargs = {"e": "Usuário ou senha incorretos"}

    return redirect(url_for('login', **kwargs))

@app.route('/selecionar-laboratorio')
def laboratorios():
    if not autenticado():
        return redirect(url_for('login'))

    laboratorios = controllers.obter_informacoes_labs()
    return render_template('labs.html',
                           laboratorios=laboratorios,
                           autenticado=autenticado(),
                           admin=admin_autenticado(),
                           pagina='laboratorios')

    args = [id, nome, endereco, intervalo_parser, intervalo_arduino]
    if "" not in args:
        controllers.atualizar_informacoes_lab(*args)

    kwargs = {"c" : "Informações atualizadas com sucesso"}
    return redirect(url_for("laboratorio", id=id, nome=nome, **kwargs))

@app.route('/laboratorio/<id>/')
@app.route('/laboratorio/<id>/<nome>')
def laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    laboratorio = controllers.obter_laboratorio(id)
    return render_template('gerenciar.html',
                           laboratorio=laboratorio,
                           lab_id=laboratorio.id,
                           lab_nome=laboratorio.nome,
                           autenticado=autenticado(),
                           admin=admin_autenticado(),
                           pagina='gerenciar')

@app.route('/remover-laboratorio/<id>/', methods=["POST"])
def remover_laboratorio(id):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login'))

    controllers.remover_laboratorio(id)
    kwargs = {"c" : "Laboratório removido com sucesso!"}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/editar-laboratorio/<id>/')
@app.route('/editar-laboratorio/<id>/<nome>')
def editar_laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    laboratorio = controllers.obter_laboratorio(id)

    return render_template('editar_lab.html',
                           lab_id=id,
                           lab_nome=nome,
                           autenticado=autenticado(),
                           admin=admin_autenticado(),
                           pagina='editar_laboratorio',
                           laboratorio=laboratorio)

@app.route('/editar-laboratorio/<id>/', methods=["POST"])
@app.route('/editar-laboratorio/<id>/<nome>', methods=["POST"])
def editar_laboratorio_post(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
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
        kwargs = {"c" : "Dados do laboratório atualizados com sucesso"}
        return redirect(url_for("laboratorio", id=id, nome=nome, **kwargs))
    else:
        kwargs = {"e" : "Por favor, preencha todos os campos"}
        return redirect(url_for('zona_de_conforto', id=id, nome=nome, **kwargs))

@app.route('/zona-de-conforto/<id>/')
@app.route('/zona-de-conforto/<id>/<nome>')
def zona_de_conforto(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    zc = controllers.obter_zona_de_conforto(id)
    return render_template('alterar_zona_conforto.html',
                           lab_id=zc.lab_id,
                           lab_nome=zc.nome_laboratorio,
                           autenticado=autenticado(),
                           admin=admin_autenticado(),
                           pagina='zona_de_conforto',
                           zona_conforto=zc)

@app.route('/zona-de-conforto/<id>/', methods=["POST"])
@app.route('/zona-de-conforto/<id>/<nome>', methods=["POST"])
def zona_de_conforto_post(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    temp_min = request.form.get("temp-min") or ''
    temp_max = request.form.get("temp-max") or ''
    umid_min = request.form.get("umid-min") or ''
    umid_max = request.form.get("umid-max") or ''

    args = [temp_min, temp_max, umid_min, umid_max, id]
    if "" not in args:
        controllers.atualizar_zona_de_conforto(*args)
        kwargs = {"c" : "Zona de Conforto atualizada com sucesso"}
        return redirect(url_for("laboratorio", id=id, nome=nome, **kwargs))
    else:
        kwargs = {"e" : "Por favor, preencha todos os campos"}
        return redirect(url_for('zona_de_conforto', id=id, nome=nome, **kwargs))

@app.route('/usuarios-lab/<id>/')
@app.route('/usuarios-lab/<id>/<nome>')
def usuarios_laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
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
                           autenticado=autenticado(),
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
        kwargs = {"c" : "Laboratório cadastrado com sucesso"}
    else:
        kwargs = {"e" : "Por favor, lembre-se de preencher o nome do laboratório"}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro_usuario_sistema.html',
                           pagina='cadastro',
                           autenticado=autenticado(),
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
            kwargs = {"e": "Login ou e-mail já utilizados"}
            return redirect(url_for("cadastro", **kwargs))
    kwargs = {"c": "Usuário enviado para autorização!"}
    return redirect(url_for('login', **kwargs))


@app.route('/alterar-usuario-sistema/<id>', methods=["GET", "POST"])
def alterar_usuario_sistema(id):
    if not admin_autenticado():
        kwargs = {"e" : "Por favor, faça login como administrador"}
        return redirect(url_for('login'))

    if request.method == 'POST':
        login = request.form.get("login") or ''
        senha = request.form.get("senha") or ''
        nome = request.form.get('nome') or ''
        email = request.form.get('email') or ''
        controllers.editar_usuario_sistema(id, login, senha, nome, email)
        kwargs = {"c":"Usuário alterado com sucesso!"}
        return redirect(url_for('aprovar_usuario', **kwargs))
    else:
        return render_template('alterar_usuario_sistema.html',
                                user = controllers.obter_usuario_sistema(id),
                                autenticado=autenticado(),
                                admin=admin_autenticado(),
                                pagina='aprovar_usuario')

@app.route('/alterar-senha/<user_id>')
def alterar_senha(user_id):
    if not autenticado():
        return redirect(url_for('login'))

    return render_template('alterar_senha.html',
                           pagina='aprovar_usuario',
                           autenticado=autenticado(),
                           admin=admin_autenticado(),
                           user_id=user_id)


@app.route('/alterar-senha/<user_id>', methods=["POST"])
def alterar_senha_post(user_id):
    if not autenticado():
        return redirect(url_for('login'))

    senha_atual        = request.form.get('senha_atual')
    senha_nova         = request.form.get('senha_nova')
    senha_nova_confirm = request.form.get('senha_nova_confirm')

    if (senha_nova != senha_nova_confirm):
        kwargs = {"e" : "Nova senha e confirmação de nova senha não são iguais"}
        return redirect(url_for('alterar_senha', user_id=user_id, **kwargs))

    usuario = controllers.obter_usuario_sistema(user_id)

    try:
        controllers.autenticar(usuario.login, senha_atual)

        if controllers.alterar_senha(usuario.login, senha_nova):
            kwargs = {"c" : "Senha alterada com sucesso"}
            return redirect(url_for('aprovar_usuario', **kwargs))
        else:
            kwargs = {"e" : "Não foi possível alterar a senha. Tente novamente"}
            return redirect(url_for('alterar_senha', user_id=user_id, **kwargs))

    except InformacoesIncorretas:
        kwargs = {"e" : "Senha atual incorreta. Tente novamente"}
        return redirect(url_for('alterar_senha', user_id=user_id, **kwargs))

@app.route('/remover-usuario/<id>/', methods=["POST"])
def remover_usuario_sistema(id):
    if not admin_autenticado():
        kwargs = {"e" : "Por favor, faça login como administrador"}
        return redirect(url_for('login'))

    if id == session["id"]:
        kwargs = {"e" : "Você não pode se remover!"}
    else:
        controllers.remover_usuario_sistema(id)
        kwargs = {"c" : "Usuário removido com sucesso!"}
    return redirect(url_for('aprovar_usuario', **kwargs))

@app.route('/alterar-usuario-lab/<lab_id>/<lab_nome>/<id>', methods=["GET", "POST"])
def alterar_usuario_lab(lab_id, lab_nome, id):
    if not admin_autenticado():
        kwargs = {"e" : "Por favor, faça login como administrador"}
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = request.form.get('id-user') or ''
        nome = request.form.get('nome') or ''
        email = request.form.get('email') or ''
        userToEdit = controllers.obter_usuario_lab(id)
        userToEdit.nome = nome
        userToEdit.email = email
        userToEdit.user_id = user_id
        if (id != user_id):
            userToEdit.editar(old_user_id=id)
        else:
            userToEdit.editar()
        kwargs = {"c":"Usuário alterado com sucesso!"}
        return redirect(url_for('usuarios_laboratorio', id=lab_id, nome=lab_nome, **kwargs))


    else:
        #GET
        return render_template('alterar_usuario_lab.html',
                               lab_id=lab_id,
                               lab_nome=lab_nome,
                               user = controllers.obter_usuario_lab(id),
                               autenticado=autenticado(),
                               admin=admin_autenticado(),
                               pagina='usuarios_laboratorio')

@app.route('/remover-usuario-lab/<lab_id>/<lab_nome>/<id>', methods=["POST"])
def remover_usuario_lab(lab_id, lab_nome, id):
    if not admin_autenticado():
        kwargs = {"e" : "Por favor, faça login como administrador"}
        return redirect(url_for('login'))

    controllers.remover_usuario_lab(lab_id, id)
    kwargs = {"c" : "Usuário removido com sucesso!",
              "id": lab_id,
              "nome": lab_nome}
    return redirect(url_for('usuarios_laboratorio', **kwargs))

@app.route('/aprovar-usuario-lab/<id>', methods=["POST"])
def aprovar_usuario_lab(id):
    if not admin_autenticado():
        return redirect(url_for('laboratorios',
                                {"e": "Autorizaçã negada!"}))

    aprovar = request.form.get('aprovar') == 'true'
    controllers.aprovar_usuario_lab(id, aprovar)
    kwargs = {"c" : "Autorização alterada com sucesso!"}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/adicionar-usuario-lab/<id>/', methods=["POST"])
@app.route('/adicionar-usuario-lab/<id>/<nome>', methods=["POST"])
def adicionar_usuario_lab(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login'))

    user_id = request.form.get('id-user') or ''
    if user_id != "":
        controllers.adicionar_usuario_lab(id, user_id)
        kwargs = {'c': "Usuário associado ao laboratório com sucesso"}
    else:
        kwargs = {'e': "Por favor, escolha um usuário"}

    return redirect(url_for('usuarios_laboratorio', id=id, nome=nome, **kwargs))

@app.route('/cadastro-usuario-lab')
def cadastro_usuario_lab():
    laboratorios = controllers.obter_laboratorios()
    if len(laboratorios) == 0:
        kwargs = {"e" : "Primeiro, cadastre um laboratório"}
        return redirect(url_for("laboratorios", _anchor="cadastrar", **kwargs))

    return render_template('cadastro_usuario_lab.html',
                           pagina='cadastro_usuario_lab',
                           autenticado=autenticado(),
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
        kwargs = {"e": "Id de usuário já existente"}
    else:
        kwargs = {"c": "Usuário cadastrado com sucesso"}

    return redirect(url_for('cadastro_usuario_lab', **kwargs))

@app.route('/remover-equipamento/<lab_id>/<lab_nome>/<id>/', methods=["POST"])
def remover_equipamento(lab_id, lab_nome, id):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login'))

    controllers.remover_equipamento(id)
    kwargs = {"c": "Equipamento removido com sucesso!",
              "id": lab_id,
              "nome": lab_nome}
    return redirect(url_for('equipamentos_laboratorio', **kwargs))


@app.route('/alterar-equipamento/<lab_id>/<lab_nome>/<id>', methods=["GET", "POST"])
def alterar_equipamento(lab_id, lab_nome, id):
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    if request.method == 'POST':
        #create new Equipment, save changes to BD
        temp_min = request.form.get('temp-min')
        temp_max = request.form.get('temp-max')
        MAC = request.form.get('endereco-mac')
        nome_equip = request.form.get('nome')
        descricao = request.form.get('descricao')
        parent_id = request.form.get('parent_id')
        controllers.atualizar_equipamento(lab_id, nome_equip, descricao, temp_min, temp_max, MAC, parent_id, id)
        kwargs = {"c":"Equipamento alterado com sucesso!"}
        return redirect(url_for('equipamentos_laboratorio', id=lab_id, nome=lab_nome, **kwargs))
    else:
        #GET
        equips = controllers.obter_equipamentos(lab_id)
        lista_arduinos = controllers.listar_arduinos_laboratorio(lab_id)
        return render_template('alterar_equipamento.html',
                               lab_id=lab_id,
                               lab_nome=lab_nome,
                               equip=controllers.obter_equipamento(id),
                               lista_arduinos=lista_arduinos,
                               equipamentos=equips+lista_arduinos,
                               autenticado=autenticado(),
                               admin=admin_autenticado(),
                               pagina='equipamentos_laboratorio')

@app.route('/cadastro-equipamento/<id>/<nome>', methods=["POST"])
def cadastro_equipamento(id, nome):
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    temp_min = request.form.get('temp-min')
    temp_max = request.form.get('temp-max')
    MAC = request.form.get('endereco-mac')
    nome_equip = request.form.get('nome')
    descricao = request.form.get('descricao')
    parent_id = request.form.get('parent_id')

    args = [id, nome_equip, descricao, temp_min, temp_max, MAC, parent_id]
    kwargs = {"id": id,
              "nome": nome}
    if "" not in args:
        controllers.cadastro_equipamento(*args)
        kwargs["c"] = "Equipamento cadastrado com sucesso"
    else:
        kwargs["e"] = "Por favor preencha todos os campos"
        kwargs["_anchor"] = "cadastrar"
    return redirect(url_for('equipamentos_laboratorio', **kwargs))

@app.route('/log-eventos/<id>/<nome>/')
def log_eventos_hoje(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

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
                           autenticado=autenticado(),
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
                           autenticado=True,
                           admin=True,
                           usuarios=usuarios)

@app.route('/aprovar-usuario/<id>', methods=["POST"])
def aprovar_usuario_post(id):
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    aprovar = request.form.get('aprovar') == 'true'
    controllers.aprovar_usuario(id, aprovar)

    if aprovar:
        kwargs = {"c": "Usuário autorizado com sucesso"}
    else:
        kwargs = {"c": "Autorização do usuário removida com sucesso"}

    return redirect(url_for('laboratorios', **kwargs))

@app.route('/editar-status-admin/<id>', methods=["POST"])
def editar_status_administrador(id):
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    aprovar = request.form.get('aprovar') == 'true'
    controllers.editar_status_administrador(id, aprovar)

    kwargs = {"c": "Status de administrador alterado com sucesso"}
    return redirect(url_for('laboratorios', **kwargs))

@app.route('/equipamentos-lab/<id>/')
@app.route('/equipamentos-lab/<id>/<nome>')
def equipamentos_laboratorio(id, nome=""):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    equipamentos = controllers.obter_equipamentos(id)
    lista_arduinos = controllers.listar_arduinos_laboratorio(id)

    return render_template('lista_equipamentos.html',
                           autenticado=autenticado(),
                           admin   = admin_autenticado(),
                           lab_id  = id,
                           lab_nome= nome,
                           equipamentos=equipamentos+lista_arduinos,
                           lista_arduinos=lista_arduinos,
                           pagina  = "equipamentos_laboratorio")

@app.route('/status-sistema/<id>/<nome>')
def system_status(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    # pegar as infos do banco
    lab_id = id
    timestamp_parser = int(controllers.ultima_atualizacao_parser())
    tempos_arduinos  = controllers.ultima_atualizacao_arduino(lab_id)

    agora = datetime.today()
    status_componente = "OK"
    dados = []

    mydenox = controllers.ultima_atualizacao_mydenox()
    if mydenox is not None:
        dados += [{"nome_componente":    "MyDenox",
                   "ultima_atualizacao": mydenox.ultima_atualizacao,
                   "status":             mydenox.status}]
    else:
        dados += [{"nome_componente":    "MyDenox",
                   "ultima_atualizacao": None,
                   "status":             "Nenhuma mensagem recebida"}]


    # parsear as infos e preencher o dicionario com os dados
    if ((datetime.fromtimestamp(timestamp_parser)) <
        (agora - timedelta(minutes=(2*controllers.obter_intervalo_parser())))):
        status_componente = "Fora do Ar"

    dados += [{"nome_componente"    : "Parser",
               "ultima_atualizacao" : timestamp_parser,
               "status"             : status_componente}]

    if tempos_arduinos is not None:
        status_componente = "OK"
        if ((datetime.fromtimestamp(int(tempos_arduinos)) <
            (agora - timedelta(minutes=(2*controllers.obter_intervalo_arduino(id)))))):
            status_componente = "Fora do Ar"

        dados += [{"nome_componente"    : "Arduino",
                   "ultima_atualizacao" : int(tempos_arduinos),
                   "status"             : status_componente}]

    return render_template('system-status.html',
                           lab_id = lab_id,
                           lab_nome = nome,
                           componentes = dados,
                           admin = admin_autenticado(),
                           pagina = 'system-status',
                           autenticado=autenticado())

@app.route('/robots.txt')
def robots_txt():
    return """User-Agent: *<br>\nDisallow: /"""

@app.route('/mostrar-grafico/<id>/<nome>')
def mostrar_grafico(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    equipamentos = controllers.obter_equipamentos(id)

    return render_template('grafico.html',
                            lab_id=id,
                            lab_nome=nome,
                            autenticado=True,
                            admin = admin_autenticado(),
                            equipamentos=equipamentos,
                            pagina='mostrar_grafico')

@app.route('/mostrar-grafico/<id>/<nome>', methods=["POST"])
def mostrar_grafico_post(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    chart_type = request.form.get("chart_type") or ''
    chart_target = request.form.get("target")
    date = request.form.get("daterange") or ''
    dates = date.split('-');
    intervalo_grafico = request.form.get("intervalo_grafico") or 60 #em min

    start_date_epoch = int(datetime.strptime(dates[0], "%d/%m/%Y %H:%M:%S ").timestamp())
    end_date_epoch = int(datetime.strptime(dates[1], " %d/%m/%Y %H:%M:%S").timestamp())

    interval = int(intervalo_grafico)*60

    args = [id]
    equipamentos = controllers.obter_equipamentos(*args)

    data = []

    args = [chart_type, chart_target, start_date_epoch, end_date_epoch, id]
    data = controllers.get_data_log(*args)

    chart_type_dict = {"temperatura": "Temperatura",
                        "umidade": "Umidade"}

    chart_title = chart_type_dict[chart_type] + (" do equipamento" if chart_target != "laboratorio" else "")
    
    if data == []:
        kwargs = {"e" : "Não existem dados para o período selecionado. Por favor, selecione outro período",
                  "id" : id,
                  "nome" : nome}
        return redirect(url_for('mostrar_grafico', **kwargs))

    data = json.dumps(data)
    array_of_epochs = json.loads(data)

    result = []

    try:
        result = get_interval_means(interval, array_of_epochs, start_date_epoch, end_date_epoch)
    except:
        kwargs = {"e" : "Intervalo de datas muito curto! Um período maior que 2 horas",
                  "id" : id,
                  "nome" : nome}
        return redirect(url_for('mostrar_grafico', **kwargs))

    return render_template('grafico.html',
                            pagina='mostrar_grafico',
                            autenticado=True,
                            lab_id=id,
                            chart_title=chart_title,
                            lab_nome=nome,
                            data=result,
                            equipamentos=equipamentos,
                            admin = admin_autenticado(),
                            intervalo_grafico=intervalo_grafico)


@app.route('/mostrar-relatorio/<id>/<nome>')
def mostrar_relatorio(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    return render_template('relatorio.html',
                            pagina="mostrar_relatorio",
                            autenticado=True,
                            admin = admin_autenticado(),
                            lab_id=id,
                            lab_nome=nome)

@app.route('/mostrar-relatorio/<id>/<nome>', methods=["POST"])
def mostrar_relatorio_post(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    date = request.form.get("daterange") or ''
    dates = date.split('-');

    start_date_epoch = int(datetime.strptime(dates[0], "%d/%m/%Y %H:%M:%S ").timestamp())
    end_date_epoch = int(datetime.strptime(dates[1], " %d/%m/%Y %H:%M:%S").timestamp())

    # tabela para log de temperatura e umidade
    args = [start_date_epoch, end_date_epoch, id]
    lab_temp_umid = [[int(v[0]), int(v[1]), int(v[2])] for v in controllers.obter_dados_entre_tempos(*args)]

    # tabela de log de temperatura para equipamentos
    equipamentos = controllers.obter_ids_equipamentos(id)
    equip_dict ={}
    for equipamento in equipamentos:
        args = [start_date_epoch, end_date_epoch, equipamento]
        equip_temp_umid = controllers.obter_dados_entre_tempos_equip(*args)
        equip_dict[equipamento] = [[int(v[0]), int(v[1])] for v in equip_temp_umid]

    nome_equips = controllers.obter_nome_equipamentos(id)

    # tabela para log de presença
    args = [start_date_epoch, end_date_epoch, id]
    log_presenca_lista = controllers.log_usuario(*args)

    # tabela para usuários presentes
    presentes_list = controllers.usuarios_presentes(id)

    kwargs = {
              "lab_id": id,
              "lab_nome": nome,
              "path": join(getcwd(), "issues_monitoring"),
              "usuarios_presentes": presentes_list,
              "eventos": log_presenca_lista,
              "nome_equips": nome_equips,
              "condicoes_ambiente_equip": equip_dict,
              "condicoes_ambiente_lab": lab_temp_umid}
    page = render_template('relatorio_template.html',
                           **kwargs)

    css = './issues_monitoring/static/css/table.css'
    name = random_string(20)
    kwargs["nome_pdf"] = name
    pdf_path = './issues_monitoring/reports/{}.pdf'.format(name)
    pdf_report = HeadlessPDFKit(page,
                                'string',
                                css=css,
                                cover_first=False).to_pdf(pdf_path)
    return render_template('relatorio.html',
                           **kwargs)

@app.route('/anomalias/<id>/<nome>/')
def anomalias_hoje(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    _hoje = datetime.fromtimestamp(hoje()).strftime("%d-%m-%Y")
    return redirect(url_for('anomalias',
                            id=id,
                            nome=nome,
                            dia=_hoje))

@app.route('/anomalias/<id>/<nome>/<dia>')
def anomalias(id, nome, dia):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    dia = int(datetime.strptime(dia, "%d-%m-%Y").timestamp())
    anomalias = controllers.obter_anomalias(id)
    anomalias_resolvidas = controllers.obter_anomalias_resolvidas_dia(id, dia)

    proximo_dia = controllers.data_proxima_anomalia_resolvida(id, dia)
    dia_anterior = controllers.data_anomalia_resolvida_anterior(id, dia)

    return render_template('anomalias.html',
                           anomalias=anomalias,
                           anomalias_resolvidas=anomalias_resolvidas,
                           proximo_dia=proximo_dia,
                           dia_anterior=dia_anterior,
                           dia=dia,
                           pagina='anomalias',
                           autenticado=True,
                           admin=admin_autenticado(),
                           lab_id=id,
                           lab_nome=nome)

@app.route('/solucionar-anomalia/<lab_id>/<lab_nome>/<id>')
def solucionar_anomalia(lab_id, lab_nome, id):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    anomalia = controllers.obter_anomalia(id)
    return render_template('solucionar_anomalia.html',
                           lab_id=lab_id,
                           lab_nome=lab_nome,
                           autenticado=True,
                           admin = admin_autenticado(),
                           anomalia=anomalia)

@app.route('/acao/<id>/<nome>', methods=["POST"])
def acao(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    tipo_anomalia = request.form.get("tipo_anomalia") or ''
    id_anomalia = request.form.get("id_anomalia") or ''
    user_id = session.get("id")
    descricao_acao = request.form.get("descricao") or ""
    args = [id_anomalia, descricao_acao, user_id]
    if "" not in args:
        controllers.resolver_anomalia(*args)
        controllers.enviar_email_acao_realizada(id,
                                                descricao_acao,
                                                tipo_anomalia,
                                                user_id)

    return redirect(url_for('anomalias_hoje',
                            id=id,
                            nome=nome))


@app.route('/relatorio/<nome>.pdf')
def relatorio_pdf(nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    path = join('issues_monitoring', 'reports', '{}.pdf'.format(nome))
    def stream():
        with open(path, 'rb') as f:
            while True:
                piece = f.read(1024)
                if not piece:
                    break
                yield piece


    header = Headers()
    header.add('Content-Disposition', 'inline', filename="Relatorio.pdf")
    header.add('Content-Type', 'application/pdf; charset=utf-8')
    header.add('Content-Length', '{}'.format(stat(path).st_size))
    return Response(stream(),
                    headers=header)
