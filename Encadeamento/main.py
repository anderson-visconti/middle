#!/usr/bin/python
# *- coding: utf-8 -*-
__author__ = 'Anderson Visconti'
'''
Script para encadeamento Newave-Decomp-Newave
'''

arqv = ''
dadger = 'dadger.rv0'
path = r'/home/centos/encadeamento/2018/201804/rv0/partida_1_carga_normal_p1'
PathScript = r'/home/centos/script'

import sys
import os
sys.path.insert(0,PathScript)
from funcoes import *
# Variaveis de controle ------------------------------------------------------------------------------------------------
nNos = 1                # Numero de nos que o scritp requisitara
nProc = '32'            # Total de processadores ex: 8 nos com 8 proc = 64  em string. 40 se for servidor enex ou 36 na amazon
iniciaMPD = 0           # 1 - Aloca nos (versao legacy) ; 0 - Nao aloca nos (versao com hydra mais moderna)
fileNos = 'nodes'       # Nome do arquivo contendo os alias dos nos do cluster
dBinarios = {'newave': '/usr/bin'  ,
            'decomp': '/usr/bin'
             }                          # Local onde os binarios dos programas estao
dVersoes = {'newave': '24.0.0',
            'decomp': '26.1'
            }                           # Numero das Versoes dos softwares Newave e Decomp


# Penalizacao de armazenamento por REE - Valor a utilizar como acrescimo ou penalidade
penalidades_ree = {
    1:0.96,
    6:0.96,
    7:0.96,
    5:0.96,
    10:0.92,
    12:0.97,
    2:0.95,
    11:0.95,
    3:0.99,
    4:0.98,
    8:0.98,
    9:0.98,
}
Deslig = 0                              # Flag para desligar maquina no final; 1 - Desliga , 0 - Nao desliga
lista_email = ['anderson.visconti@enexenergia.com.br',
               'alessandra.marques@enexenergia.com.br']  # Lista de email para envio dos resultados
# ----------------------------------------------------------------------------------------------------------------------
#os.system('module load mpich/3.1.4') # Caso necessite
fEncadeamento(Path=path,nProc=nProc, nNos=nNos, PathScript=PathScript, numVersaoNewave=dVersoes['newave'],
              numVersaoDecomp=dVersoes['decomp'], iniciaMPD=iniciaMPD, fileNos=fileNos, dBinarios=dBinarios,
              lista_email=lista_email, penalidades_ree=penalidades_ree)

print ('Fim')

if Deslig == 1:
    os.system('sudo poweroff')
