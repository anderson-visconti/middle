def pega_chuva(path, nc_vars, coords, tempos, nomes):
    '''
    :param paths: dicionario de caminhos
    :param nc_vars: dicionario com nomes das variaveis do arquivo netcdf
    :param coords: dicionario com lat/lon para subset dos dados
    :param tempos: dicionario com t_inicial e t_final para recorte dos dados
    :return: df_24h - dataframe com dados acumulados de chuva em 24 horas
    :return: df_tabular - dataframe com dados acumulados de chuva em 24 horas em formato tabular
    '''
    import pandas as pd
    import numpy as np
    from netCDF4 import *
    from datetime import datetime

    t1 = datetime.now()

    temp = pd.date_range(start=tempos['t_inicial'], end=tempos['t_final'], freq='D', tz='UTC')
    caminhos = []

    for i in range(0, len(temp)):   # cria caminhos dos arquivos
        caminhos.append('{path}\{variavel}\{year}\{nome_base}{data_form}{extensao}'.format(
            path=path['path_chuva'],
            variavel=nomes['variavel'],
            year=temp[i].year,
            nome_base=nomes['base'],
            data_form=temp[i].strftime('%Y%m%d'),
            extensao=nomes['extensao']))

    file = MFDataset(caminhos)
    lats = file.variables[nc_vars['lat']][:]  # pega latitutes
    lons = file.variables[nc_vars['lon']][:]  # pega longitudes

    # indices para recortar em lat/lon
    lat_inds = np.where((lats >= coords['lat'][0]) & (lats <= coords['lat'][1]))
    lon_inds = np.where((lons >= coords['lon'][0]) & (lons <= coords['lon'][1]))

    # subset dos dados
    sub_lats = lats[lat_inds[0]]
    sub_lons = lons[lon_inds[0]]

    sub_times = num2date(file.variables[nc_vars['tempo']][:], file.variables[nc_vars['tempo']].units)
    precip = file.variables[nc_vars['chuva']][:, lat_inds[0], lon_inds[0]]
    dados = []

    for i in range(0, precip.shape[0]):  # tera sobre o tempo
        for j in range(0, precip.shape[1]):  # itera sobre lat
            for k in range(0, precip.shape[2]):  # itera sobre lon
                dados.append([sub_times[i],
                              sub_lats[j],
                              sub_lons[k],
                              precip[i, j, k] * 3])

    df = pd.DataFrame(data=dados, columns=['data_3h', 'lat', 'lon', 'precip_3h'])
    df_indexado = df.set_index(['data_3h', 'lat', 'lon'])
    # calcula chuva acumulada em 24 h
    df_24h = df_indexado.unstack(level=[2, 1]).resample('D').sum().stack(level=[2, 1])
    # renomeia colunas
    df_24h.index = df_24h.index.set_names('data', level=0)
    df_24h.rename(columns={'precip_3h': 'precip_24h'}, inplace=True)
    # monta dataframe tabular
    df_tabular = df_24h.unstack(level=[2, 1]).resample('D').sum()
    # esreve arquivos .csv
    # df_indexado.to_csv(r'{}\chuva-3.csv'.format(path_export), sep=';', decimal=',')
    df_24h.to_csv(r'{}\chuva-24.csv'.format(path['path_export']), sep=';', decimal=',')
    # df_tabular.to_csv(r'{}\chuva-tab.csv'.format(path_export), sep=';', decimal=',')
    print '{}: {}s'.format('Tempo total para captura dos dados de chuva', (datetime.now() - t1).total_seconds())
    df_24h = pd.DataFrame(df_24h)
    df_tabular = pd.DataFrame(df_tabular)
    return df_tabular


