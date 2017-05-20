class Medida_Lab:
    def __init__(self, lab_id, lum, hum, term_sens, medidas_equips, epoch=None):
        self.epoch          = epoch
        self.lab_id         = lab_id
        self.lum            = lum
        self.hum            = hum
        self.term_sens      = term_sens
        self.medidas_equips = medidas_equips

class Medida_Equip:
    def __init__(self, equip_id, temp):
        self.equip_id = equip_id
        self.temp     = temp
