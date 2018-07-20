# !/usr/bin/env python
# *- coding: utf-8 -*-
import sys
import os
import openpyxl as pyxl
import pandas as pd
import pyexcel
import sqlalchemy
from configparser import ConfigParser
from hidrologia.Banco import *
from hidrologia.Hidro import Hidrologia, Calculador
from hidrologia.Postos import *

config = {
    'user': 'admin',
    'password': 'idealenergia#01',
    'host': r'onsdb.cm0s2bcwfhep.sa-east-1.rds.amazonaws.com',
    'database': 'db_hidro',
    'raise_on_warnings': True,
    'port': 3306,
    'get_warnings': True
}
# Leitura da configuracao dos parametros de configuracao
config_file = ConfigParser(
    defaults=None,
    allow_no_value=True
)
config_file.read('config.ini')

rdhs = [
    r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\RDH\2018\RDH12JUL.xlsx',
    r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\RDH\2018\RDH13JUL.xlsx'
]

acomphs = [
    r'C:\Onedrive\Middle Office\Middle\Hidrologia\Relatorios\AcompH\2018\ACOMPH_20180713.xls'
]

config_acomph = dict(
    row=[6, 35],
    bloco_dados=8
)

hidro = Hidrologia()
hidro.get_acomph(
    acomphs=acomphs,
    config_acomph=config_acomph)

# Determina todos os postos calculados
for posto in Posto.__subclasses__():
    calculador = Calculador()
    print(posto.__name__)
    calculador.realiza_calculo(dados=hidro.dados, posto=posto())


#calculador = Calculador()
#calculador.realiza_calculo(dados=hidro.dados, posto=P119())







