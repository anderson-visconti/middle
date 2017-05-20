from Chuva import *
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import TimeSeriesSplit
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
import pandas as pd
from itertools import chain
import matplotlib.pyplot as plt

from datetime import datetime

t1 = datetime.now()
#  Variaveis de chuva observada
path = {'path_chuva': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva',
        'path_export': r'C:\Users\anderson.visconti\Desktop\Nova pasta'
        }

nomes = {'variavel': 'cmorph', 'base': 'cmorph.3hr-025deg.', 'extensao': '.nc'}
nc_vars = {'chuva': 'cmorph_precip',
           'lat': 'lat',
           'lon': 'lon',
           'tempo': 'time'
           }

coords = {'lat': [-22.000, -21.125],
          'lon': [313.625, 315.875]
          }

tempos = {'t_inicial': '2016-01-01',
          't_final': '2016-12-13'
          }

#  Variaveis chuva projetada
path_proj = {'path_chuva': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva',
             'path_export': r'C:\Users\anderson.visconti\Desktop\Projecao'
             }

nomes_proj = {'variavel': 'cfs',
              'base': 'prate.01.2016091000',
              'extensao': '.daily.nc'
              }

nc_vars_proj = {'chuva': 'PRATE_surface',
                'lat': 'lat',
                'lon': 'lon',
                'tempo': 'time'
                }

coords_proj = {'lat': [-22.000, -21.125],
               'lon': [313.625, 315.875]
               }

tempos_proj = {'t_inicial': '2016-12-14',
               't_final': '2017-01-01'
               }

#  Dados de Vazao
path_vazoes = r'C:\Users\anderson.visconti\Desktop'
path_export_vazoes = r'C:\Users\anderson.visconti\Desktop'

nome_arquivo = {'nome': r'Vazoes.csv',
                'sep': ';'
                }

colunas_vazoes = ['Data', 'intCodPosto', 'VazaoNatural']

postos = {'vazao': [6],
          'montante': [0]
          }

limites_lags = {'vazao': [0.70, 1.0],
                'chuva': [0.40, 1.0],
                'montante': [0.7, 1.0]
                }

# retirado porque script calcula automaticamente
#lags = {'vazao': [1, 2, 3],
#        'chuva': [0, 1, 2],
#        'montante': [0, 1, 2, 3, 4, 5]
#        }

#  Pega chuva
df_24h = pega_chuva(path=path, nc_vars=nc_vars, coords=coords, tempos=tempos, nomes=nomes)
df_24h = pd.DataFrame(df_24h)

#  Pega projecao
df_24h_cfs = pega_cfs(path=path_proj, nc_vars=nc_vars_proj, coords=coords_proj,
                      tempos=tempos_proj, nomes=nomes_proj)

df_24h_cfs = pd.DataFrame(df_24h_cfs)

#  Pega vazao propria e vazao montante
df_vazao, df_montante = pega_vazao(path=path_vazoes, path_export=path_export_vazoes,
                                   nome_arquivo=nome_arquivo, postos=postos, colunas=colunas_vazoes, tempos=tempos)
df_vazao = pd.DataFrame(df_vazao)

df_montante = pd.DataFrame(df_montante)
if postos['montante'][0] == 0:
    df_montante.fillna(value=0, inplace=True)

#  Define lags  autoregressivos automaticamente
lags = define_lags(df_vazao=df_vazao, df_24h=df_24h, df_montante=df_montante, limites_lags=limites_lags, postos=postos)

#  Normaliza dados
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

#  Cria lags
df_vazao_lag, df_24H_lag, df_montante_lag, maior = cria_lags(df_vazao, df_24h, df_montante,
                                                      lags=lags, limites_lags=limites_lags, postos=postos)

#  Cria dataframe de entradas de lags
df_entradas = pd.DataFrame(index=pd.date_range(start=tempos['t_inicial'], end=tempos['t_final'], freq='D'))

for i in df_vazao_lag:
    df_entradas['{}'.format(i)] = df_vazao_lag.loc[:, i]

for i in df_24H_lag:
    df_entradas['{}'.format(i)] = df_24H_lag.loc[:, i]

for i in df_montante_lag:
    df_entradas['{}'.format(i)] = df_montante_lag.loc[:, i]

df_entradas.dropna(inplace=True)

#  Cria dataframe de saidas de lags
df_saidas = pd.DataFrame(df_vazao.loc[:, 'vazao'].shift(max(maior))).dropna()

#  Cria dataset para treinamento - k-folds series temporais
tscv = TimeSeriesSplit(n_splits=3)

t2 = datetime.now()
#  Criacao do modelo

