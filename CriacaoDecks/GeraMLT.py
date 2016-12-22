__author__= 'Anderson Visconti'

strPath = r'C:\Users\Anderson\Desktop\Gerador Decks'
strArqv = r'vazao.txt'

import os
from _datetime import datetime

strFullPath = os.path.join(strPath,strArqv)
file = open(strFullPath)
export = open(os.path.join(strPath,'saida.txt'),'w')

export.write('Posto;Data;Vazao\n')

for linha in file:
    aux = (' '.join(linha.split())).split(' ')
    codPosto = int(float(aux[0]))   # Codigo do Posto
    ano = int(float(aux[1]))

    for i in range(2,len(aux)):
        dtData = '{:%d/%m/%Y}'.format(datetime(year= ano, month= i - 1, day= 1))
        texto = '{0};{1};{2}'.format(codPosto, dtData, aux[i])
        export.write(texto + '\n')

file.close()
export.close()
print('qualquer coisa')
