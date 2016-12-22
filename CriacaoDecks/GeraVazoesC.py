#!/usr/bin/python
# *- coding: utf-8 -*-
__author__ = 'Anderson Visconti'
'''
Script para editar arquivo vazoesC com projecoes feitas separadamente
O script acrescenta 1 ano apenas para facilitar ao ano inicial indicado e repete os valores
'''

import os
# Variaveis-------------------------------------------------------------------------------------------------------------
strPath = r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2016\12\01-pessimista-SE-medio-NE-N\vazoes'         # Caminho onde esta arquivo vazeosC base e arquivo de projecao
strPathExport = r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2016\12\01-pessimista-SE-medio-NE-N\vazoes'   # Caminho onde de exportacao
strNomeArquivo = r'Vazoes-2016.txt'                                       # Nome do arquivo base vazoesC
strNomeArqvProj = r'export-2017.txt'                                      # Nome do arquivo com vazoes projecoes
intAnoInicial = 2017                                                 # Ano a ser alterado
# ----------------------------------------------------------------------------------------------------------------------
vProjecoes = []
vDados = []
vDadosNew = []

# Leitura dos dados de vazoes projetadas -------------------------------------------------------------------------------
file = open(os.path.join(strPath, strNomeArqvProj))

for linha in file:
    aux = linha.split(';')

    for i in range(0,len(aux)):
        aux[i] = aux[i].strip() # Tira espacos em branco do vetor de string

    for i in range(2,len(aux)):
        aux[i] = aux[i][:-3]

    vProjecoes.append(aux)

print('Valores projetados na memoria')
# ----------------------------------------------------------------------------------------------------------------------

# Leitura do VazoesC ---------------------------------------------------------------------------------------------------
fileVazoes = open(os.path.join(strPath,strNomeArquivo),'r')

for linha in fileVazoes:
    vDados.append((' '.join(linha.split())).split(' '))

print('VazoesC na memoria')
#-----------------------------------------------------------------------------------------------------------------------

# Edicao do arquivo VazoesC --------------------------------------------------------------------------------------------
for i in range(0, len(vDados)):
    vDadosNew.append(vDados[i])

    # Verifica se precisa fazer alteracao ------------------------------------------------------------------------------
    if int(float(vDadosNew[i][1])) == intAnoInicial:   # Itera ate achar o ano que precisa ser alterado

        for j in range(1, len(vProjecoes)):  # procura o posto no vetor de projecoes

            if int(float(vDadosNew[i][0])) == int(float(vProjecoes[j][0])):

                for k in range(2, len(vDados[i])):    #Itera sobre o elemtento do vetor
                    vDadosNew[i][k] = vProjecoes[j][k]
    #-------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

# Escrita Arquivo VazoesC ----------------------------------------------------------------------------------------------
fileExport = open(os.path.join(strPathExport,'vazoesc.new',), 'w')
for i in range(0, len(vDadosNew)):
    aux = '{:>3} {:>4} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5}\n'.format(*vDadosNew[i])
    fileExport.write(aux)

    # Acrescenta um ano ------------------------------------------------------------------------------------------------
    if int(float(vDadosNew[i][1])) == intAnoInicial:
        vAux = vDadosNew[i]
        vAux[1] = str(intAnoInicial + 1)

        for i in range(2,len(vAux)):
            vAux[i] = '00'

        fileExport.write('{:>3} {:>4} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5}\n'.format(*vAux))
    #-------------------------------------------------------------------------------------------------------------------

fileExport.close()
print('Arquivo vazoesC gerado')
#-----------------------------------------------------------------------------------------------------------------------