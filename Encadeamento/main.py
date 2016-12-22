#!/usr/bin/python
# *- coding: utf-8 -*-
__author__ = 'Anderson Visconti'
'''
Script para encadeamento Newave-Decomp-Newave
'''

arqv = ''
dadger = 'dadger.rv0'
path = r'C:\Users\anderson.visconti\Desktop\teste'
PathScript = r'/home/endesa/avisconti/script'

import sys
import os
sys.path.insert(0,PathScript)
from funcoes import *
# Variaveis de controle ------------------------------------------------------------------------------------------------
nNos = 1               # Numero de nos que o scritp requisitara
nProc = '40'            # Total de processadores ex: 8 nos com 8 proc = 64  em string
iniciaMPD = 0           # 1 - Aloca nos (versao legacy) ; 0 - Nao aloca nos (versao com hydra mais moderna)
fileNos = 'nodes'       # Nome do arquivo contendo os alias dos nos do cluster
dBinarios = {'newave': '/home/endesa/sw/newave'  ,
            'decomp': '/home/endesa/sw/decomp/bin'
             }                          # Local onde os binarios dos programas estao
dVersoes = {'newave': '22',
            'decomp': '24'
            }                           # Numero das Versoes dos softwares Newave e Decomp

Deslig = 0                              # Flag para desligar maquina no final; 1 - Desliga , 0 - Nao desliga
lista_email = ['anderson.visconti@enexenergia.com.br']  # Lista de email para envio dos resultados
# ----------------------------------------------------------------------------------------------------------------------
os.system('module load mpich/3.1.4')
fEncadeamento(Path=path,nProc=nProc, nNos=nNos, PathScript=PathScript, numVersaoNewave=dVersoes['newave'],
              numVersaoDecomp=dVersoes['decomp'], iniciaMPD=iniciaMPD, fileNos=fileNos, dBinarios=dBinarios,
              lista_email=lista_email)

print ('Fim')

if Deslig == 1:
    os.system('sudo poweroff')
