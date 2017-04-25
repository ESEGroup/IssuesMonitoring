class ZonaConforto:
    def __init__(self, temp_min, temp_max, umidade_min, umidade_max,
                 lumin_min, lumin_max):
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.umidade_min = umidade_min
        self.umidade_max = umidade_max
        self.lumin_min = lumin_min
        self.lumin_max = lumin_max

class Equipamento:
    def __init__(self, temp_min, temp_max, MAC, id = None):
        self.id = id
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.MAC = MAC

    def obter_medidas(_id):
        pass

    def registrar_medidas(_id, temperatura):
        data_registro = int(datetime.now().timestamp())

    def cadastrar(self):
        pass

class Laboratorio:
    def __init__(self, nome, endereco, zona_conforto_lab,
                 intervalo_parser, intervalo_arduino, MACs = None,
                 equipamentos = None, id = None):
        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.intervalo_parser = intervalo_parser
        self.intervalo_arduino = intervalo_arduino
        self.zona_conforto_lab = zona_conforto_lab
        self.equipamentos = equipamentos
        self.MACs = MACs

    def registrar_medidas(_id, temperatura, luminosidade, umidade):
        data_registro = int(datetime.now().timestamp())

    def cadastrar_laboratorio(self):
        pass

    def editar_zona_conforto(_id, zona_conforto_lab):
        pass

    def editar_intervalos(_id, intervalo_parser, intervalo_arduino):
        pass

    def obter_medidas(_id):
        pass

    def reset_lista_presenca():
        pass
