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

tempos = {'t_inicial': '2016-01-01',
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
lags = {'vazao': [1],
        'chuva': [0, 1],
        'montante':[0, 1]
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

# Normaliza dados
scaler_vazao = preprocessing.MinMaxScaler()
scaler_chuva = preprocessing.MinMaxScaler()
scaler_montante = preprocessing.MinMaxScaler()

df_vazao = pd.DataFrame(data=scaler_vazao.fit_transform(df_vazao), index=df_vazao.index,
                        columns=df_vazao.columns)
df_24h = pd.DataFrame(data=scaler_chuva.fit_transform(df_24h), index=df_24h.index,
                      columns=df_24h.columns)
df_24h_cfs = pd.DataFrame(data=scaler_chuva.transform(df_24h_cfs), index=df_24h_cfs.index,
                          columns=df_24h_cfs.columns)
df_montante = pd.DataFrame(data=scaler_montante.fit_transform(df_montante), index=df_montante.index,
                           columns=df_montante.columns)

# Cria lags
df_vazao_lag, df_24H_lag, df_montante_lag = cria_lags(df_vazao, df_24h, df_montante, lags=lags)

# Cria dataframe de entradas
df_entradas = pd.DataFrame(index=pd.date_range(start=tempos['t_inicial'], end=tempos['t_final'], freq='D'))
for i in df_vazao_lag:
    print i
    df_entradas['{}'.format(i)] = df_vazao_lag.loc[:, i]

for i in df_24H_lag:
    df_entradas['{}'.format(i)] = df_24H_lag.loc[:, i]

for i in df_montante_lag:
    df_entradas['{}'.format(i)] = df_montante_lag.loc[:, i]

df_entradas.dropna(inplace=True)


pass


