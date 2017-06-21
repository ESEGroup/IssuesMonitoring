from flask import render_template, request, redirect, url_for, session
from datetime import datetime
import time
from datetime import datetime, timedelta
from ..common.utils import autenticado, admin_autenticado, hoje, agora
from .. import app, Config, controllers
from ..models import Laboratorio
import json

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
        return redirect(url_for('login'))

    (session['id'],
     session['admin']) = controllers.autenticar(usuario, senha)

    if session['id'] is not None:
        now = int(datetime.now().timestamp())
        session['expiration'] = now + Config.session_duration
        kwargs = {}
    else:
        session.clear()
        kwargs = {"e": "Usuário ou senha incorretos ou usuário não autorizado."}
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
                           autenticado=autenticado(),
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
                           autenticado=autenticado(),
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
                           autenticado=autenticado(),
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
        kwargs = {"c" : "Laboratório cadastrado com sucesso."}
    else:
        kwargs = {"e" : "Por favor, lembre-se de preencher o nome do laboratório."}
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
            kwargs = {"e": "Login ou e-mail já utilizados."}
            return redirect(url_for("cadastro", **kwargs))
    kwargs = {"c": "Usuário enviado para autorização!"}
    return redirect(url_for('login', **kwargs))

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
                           autenticado=autenticado(),
                           admin=True,
                           usuarios=usuarios)