mlp = MLPRegressor()
parameters = {'hidden_layer_sizes': [(30,), (50,), (100,), (150,), (300,), (500,), (600,),
                                     (800,)
                                     ],
              'activation':['relu'],
              'solver':['lbfgs'],
              'learning_rate': ['adaptive'],
              'early_stopping': [True],
              'max_iter': [200],
              'momentum': [0.9],
              }
#  neg_median_absolute_error - mediana do erro medio absoluto
#  r2 -
#  neg_mean_squared_error - erro medio quadratico
scores = ['neg_mean_squared_error']

#  Avaliacao dos hyperparametros - Escolha do melhor modelo - Validacao cruzada
clf = GridSearchCV(estimator=mlp, param_grid=parameters, scoring=scores[0], n_jobs=1, cv=tscv)
clf.fit(X=df_entradas, y=df_saidas)
resultados = pd.DataFrame(clf.cv_results_)
resultados.to_csv(path_or_buf='{}\{}_{}{}'.format(path['path_export'], 'resultados', postos['vazao'][0], '.csv'),
                  sep=';', decimal=','
                  )

print('Validacao Cruzada: {}s'.format(datetime.now() - t2))
print('Melhor modelo:'
      '{}'.format(clf.best_params_)
      )

print('Menor RMSE: {}'.format(clf.best_score_))
print('Tempo total: {}s'.format(datetime.now() - t1))

teste = clf.predict(df_entradas)

#  Simula serie temporal
df_24h_proj = pd.DataFrame(pd.concat([df_24h, df_24h_cfs], axis=0))
df_vazao_proj = pd.DataFrame(index=pd.date_range(tempos_proj['t_inicial'], tempos_proj['t_final']),
                             columns=df_vazao.columns
                             )

df_vazao_proj.fillna(value=0, inplace=True)

df_vazao_proj = pd.concat([df_vazao, df_vazao_proj], axis=0)

df_montante_proj = pd.DataFrame(index=pd.date_range(tempos_proj['t_inicial'], tempos_proj['t_final']),
                             columns=df_montante.columns
                             )

df_montante_proj.fillna(value=0, inplace=True)
df_montante_proj = pd.concat([df_montante, df_montante_proj], axis=0)
df_previsao = pd.DataFrame()

for i in pd.date_range(tempos_proj['t_inicial'], tempos_proj['t_final'], freq='D'):
    df_entradas_proj = pd.DataFrame(index=pd.date_range(tempos['t_inicial'], tempos_proj['t_final']))

    #  Cria lags
    df_vazao_lag_proj, df_24h_lag_proj, df_montante_lag_proj, maior = \
        cria_lags(df_vazao_proj, df_24h_proj, df_montante_proj,lags=lags, limites_lags=limites_lags, postos=postos)

    for j in df_vazao_lag_proj:
        df_entradas_proj['{}'.format(j)] = df_vazao_lag_proj.loc[:, j]

    for j in df_24h_lag_proj:
        df_entradas_proj['{}'.format(j)] = df_24h_lag_proj.loc[:, j]

    for j in df_montante_lag_proj:
        df_entradas_proj['{}'.format(j)] = df_montante_lag_proj.loc[:, j]

    df_entradas_proj = df_entradas_proj.loc[i, :]
    previsao = clf.predict(df_entradas_proj.reshape(1, -1))
    df_vazao_proj.set_value(i, ('vazao', postos['vazao'][0]), previsao)

    dic_temp = {'posto': postos['vazao'][0], 'previsao': scaler_vazao.inverse_transform(previsao)}
    df_temp = pd.DataFrame(dic_temp, index=[i])
    df_previsao = pd.concat([df_previsao, df_temp], axis=0)

print df_previsao

# Impressao do resultado
plt.figure()
plt.plot(df_saidas.index, scaler_vazao.inverse_transform(df_saidas.loc[:, (postos['vazao'][0])]), label='real',
         linewidth=2.0, color='red'
         )

plt.plot(df_saidas.index, scaler_vazao.inverse_transform(teste), color='blue', label='melhor_modelo', linewidth=1.25)
plt.plot(pd.date_range(tempos_proj['t_inicial'], tempos_proj['t_final'], freq='D'),
         df_previsao.loc[:, 'previsao'.format(postos['vazao'][0])], color='green',
         label='projecao', linewidth=1.25, linestyle='--'
         )

plt.title('posto - {}'.format(postos['vazao'][0]))
plt.xlabel('Tempo')
plt.ylabel('Vazao Natural [m^3/s]')
plt.legend(loc='upper right')
plt.grid()
df_previsao.to_csv(path_or_buf=r'{}\previsao_{}{}'.format(path['path_export'],postos['vazao'][0],'.csv'),
                   sep=';', decimal=',')
plt.show()
pass


