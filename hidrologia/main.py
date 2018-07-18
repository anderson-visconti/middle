# !/usr/bin/env python
# *- coding: utf-8 -*-
import sys
import os
import pandas as pd
import openpyxl as pyxl
import pandas as pd
from hidrologia.Banco import *
from hidrologia.Hidro import *
from configparser import ConfigParser
import sqlalchemy

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

#
hidro = Hidrologia()
hidro.get_rdh(datas=['2018-07-17', '2018-07-16'])
wb = pyxl.load_workbook()