def pega_cfs(path, nc_vars, coords, tempos, nomes):
    '''
    :param paths: dicionario de caminhos
    :param nc_vars: dicionario com nomes das variaveis do arquivo netcdf
    :param coords: dicionario com lat/lon para subset dos dados
    :param tempos: dicionario com t_inicial e t_final para recorte dos dados
    :return: df_24h - dataframe com dados acumulados de chuva em 24 horas
    :return: df_tabular - dataframe com dados acumulados de chuva em 24 horas em formato tabular
    '''
    import pandas as pd
    import numpy as np
    from netCDF4 import *
    from datetime import datetime

    t1 = datetime.now()
    temp = pd.date_range(start=tempos['t_inicial'], end=tempos['t_final'], freq='D', tz='UTC')
    caminhos = ['{path}\{variavel}\{nome_base}{extensao}'.format(
        path=path['path_chuva'],
        variavel=nomes['variavel'],
        nome_base=nomes['base'],
        extensao=nomes['extensao'])
    ]

    file = MFDataset(caminhos)
    lats = file.variables[nc_vars['lat']][:]  # pega latitutes
    lons = file.variables[nc_vars['lon']][:]  # pega longitudes

    # indices para recortar em lat/lon
    lat_inds = np.where((lats >= coords['lat'][0]) & (lats <= coords['lat'][1]))
    lon_inds = np.where((lons >= coords['lon'][0]) & (lons <= coords['lon'][1]))

    # subset dos dados
    sub_lats = lats[lat_inds[0]]
    sub_lons = lons[lon_inds[0]]

    sub_times = num2date(file.variables[nc_vars['tempo']][:], file.variables[nc_vars['tempo']].units)
    precip = file.variables[nc_vars['chuva']][:, lat_inds[0], lon_inds[0]]
    dados = []

    for i in range(0, precip.shape[0]):  # tera sobre o tempo
        for j in range(0, precip.shape[1]):  # itera sobre lat
            for k in range(0, precip.shape[2]):  # itera sobre lon
                dados.append([sub_times[i],
                              sub_lats[j],
                              sub_lons[k],
                              precip[i, j, k] * 21600.0
                              ]
                             )

    df = pd.DataFrame(data=dados, columns=['data_3h', 'lat', 'lon', 'precip_3h'])
    df_indexado = df.set_index(['data_3h', 'lat', 'lon'])
    # calcula chuva acumulada em 24 h
    df_24h = df_indexado.unstack(level=[2, 1]).resample('D').sum().stack(level=[2, 1])

    # renomeia colunas
    df_24h.index = df_24h.index.set_names('data', level=0)
    df_24h.rename(columns={'precip_3h': 'precip_24h'}, inplace=True)
    # monta dataframe tabular
    df_tabular = df_24h.unstack(level=[2, 1]).resample('D').sum()
    # esreve arquivos .csv
    df_24h.to_csv(r'{}\projecao-24.csv'.format(path['path_export']), sep=';', decimal=',')
    print '{}: {}s'.format('Tempo total para captura dos dados de chuva', (datetime.now() - t1).total_seconds())
    df_24h = pd.DataFrame(df_24h)
    df_tabular = pd.DataFrame(df_tabular)
    df_tabular = df_tabular[tempos['t_inicial']: tempos['t_final']]
    return df_tabular


def pega_vazao(path, path_export, nome_arquivo, postos, colunas, tempos):
    import pandas as pd
    import os
    import numpy as np

    df_temp = pd.read_csv(filepath_or_buffer=os.path.join(path, nome_arquivo['nome']),
                          sep=nome_arquivo['sep'],
                          usecols=colunas,
                          decimal=',',
                          dtype = {colunas[0]: object, colunas[1]: np.int, colunas[2]: np.float64}
                          )

    df_temp.rename(columns=dict(zip(colunas, ['data', 'posto', 'vazao'])), inplace=True)
    df_temp = df_temp[df_temp['posto'].isin(postos['vazao']) |
                      df_temp['posto'].isin(postos['montante'])
                      ]

    df_temp['data'] = pd.to_datetime(df_temp['data'], format='%d/%m/%Y')
    df_temp.set_index(['data', 'posto'], inplace=True)
    df_temp.sort_index(level=[0, 1], ascending=True, inplace=True)
    df_temp = df_temp.unstack(level=[1])
    df_temp.fillna(method='ffill', axis=0, inplace=True)
    df_temp = df_temp.loc[tempos['t_inicial'] : tempos['t_final'], :]

    # Monta df Vazao propria
    df_vazao = pd.DataFrame(df_temp.loc[:, ('vazao', postos['vazao'][0])])
    df_vazao.fillna(method='ffill', axis=0, inplace=True)
    df_vazao.sort_index(ascending=True, inplace=True)

    # Monta df vazao montante propria
    df_montante = pd.DataFrame(df_temp.loc[:, zip(['vazao'] * len(postos['montante']), postos['montante'])])
    df_montante.columns = df_montante.columns.set_levels(['vazao_montante'], level=0)
    df_montante.to_csv(path_or_buf=os.path.join(path, 'df_montante_{}.csv'.format(postos['vazao'][0])),
                       sep=nome_arquivo['sep'], decimal=','
                       )

    df_vazao.to_csv(path_or_buf=os.path.join(path, 'df_vazao_{}.csv'.format(postos['vazao'][0])),
                    sep=nome_arquivo['sep'], decimal=','
                    )
    return df_vazao, df_montante


