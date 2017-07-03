from datetime import datetime
from ..common.mail import send_email
from ..models import UsuarioSistema, UsuarioLab, AdministradorSistema

def autenticar(usuario, senha):
    return UsuarioSistema.autenticar(usuario, senha)

def alterar_senha(usuario, senha):
    return UsuarioSistema.alterar_senha(usuario, senha)

def obter_usuarios_sistema():
    return UsuarioSistema.obter_informacoes()

def obter_usuario_sistema(user_id):
    return UsuarioSistema.obter(user_id)

def editar_usuario_sistema(user_id, login, senha, nome, email):
    usuario = UsuarioSistema(login, senha, email, nome, user_id)
    usuario.editar()

def remover_usuario_sistema(user_id):
    UsuarioSistema.remover(user_id)

def editar_status_administrador(user_id, admin):
    AdministradorSistema.editar_status_administrador(user_id, admin)

def aprovar_usuario(user_id, aprovar):
    AdministradorSistema.aprovar_usuario(user_id, aprovar)

def enviar_emails_cadastro_usuario():
    admins = AdministradorSistema.obter_administradores()

    emails = [a.email for a in admins]

    msg_content = """
Caro responsável,
Você está recebendo essa mensagem pois um novo usuário foi cadastrado no banco de dados do sistema ISSUES Monitoring.
Para continuar o processo de cadastro do novo usuário, por favor entre no site do sistema com seu nome de usuário e senha e autorize o cadastro.
\n\nAtenciosamente, \nEquipe ISSUES Monitoring"""

    send_email("Alerta de cadastro de novo usuário",
               msg_content,
               emails)

def cadastro_usuario_sistema(login, senha, email, nome):
    if not UsuarioSistema.existe(login, email):
        usuario = UsuarioSistema(login, senha, email, nome)
        usuario.cadastrar()
        enviar_emails_cadastro_usuario()
        return True
    else:
        return False

def aprovar_usuario_lab(user_id, aprovar):
    AdministradorSistema.autorizar_usuario_lab(user_id, aprovar)

def obter_usuario_lab(user_id):
    return UsuarioLab.obter(user_id)

def obter_usuarios_laboratorio(id):
    return UsuarioLab.obter_do_laboratorio(id)

def obter_usuarios_laboratorios():
    return UsuarioLab.obter_todos()

def cadastro_usuario_lab(lab_id, user_id, nome, email):
    if not UsuarioLab.existe(user_id):
        usuario = UsuarioLab(user_id,
                             nome,
                             email,
                             lab_id=lab_id)
        usuario.cadastrar()
        return True
    else:
        return False

def editar_usuario_lab(user_id, nome, email):
    usuario = UsuarioLab(user_id, nome, email)
    usuario.editar()

def usuarios_presentes(lab_id):
    return UsuarioLab.presentes(lab_id)

def remover_usuario_lab(id_lab, user_id):
    UsuarioLab.remover(id_lab, user_id)

def log_eventos(lab_id, dia):
    return UsuarioLab.eventos(lab_id, dia)

def data_proximo_evento_mydenox(lab_id, dia):
    return UsuarioLab.data_proximo_evento(lab_id, dia)

def data_evento_anterior_mydenox(lab_id, dia):
    return UsuarioLab.data_evento_anterior(lab_id, dia)

def log_usuario(hoje, amanha, lab_id):
    return UsuarioLab.obter_dado_presenca(hoje, amanha, lab_id)

def adicionar_usuario_lab(lab_id, user_id):
    UsuarioLab.adicionar_ao_laboratorio(lab_id, user_id)
