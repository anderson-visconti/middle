import pandas as pd
from Chuva import *
from sklearn import preprocessing
import numpy as np
import pandas as pd

# Variaveis de chuva observada
path = {'path_chuva': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva',
        'path_export': r'C:\Users\anderson.visconti\Desktop\Nova pasta'
        }

nomes = {'variavel': 'cmorph', 'base': 'cmorph.3hr-025deg.', 'extensao': '.nc'}
nc_vars = {'chuva': 'cmorph_precip',
           'lat': 'lat',
           'lon': 'lon',
           'tempo': 'time'
           }

coords = {'lat': [-22.0, -20.0],
          'lon': [313.4, 316.0]
          }

tempos = {'t_inicial': '2016-12-10',
          't_final': '2016-12-13'
          }
# Variaveis chuva projetada
path_proj = {'path_chuva': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva',
             'path_export': r'C:\Users\anderson.visconti\Desktop\Projecao'
             }

nomes_proj = {'variavel': 'cfs', 'base': 'prate.01.2016091000', 'extensao': '.daily.nc'}

nc_vars_proj = {'chuva': 'PRATE_surface',
                'lat': 'lat',
                'lon': 'lon',
                'tempo': 'time'
                }

coords_proj = {'lat': [-22.0, -20.0],
               'lon': [313.4, 316.0]
               }

tempos_proj = {'t_inicial': '2016-12-14',
               't_final': '2016-12-14'
               }

# Dados de Vazao
path_vazoes = r'C:\Users\anderson.visconti\Desktop'
path_export_vazoes = r'C:\Users\anderson.visconti\Desktop'
nome_arquivo = {'nome':r'Vazoes.csv',
                'sep':';'
                }

colunas_vazoes = ['Data', 'intCodPosto', 'VazaoNatural']
postos = {'vazao': [6],
          'montante': [1,2,6]
          }

# Pega chuva
df_24h = pega_chuva(path=path, nc_vars=nc_vars, coords=coords, tempos=tempos, nomes=nomes)
df_24h = pd.DataFrame(df_24h)

# Pega projecao
df_24h_cfs = pega_cfs(path=path_proj, nc_vars=nc_vars_proj, coords=coords_proj,
                                tempos=tempos_proj, nomes=nomes_proj)
df_24h_cfs = pd.DataFrame(df_24h_cfs)

# Pega vazao propria e vazao montante
df_vazao, df_montante = pega_vazao(path=path_vazoes, path_export=path_export_vazoes,
                                   nome_arquivo=nome_arquivo, postos=postos, colunas=colunas_vazoes, tempos = tempos)
df_vazao = pd.DataFrame(df_vazao)
df_montante = pd.DataFrame(df_montante)

# Normaliza entradas das chuvas e projecoes para intervalo [0,1]
scaler_chuva = preprocessing.MinMaxScaler()
scaler_vazao = preprocessing.MinMaxScaler()
df_24h['precip_24h'] = scaler_chuva.fit_transform(df_24h['precip_24h'])
df_24h_cfs['precip_24h'] = scaler_chuva.fit_transform(df_24h_cfs['precip_24h'])
df_vazao['vazao'] = scaler_vazao.fit_transform(df_vazao['vazao'])
df_montante['vazao'] = scaler_vazao.fit_transform(df_montante['vazao'])

print df_24h.head()
df_24h_cfs['precip_24h'] = scaler_chuva.inverse_transform(df_24h_cfs['precip_24h'])
print df_24h.head()
pass


