#pseudo_arduino, ou melhor, o nosso emulador de Arduino para testes com o Servidor
#envia JSON com dados periodicamente, de [segundo argumento] em [segundo argumento] segundos

import requests
import random
import sys
import time

random.seed()


#Formatos das funcoes
#random.gauss([media], [desvio padrao])
#random.uniform([minimo], [maximo])

luz = 0
umidade = 0.0
sensacao_termica = 0.0
equipamento1 = {'id': 1, 'temperatura': 0.0}
equipamento2 = {'id': 2, 'temperatura': 0.0}

if(len(sys.argv) != 3):
    print("Uso: python3 pseudo_arduino.py [ip-do-servidor/rota] [periodo de envio em segundos]")
    
while(True):

	#Calculando os valores das medidas

	#luz
	
	#acesa
	luz = 1

	#alguem da uma "luz" de como fazer. qual distribuicao?
	
	#umidade

	#minimo de 40% e maximo de 75%

	umidade = random.gauss(57.5, 12.5)

	#sensacao termica

	#minimo de 20 e maximo de 26
	sensacao_termica = random.gauss(23, 3)
	
	#equipamento 1
	#pode passar de 55 graus (que eh a temperatura em que a maquina deve ser desligada)
	equipamento1['temperatura'] = random.gauss(40, 20)
	
    #equipamento 2
	#pode passar de 55 graus (que eh a temperatura em que a maquina deve ser desligada)
	equipamento2['temperatura'] = random.gauss(40, 20)	
	
	r = requests.post("http://" + sys.argv[1], json={"MAC":"AB:BB:CC:DD:EE","lab_id":1,"dados":{"luz":luz,"umidade":umidade,"sensacao_termica":sensacao_termica,"equipamentos":[equipamento1,equipamento2]}})

	#mensagens de 2 em 2 minutos
	time.sleep(float(sys.argv[2]))
