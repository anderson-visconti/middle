import pandas as pd
import numpy as np
from datetime import datetime
from Chuva import *
t1 = datetime.now()

# Caminhos
path = {'path_chuva': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva',
        'path_export': r'C:\Users\ander\Desktop\Nova pasta',
        'path_vazao': r'C:\Users\ander\Desktop'}

# Especificacoes do arquivo netcdf
nomes = {'variavel': 'cmorph',
         'base': 'cmorph.3hr-025deg.',
         'extensao': '.nc'
         }
# Especificacoes do arquivo csv de vazoes
nomes_vazao ={'nome_vazao': 'vazao',
              'extensao': '.csv'}

# Especificacoes de filtragem
posto ={'vazao': 6,
        'montante': 1}

nc_vars = {'chuva': 'cmorph_precip',
           'lat': 'lat',
           'lon': 'lon',
           'tempo': 'time'
           }

coords = {'lat': [-22, -20],
          'lon': [313.4, 316]
          }

tempos = {'t_inicial': '2016-01-01',
          't_final': '2016-12-13'
          }

# range de lags para cada variavel - chuva, vazao propria e vazao a montante
n_lags = {'chuva': [0, 5],
          'vazao': [1, 5],
          'montante': [0, 7]
          }

# Pega dados de chuva
df_24h, df_tabular = pega_chuva(path=path, nomes=nomes, nc_vars=nc_vars, coords=coords, tempos=tempos)

# Pega dados de vazao montante
df_vazao = le_vazao(path=path, nomes_vazao=nomes_vazao, posto=posto, tempos=tempos)

# Prepara lags de chuva
df_lags = lags_chuva(df_tabular=df_tabular, n_lags=n_lags)

df_lags.to_csv(path_or_buf=r'{path_export}\chuva-lags.csv'.format(path_export=path['path_export']),
               sep=';',
               decimal=',')

df_vazao.to_csv(path_or_buf=r'{path_export}\vazao.csv'.format(path_export=path['path_export']),
               sep=';',
               decimal=',')

pass
