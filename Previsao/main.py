import pandas as pd
from Chuva import *

path = {'path_chuva': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva',
            'path_export': r'C:\Users\ander\Desktop\Nova pasta'}

nomes = {'variavel': 'cmorph', 'base': 'cmorph.3hr-025deg.', 'extensao': '.nc'}
nc_vars = {'chuva': 'cmorph_precip',
           'lat': 'lat',
           'lon': 'lon',
           'tempo': 'time'}

coords = {'lat': [-22, -20],
          'lon': [313.4, 316]}

tempos = {'t_inicial': '2016-01-20',
          't_final': '2016-12-13'}

df_24h, df_tabular = pega_chuva(paths=path,
                                nc_vars=nc_vars,
                                coords=coords,
                                tempos=tempos)
print df_24h.head()
pass