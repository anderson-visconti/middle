import pandas as pd
from Chuva import *
from sklearn import preprocessing
import numpy as np
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
# 313.4 316.0
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

# Pega chuva
df_24h, df_tabular = pega_chuva(path=path, nc_vars=nc_vars, coords=coords, tempos=tempos, nomes=nomes)

# Pega projecao
df_24h_cfs, df_tabular_cfs = pega_cfs(path=path_proj, nc_vars=nc_vars_proj, coords=coords_proj,
                                tempos=tempos_proj, nomes=nomes_proj)

# Normaliza entradas das chuvas [0,1]
scaler_chuva = preprocessing.MinMaxScaler()
df_24h['precip_24h'] = scaler_chuva.fit_transform(df_24h['precip_24h'])
print df_24h.head()
print df_24h_cfs.head()
print df_tabular_cfs.head()
pass