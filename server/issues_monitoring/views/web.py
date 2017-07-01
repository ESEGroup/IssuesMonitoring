from flask          import render_template, request, redirect, url_for, session
from flask          import send_file, current_app as app
from datetime       import datetime, timedelta
from ..common.erros import NaoAutorizado, InformacoesIncorretas
from ..common.utils import autenticado, admin_autenticado, hoje, agora
from ..             import app, Config, controllers
from ..models       import UsuarioLab, UsuarioSistema, Equipamento
import json
import pdfkit

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

    return render_template('alterar_usuario_lab.html',
                           lab_id=lab_id,
                           lab_nome=lab_nome,
                           user = UsuarioLab.obter(id),
                           autenticado=autenticado(),
                           admin=admin_autenticado(),
                           pagina='alterar_usuario_lab'
                           )   

# @app.route('/alterar-usuario-lab/<lab_id>/<lab_nome>/<id>', methods=["POST"])
# def alterar_usuario_lab(lab_id, lab_nome, id):
#     if not admin_autenticado():
#         kwargs = {"e" : "Por favor, faça login como administrador"}
#         return redirect(url_for('login'))

#     #controllers.remover_usuario_lab(lab_id, id)
#     kwargs = {"c" : "Usuário selecionado p/ edição com sucesso!",
#               "id": lab_id,
#               "nome": lab_nome}
#     return redirect(url_for('usuarios_laboratorio', **kwargs))

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
        return redirect(url_for('usuarios_laboratorio'))

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

# @app.route('/escolher-grafico/')
# def escolher_grafico(id):
#     json.dumps(temp_data)
#     return render_template('grafico.html',
#                             lab_id=id,
#                             pagina='grafico')