@app.route('/aprovar-usuario/<id>', methods=["POST"])
def aprovar_usuario_post(id):
    if not admin_autenticado():
        return redirect(url_for('laboratorios'))

    aprovar = request.form.get('aprovar') == 'true'
    controllers.aprovar_usuario(id, aprovar)

    if aprovar:
        kwargs = {"c": "Usuário autorizado com sucesso."}
    else:
        kwargs = {"c": "Autorização do usuário removida com sucesso."}

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
                           autenticado=autenticado(),
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
        #print(tempos_arduinos[lab_id])
        if ((datetime.fromtimestamp(int(tempos_arduinos[lab_id]))) <
            (agora - timedelta(minutes=Laboratorio.obter_intervalo_arduino(lab_id)))):
            #print ("ENTROU")
            status_componente = "Fora do Ar"

        dados += [{"nome_componente"    : "Arduino - Lab " + str(lab_id),
                   "ultima_atualizacao" : int(tempos_arduinos[lab_id]),
                   "status"             : status_componente}]

    return render_template('system-status.html',
                            componentes = dados,
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

@app.route('/mostrar-grafico/<id>/')
def mostrar_grafico(id):
    return render_template('grafico.html',
                            lab_id=id,
                            pagina='mostrar_grafico')

@app.route('/mostrar-grafico/<id>/', methods=["POST"])
def mostrar_grafico_post(id):
    temperatura = request.form.get("temperatura") or ''
    umidade = request.form.get("umidade") or ''
    intervalo_grafico = request.form.get("intervalo_grafico") or 60 #em min
    dia = datetime.fromtimestamp(hoje()).strftime("%d-%m-%Y")
    dia = int(datetime.strptime(dia, "%d-%m-%Y").timestamp())
    # dia = 1497668400
    cols = [0, 0]

    interval = int(intervalo_grafico)*60
    # interval = 8000
    args = [temperatura, umidade, dia, id]
    print (args)
    temp_data = controllers.get_data_log(*args)
    json.dumps(temp_data)
    arrayOfEpochs = json.loads(temp_data)

    if (arrayOfEpochs == []):
        print ("Deu ruim!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        kwargs = {"error_message": "Não existem dados para o período selecionado. Por favor, selecione outro período"}
        return render_template('grafico.html',
                               lab_id=id,
                               pagina='mostrar_grafico',
                               **kwargs)

    print("Array of Epochs: {}".format(arrayOfEpochs))
    if (temperatura == "on"):
        cols[0] = 1

    if (umidade == "on"):
        cols[1] = 1

    result_means = []

    if (temperatura == "on" and umidade == "on"):
        result_means = getTemperatureAndHumidityMeans(interval, arrayOfEpochs)
    elif (temperatura == "on"):
        result_means = getIntervalMeans(interval, arrayOfEpochs)
    elif (umidade == "on"):
        result_means = getIntervalMeans(interval, arrayOfEpochs)

    return render_template('grafico.html',
                            lab_id=id,
                            pagina='mostrar_grafico',
                            temp_data=result_means,
                            cols=cols,
                            intervalo_grafico=intervalo_grafico)


def getIntervalMeans(interval, arrayOfEpochs):
    temp = arrayOfEpochs[0][0]
    for i in range(len(arrayOfEpochs)):
        arrayOfEpochs[i][0] -= temp

    if(len(arrayOfEpochs)<1):
        return #invalid entry

    numberOfIntervals = int((86400)/interval)
    print("Number of intervals is: %i" %numberOfIntervals)
    intervalIndex = 0
    #will save the interval means like [[interval1, mean1], [interval2, mean2],...]
    intervalMeans = []

    #do the first exception(00:00), gets means from 00:00 till interval/2
    mean = 0.0
    counter = 0
    numberOfSamples = 0
    currentEpoch = 0
    while(currentEpoch < interval/2):
        currentEpoch = float(arrayOfEpochs[counter][0])
        print ("Current epoch = %f" %currentEpoch)
        if(currentEpoch<interval/2):
            print("Added to first mean")
            #Then save this value on the current mean calculation
            mean+= arrayOfEpochs[counter][1]
            counter = counter + 1
            numberOfSamples +=1
        #repeats until currentEpoch gets an epoch that surpasses interval/2
    if (numberOfSamples>0):
        mean = mean/numberOfSamples
        intervalMeans += [[intervalIndex, mean]]
        intervalIndex+=1
    #now for the rest of the intervals(except the last one)
    for i in range (intervalIndex, numberOfIntervals):
        mean = 0.0
        numberOfSamples = 0.
        while(currentEpoch < i*interval + interval/2 and counter < len(arrayOfEpochs)):
            print ("Current epoch = %f" %currentEpoch)
            currentEpoch = float(arrayOfEpochs[counter][0])
            if(currentEpoch<i*interval + interval/2):
                print ("Added to mean %i" %i)
                #Then save this value on the current mean calculation
                mean+= arrayOfEpochs[counter][1]
                counter = counter + 1
                numberOfSamples +=1.
        if (numberOfSamples>0):
            mean = mean/numberOfSamples
            intervalMeans += [[intervalIndex, mean]]
            intervalIndex+=1

    i+=1
    mean = 0.0
    numberOfSamples = 0
    #now for the final one, the right extreme
    #while it doesn't overflow to the following day...
    while(currentEpoch < interval*numberOfIntervals and counter < len(arrayOfEpochs)):
        currentEpoch = float(arrayOfEpochs[counter][0])
        print ("Current epoch = %f" %currentEpoch)
        if(currentEpoch < 86400):
            print ("Added to mean %i" %i)
            mean+= arrayOfEpochs[counter][1]
            counter = counter + 1
            numberOfSamples +=1
        #repeats until currentEpoch gets an epoch that surpasses the day's seconds limit
    if (numberOfSamples>0):
        mean = mean/numberOfSamples
        intervalMeans += [[intervalIndex, mean]]
    return intervalMeans

def getTemperatureAndHumidityMeans(interval, arrayOfTempAndHumidEpochs):
    arrayOfTempEpochs = []
    arrayOfHumidEpochs = []

    for i in range( len(arrayOfTempAndHumidEpochs)):
        arrayOfTempEpochs+= [[arrayOfTempAndHumidEpochs[i][0],arrayOfTempAndHumidEpochs[i][1]]]
        arrayOfHumidEpochs+= [[arrayOfTempAndHumidEpochs[i][0],arrayOfTempAndHumidEpochs[i][2]]]

    print ("Array Temp: {}".format(arrayOfTempEpochs))
    print ("Array Humid: {}".format(arrayOfHumidEpochs))
    tempMeans = getIntervalMeans(interval, arrayOfTempEpochs)
    HumidMeans = getIntervalMeans(interval, arrayOfHumidEpochs)

    #will have a structure of [[interval1, tempMean1, humidMean1], [interval2, tempMean2, humidMean2], ...]
    tempAndHumidMeans = []
    #assuming they have the same number of intervals:
    for i in range(len(tempMeans)):
        #gets [intervalI, tempMeanI, humidMeanI]
        tempAndHumidMeans +=[[tempMeans[i][0], tempMeans[i][1], HumidMeans[i][1]]]

    return tempAndHumidMeans

@app.route('/mostrar-relatorio/<id>/')
def mostrar_relatorio(id):
    return render_template('relatorio.html',
                            lab_id=id)

@app.route('/mostrar-relatorio/<id>/', methods=["POST"])
def mostrar_relatorio_post(id):
    dia = datetime.fromtimestamp(hoje()).strftime("%d-%m-%Y")
    dia = int(datetime.strptime(dia, "%d-%m-%Y").timestamp())
    # dia = 1497668400

    dateTomorrow = dia+24*60*60. -1.
    args = [dia, dateTomorrow, id]
    temp_data = controllers.log_usuario(*args)
    presenceList = []
    if(len(temp_data)>0):
        presenceList = organizePresenceList(dia, temp_data)

        for i in presenceList:
            i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[1]))
            i[2] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i[2]))

    intervalo_relatorio = request.form.get("intervalo_relatorio") or 60 #em min

    interval = int(intervalo_relatorio)*60
    interval = 8000

    args = ["on", "on", dia, id]
    chart_data = controllers.get_data_log(*args)
    json.dumps(chart_data)
    arrayOfEpochs = json.loads(chart_data)
    result_means = []
    if (len(arrayOfEpochs)>0):
        result_means = getTemperatureAndHumidityMeans(interval, arrayOfEpochs)

    return render_template('relatorio.html',
                            lab_id=id,
                            pagina='mostrar_relatorio',
                            log_presenca=presenceList,
                            condicoes_ambiente=result_means)



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
