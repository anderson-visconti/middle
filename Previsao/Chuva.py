def pega_chuva(path, nomes, nc_vars, coords, tempos):
    '''
    :param paths: dicionario de caminhos
    :param nomes: dicionario com estrutura da string dos arquivos netcdf
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
    # path = {'path_chuva': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva',
    #         'path_export': r'C:\Users\ander\Desktop\Nova pasta'}
    #
    # nomes = {'variavel': 'cmorph', 'base': 'cmorph.3hr-025deg.', 'extensao': '.nc'}
    # nc_vars = {'chuva': 'cmorph_precip',
    #            'lat': 'lat',
    #            'lon': 'lon',
    #            'tempo': 'time'}
    #
    # coords = {'lat': [-22, -20],
    #           'lon': [313.4, 316]}
    #
    # tempos = {'t_inicial': '2016-01-20',
    #           't_final': '2016-12-13'}

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
    df_diaria = df_indexado.unstack(level=[2, 1]).resample('D').sum().stack(level=[2, 1])
    # renomeia colunas
    df_diaria.index = df_diaria.index.set_names('data', level=0)
    df_diaria.rename(columns={'precip_3h': 'precip_24h'}, inplace=True)
    # monta dataframe tabular
    df_tabular = df_diaria.unstack(level=[2, 1])

    # escreve arquivos .csv
    # df_indexado.to_csv(r'{}\chuva-3.csv'.format(path_export), sep=';', decimal=',')
    df_diaria.to_csv(r'{}\chuva-24.csv'.format(path['path_export']), sep=';', decimal=',')
    df_tabular.to_csv(r'{}\chuva-tab.csv'.format(path['path_export']), sep=';', decimal=',')
    print '{}: {}s'.format('Tempo total para captura dos dados de chuva', (datetime.now() - t1).total_seconds())

    return df_diaria, df_tabular

def lags_chuva(df_tabular, n_lags):
    '''

    :param df_tabular: dataframe com dados de chuva em formato tabular
    :param n_lags: dicionario contendo o range de lags para chuva
    :return: dataframe com lags, sem remocao do NaN
    '''
    import numpy as np
    import pandas as pd

    df_temp = pd.DataFrame()    #  dataframe temporario

    for i in np.arange(df_tabular.columns.shape[0]):  # loop para cada coluna

        for j in range(n_lags['chuva'][0], n_lags['chuva'][1] + 1):  # loop para cada lag da variavel
            df_temp = pd.concat(objs=[df_temp,
                                      pd.Series(df_tabular[df_tabular.columns[i][0],
                                                           df_tabular.columns[i][1],
                                                           df_tabular.columns[i][2]],
                                                name='lon_{lon}_lat_{lat}_lag{lag}'.
                                                format(
                                                    lon=df_tabular.columns[i][1],
                                                    lat=df_tabular.columns[i][2],
                                                    lag=j)
                                                ).shift(j)
                                      ],
                                axis=1)

    return df_temp

def le_vazao(path, nomes_vazao, posto, tempos):
    import pandas as pd
    from datetime import datetime

    t1 = datetime.now()
    path = '{path_vazao}\{nome_vazao}{extensao}'.format(path_vazao=path['path_vazao'],
                                                        nome_vazao=nomes_vazao['nome_vazao'],
                                                        extensao=nomes_vazao['extensao']
                                                        )

    df_temp = pd.read_csv(filepath_or_buffer=path,
                          sep=';',
                          decimal=',',
                          usecols=['Data', 'intCodPosto', 'VazaoNatural'],
                          dtype={'Data': str},
                          )

    df_temp = df_temp.rename(columns={'Data': 'data', 'intCodPosto': 'posto', 'VazaoNatural': 'vazao_natural'})
    df_temp = df_temp[
        (df_temp['posto'] == posto['vazao']) |
        (df_temp['posto'] == posto['montante'])
        ]

    df_temp['data'] = pd.to_datetime(df_temp['data'])
    df_temp.set_index(['data', 'posto'], inplace=True)
    df_temp = df_temp.unstack().resample('D').bfill()
    df_temp = df_temp[tempos['t_inicial']: tempos['t_final']]

    print 'Tempo total para captura dos dados de chuva: {}s'.format((datetime.now() - t1).total_seconds())
    return df_temp