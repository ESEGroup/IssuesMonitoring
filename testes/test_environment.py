import pytest
from . import check_condicoes as cc

#teste espera que as luzes estejam acesas(retornaria '2', ultimo user + admin)(talvez)
# def test_checkIfLightsAreOn():
# 	assert cc.check_for_forgotten_lights(1) > 0

#ajeitar BD para proxima etapa

#se luzes estiverem apagadas, retorna -1 por default, não precisa checar nada
# def test_checkIfLightsAreOff():
# 	assert cc.check_for_forgotten_lights(1) == -1

#se tiver presentes no laboratório retorna presentes
# def test_checkPresents():
# 	assert cc.check_for_forgotten_lights(1) == "presentes"

# #ajeitar BD para proxima etapa

# #se temperatura anormal, retorna >0(users presentes+ admins)
# def test_checkIfTempIsOff():
# 	assert cc.check_for_abnormal_temperature(1) > 0

# #ajeitar BD para proxima etapa

# #se temperatura estiver normal, retorna -1
# def test_checkIfTempIsOk():
# 	assert cc.check_for_abnormal_temperature(1) == -1

# #ajeitar BD para proxima etapa

# #se umidade anormal, retorna >0(users presentes+ admins)
# def test_checkIfHumidityIsOff():
# 	assert cc.check_for_abnormal_humidity(1) > 0

# #ajeitar BD para proxima etapa

# se temperatura do equipamento estiver normal, retorna -1
# def test_checkIfEquipTempIsOk():
# 	assert cc.check_for_equipment_temperature(1, 1) == -1

# se temperatura do equipamento estiver anormal, retorna 1
def test_checkIfEquipTempIsNotOk():
	assert cc.check_for_equipment_temperature(1, 1) == 1