@app.route('/mostrar-grafico/<id>/<nome>')
def mostrar_grafico(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    equipamentos = controllers.obter_ids_equipamentos(id)

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
    chart_target = request.form.get("equipamento") or 'laboratorio'
    date = request.form.get("daterange") or ''
    dates = date.split('-');
    intervalo_grafico = request.form.get("intervalo_grafico") or 60 #em min

    start_date_epoch = int(datetime.strptime(dates[0], "%d/%m/%Y %H:%M:%S ").timestamp())
    end_date_epoch = int(datetime.strptime(dates[1], " %d/%m/%Y %H:%M:%S").timestamp())

    # dia = int(datetime.strptime(dia, "%d-%m-%Y").timestamp())

    interval = int(intervalo_grafico)*60

    args = [id]
    equipamentos = controllers.obter_ids_equipamentos(*args)

    temp_data = []

    if (chart_type == "temperatura"):
        if (chart_target == "laboratorio"):
            args = [chart_type, start_date_epoch, end_date_epoch, id]
            temp_data = controllers.get_data_log(*args)
        else:
            args = [chart_type, chart_target, start_date_epoch, end_date_epoch, id]
            temp_data = controllers.get_equip_log(*args)
    elif (chart_type == "umidade"):
        args = [chart_type, start_date_epoch, end_date_epoch, id]
        temp_data = controllers.get_data_log(*args)

    if temp_data == []:
        kwargs = {"error_message": "Selecione tipo do gráfico!"}
        return render_template('grafico.html',
                               lab_id=id,
                               lab_nome=nome,
                               admin = admin_autenticado(),
                               autenticado=True,
                               equipamentos=equipamentos,
                               pagina='mostrar_grafico',
                               **kwargs)

    json.dumps(temp_data)
    arrayOfEpochs = json.loads(temp_data)
    print ("Array of Epochs: ", arrayOfEpochs)

    if (arrayOfEpochs == []):
        kwargs = {"error_message": "Não existem dados para o período selecionado. Por favor, selecione outro período"}
        return render_template('grafico.html',
                               lab_id=id,
                               lab_nome=nome,
                               admin = admin_autenticado(),
                               autenticado=True,
                               equipamentos=equipamentos,
                               pagina='mostrar_grafico',
                               **kwargs)

    print("Array of Epochs: {}".format(arrayOfEpochs))

    result_means = []

    result_means = getIntervalMeans(interval, arrayOfEpochs, start_date_epoch, end_date_epoch)

    print("result means: ", result_means)
    return render_template('grafico.html',
                            pagina='mostrar_grafico',
                            autenticado=True,
                            lab_id=id,
                            lab_nome=nome,
                            temp_data=result_means,
                            equipamentos=equipamentos,
                            admin = admin_autenticado(),
                            intervalo_grafico=intervalo_grafico)


#array of epochs has format = [[epoch1, value1], [epoch2, value2],...]
def getIntervalMeans(interval, arrayOfEpochs, epochBeginning, epochEnding):
    #exceptions handling
    if(interval > 7200):
      print("Error: Interval bigger than 2h")
      return [[]]
    elif(len(arrayOfEpochs)<1):
      print ("Error: entry array is null")
      return [[]]

    beginningOfInterval = epochBeginning
    endOfInterval = epochEnding
    sum = 0.0

    meansArray = []
    numberOfValuesInInterval = 0
    intervalIndex = 0
    intervalLimit = interval
    minimumValue = arrayOfEpochs[0][1]
    maximumValue = arrayOfEpochs[0][1]
    #varrer o array calculando a média de cada intervalo
    for i in range(len(arrayOfEpochs)):
        print(arrayOfEpochs[i][0])
        if(arrayOfEpochs[i][0] < beginningOfInterval+intervalLimit):
            print("Adding {} to current sum".format(arrayOfEpochs[i][1]))
            sum+=arrayOfEpochs[i][1]
            minimumValue = min(minimumValue, arrayOfEpochs[i][1])
            maximumValue = max(maximumValue, arrayOfEpochs[i][1])
            numberOfValuesInInterval+=1
        else:
            #surpassed last interval limit, move onward to next limit
            if numberOfValuesInInterval != 0:
                mean = sum/numberOfValuesInInterval
                print("Surpassed current interval limit, adding {} to index {}\n".format(mean, intervalIndex))
                meansArray+=[[intervalIndex, mean, minimumValue, maximumValue]]
                sum=arrayOfEpochs[i][1]
                minimumValue = arrayOfEpochs[i][1]
                maximumValue = arrayOfEpochs[i][1]
                numberOfValuesInInterval=1
                intervalIndex+=1
                intervalLimit+=interval
    #if it leaves the for without even achieving the first interval, or if there is a remainder:
    #add the last value, the remainder
    if numberOfValuesInInterval != 0:
        meansArray+=[[intervalIndex, sum/numberOfValuesInInterval, minimumValue, maximumValue]]

    print (meansArray)
    return meansArray

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

    # dia = datetime.fromtimestamp(hoje()).strftime("%d-%m-%Y")
    # dia = int(datetime.strptime(dia, "%d-%m-%Y").timestamp())

    date = request.form.get("daterange") or ''
    dates = date.split('-');

    start_date_epoch = int(datetime.strptime(dates[0], "%d/%m/%Y %H:%M:%S ").timestamp())
    end_date_epoch = int(datetime.strptime(dates[1], " %d/%m/%Y %H:%M:%S").timestamp())

    # dateTomorrow = dia+24*60*60. -1.
    # args = [start_date_epoch, end_date_epoch, id]
    # temp_data = controllers.log_usuario(*args)
    # presenceList = []
    # if(len(temp_data)>0):
    #     presenceList = organizePresenceList(dia, temp_data)

    #     for i in presenceList:
    #         i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[1]))
    #         i[2] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[2]))


    # tabela para log de temperatura e umidade
    args = [start_date_epoch, end_date_epoch, id]
    lab_table = controllers.get_lab_log(*args)
    json.dumps(lab_table)
    lab_temp_umid = json.loads(lab_table)
    print("lab temp e umid: ", lab_temp_umid)

    # tabela de log de temperatura para equipamentos
    equipamentos = controllers.obter_ids_equipamentos(id)
    equip_dict ={}
    for equipamento in equipamentos:
        args = ["temperatura", equipamento, start_date_epoch, end_date_epoch, id]
        equip_table = controllers.get_equip_log(*args)
        json.dumps(equip_table)
        equip_temp_umid = json.loads(equip_table)
        equip_dict[equipamento] = equip_temp_umid
    print (equip_dict)
    # tabela para log de presença
    args = [start_date_epoch, end_date_epoch, id]
    log_presenca_lista = controllers.log_usuario(*args)
    print ("log presenca: ", log_presenca_lista)

    # tabela para usuários presentes
    presentes_list = controllers.usuarios_presentes(id)
    print ("presentes: ", presentes_list)

    page = render_template('relatorio.html',
                            lab_id=id,
                            lab_nome=nome,
                            autenticado=True,
                            admin = admin_autenticado(),
                            pagina='mostrar_relatorio',
                            usuarios_presentes=presentes_list,
                            eventos=log_presenca_lista,
                            condicoes_ambiente_equip=equip_dict,
                            condicoes_ambiente_lab=lab_temp_umid)

    css = './issues_monitoring/static/css/table.css'
    pdf_report = pdfkit.from_string(page, './issues_monitoring/reports/out.pdf', css=css)

    # return send_file('reports/out.pdf', as_attachment = False)
    # webbrowser.open_new_tab('./issues_monitoring/reports/out.pdf')

    return page


#presence: comes in the form of [[name, date, event], ...], event = IN/OUT
def organizePresenceList(currentDayEpoch, presence):
    presenceList = []
    currentIndex = 0
    currentlyPresent = False
    timeUserArrived = 0
    currentName = presence[0].nome#gets currentName
    while(currentIndex < len(presence)):
        # we're still talking about the same person
        if(currentName==presence[currentIndex].nome):
            #if the user just got in, save the time it got in
            if(currentlyPresent == False and presence[currentIndex].evento=="IN"):
                currentlyPresent = True
                timeUserArrived= presence[currentIndex].data_evento

            #OR, if the user was present but just got out, save in list that IN-OUT cycle
            elif(currentlyPresent == True and presence[currentIndex].evento=="OUT"):
                currentlyPresent = False
                presenceList+= [[presence[currentIndex].nome, timeUserArrived,presence[currentIndex].data_evento]]


            #else, it's just a repetition of IN or OUT, so ignore
            #jump to next entry on list
            currentIndex+=1

        #the person we are talking about is now another one
        else:
            #before moving on, check if last person on list got out; if they didn't, they forgot to punch out, so we need to...
            #say that they punched out at the end of the day
            if currentlyPresent:
                currentlyPresent = False
                #write their last IN-OUT cycle
                presenceList+= [[currentName, timeUserArrived,currentDayEpoch + 86399]]#TODO: maybe this needs to be epoch from end of that day?
            currentName = presence[currentIndex].nome

    #EXCEPTION: In case the last user only got in and didn't punch out, we need to make sure we get their last IN-OUT cycle
    if currentlyPresent:
        currentlyPresent = False
        #write their last IN-OUT cycle
        presenceList+= [[currentName, timeUserArrived,currentDayEpoch + 86399]]#TODO: maybe this needs to be epoch from end of that day?

    return presenceList

@app.route('/anomalias/<id>/<nome>')
def anomalias(id, nome):
    if not autenticado():
        kwargs = {"e" : "Por favor, faça o login"}
        return redirect(url_for('login', **kwargs))

    anomalias = controllers.obter_anomalias(id)

    return render_template('anomalias.html',
                            anomalias=anomalias,
                            pagina='anomalias',
                            autenticado=True,
                            admin = admin_autenticado(),
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

    return redirect(url_for('anomalias',
                            id=id,
                            nome=nome))
