class Evento:
    def __init__(self, epoch, evento, user_id, lab_id = None,
                 nome_de_usuario = None):
        self.epoch = epoch
        self.evento = evento
        self.user_id = user_id
        self.lab_id = lab_id
        self.nome_de_usuario = nome_de_usuario