def cria_lags(df_vazao, df_24h, df_montante, lags, limites_lags, postos):
    import pandas as pd
    import numpy as np

    df_vazao_lag = pd.DataFrame(index=df_vazao.index)
    df_chuva_lag = pd.DataFrame(index=df_24h.index)
    df_montante_lag = pd.DataFrame(index=df_montante.index)


    lags_vazao = pd.DataFrame(lags['vazao'])
    lags_chuva = pd.DataFrame(lags['chuva'])
    lags_montante = pd.DataFrame(lags['montante'])
    maior = []
    #(lags_vazao['vazao_{}'.format(postos['vazao'][0])] >= limites_lags['vazao'][0])
    temp = lags_vazao[(lags_vazao['lags'] < 0) &
                      (lags_vazao['vazao_{}'.format(postos['vazao'][0])] >= limites_lags['vazao'][0])
    ]

    maior.append(max(temp.loc[:, 'lags'] * -1))
    for i in df_vazao.columns:
        for j in temp['lags']:
            df_vazao_lag = pd.concat(objs=[df_vazao_lag,
                                           pd.Series(df_vazao[i].shift(periods=-j),name='{}_{}_{}_{}'.format(
                                               i[0], i[1], 'lag', -j)
                                                     )
                                           ],
                                     axis=1)

    temp = lags_chuva[(lags_chuva.iloc[:, 1:] >= limites_lags['chuva'][0]) &
                      (lags_chuva.iloc[:, 1:] <= limites_lags['chuva'][1])
    ]

    maior.append(0)
    for i in df_24h.columns:
        for j in list(temp.index.values):
            if np.isnan(temp.loc[j, '{}_{}'.format(i[1], i[2])]) != True:
                if -j > maior[1]:
                    maior[1] = -j

                df_chuva_lag = pd.concat(objs=[df_chuva_lag,
                                               pd.Series(df_24h[i].shift(periods=-j), name='{}_{}_{}_{}_{}'.format(
                                                   i[0], i[1], i[2], 'lag', -j)
                                                         )
                                               ],
                                         axis=1)

    temp = lags_montante[(lags_montante.iloc[:, 1:] >= limites_lags['montante'][0]) &
                     (lags_montante.iloc[:, 1:] <= limites_lags['montante'][1])
    ]

    maior.append(0)
    for i in df_montante.columns:
        for j in list(temp.index.values):
            if np.isnan(temp.loc[j, '{}_{}'.format(i[0], i[1])]) != True:
                if -j > maior[2]:
                    maior[2] = -j

                df_montante_lag = pd.concat(objs=[df_montante_lag,
                                               pd.Series(df_montante[i].shift(periods=-j),name='{}_{}_{}_{}'.format(
                                                   i[0], i[1], 'lag', -j)
                                                         )
                                               ],
                                         axis=1)

    return df_vazao_lag, df_chuva_lag, df_montante_lag, maior

def define_lags(df_vazao, df_24h, df_montante, limites_lags, postos):
    from sklearn import preprocessing
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import itertools


    colors = itertools.cycle(["r", "b", "g"])
    df_vazao_norm = preprocessing.normalize(df_vazao.loc[:, ('vazao', postos['vazao'][0])].reshape(1, -1))[0]
    x = np.arange(-34, 1, 1)
    chuva_corr = pd.DataFrame(index=x, data=x, columns=['lags'])
    montante_corr = pd.DataFrame(index=x, data=x, columns=['lags'])
    vazao_corr = pd.DataFrame(index=x, data=x, columns=['lags'])

    plt.figure(1)
    for i in df_24h.columns:
        chuva_norm = preprocessing.normalize(df_24h.loc[:, i].reshape(1, -1))[0]
        xcorr = np.correlate(df_vazao_norm, chuva_norm, mode='full')[df_24h.shape[0] - 35 : df_24h.shape[0]]
        chuva_corr['{}_{}'.format(i[1], i[2])] = xcorr
        plt.scatter(x, xcorr, color=next(colors), label='{}_{}'.format(i[1], i[2]))

    plt.plot(x, np.ones(len(x)) * limites_lags['chuva'][0])
    plt.grid(True)

    plt.figure(2)

    for i in df_montante.columns:
        montante_norm = preprocessing.normalize(df_montante.loc[:, i].reshape(1, -1))[0]
        xcorr = np.correlate(df_vazao_norm, montante_norm, mode='full')[df_montante.shape[0] - 35: df_montante.shape[0]]
        montante_corr['{}_{}'.format(i[0], i[1])] = xcorr
        plt.scatter(x, xcorr, color=next(colors), label='{}_{}'.format(i[0], i[1]))

    plt.plot(x, np.ones(len(x)) * limites_lags['montante'][0], color=next(colors))
    plt.grid(True)
    plt.legend(loc='lower left')

    plt.figure(3)
    xcorr = np.correlate(df_vazao_norm, df_vazao_norm, mode='full')[df_vazao_norm.shape[0] - 35: df_vazao_norm.shape[0]]
    vazao_corr['{}_{}'.format('vazao', postos['vazao'][0])] = xcorr
    plt.scatter(x, xcorr, color=next(colors), label='{}_{}'.format('vazao', postos['vazao'][0]))
    plt.plot(x, np.ones(len(x)) * limites_lags['vazao'][0], color=next(colors))
    plt.grid(True)
    plt.legend(loc='lower left')

    #plt.show()

    lags = {'vazao': vazao_corr,
            'montante': montante_corr,
            'chuva': chuva_corr
            }

    return lags

