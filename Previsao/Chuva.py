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
    '''
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
    '''
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

    print file.variables
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
    return df_24h, df_tabular

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
    '''
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
    '''
    temp = pd.date_range(start=tempos['t_inicial'], end=tempos['t_final'], freq='D', tz='UTC')
    caminhos = ['{path}\{variavel}\{nome_base}{extensao}'.format(
        path=path['path_chuva'],
        variavel=nomes['variavel'],
        nome_base=nomes['base'],
        extensao=nomes['extensao'])
    ]
    print caminhos[0]

    #for i in range(0, len(temp)):   # cria caminhos dos arquivos
    #    caminhos.append('{path}\{variavel}\{year}\{nome_base}{data_form}{extensao}'.format(
    #        path=path['path_chuva'],
    #        variavel=nomes['variavel'],
    #        year=temp[i].year,
    #        nome_base=nomes['base'],
    #        data_form=temp[i].strftime('%Y%m%d'),
    #        extensao=nomes['extensao']))

    file = MFDataset(caminhos)
    print file.variables
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
                print precip[i, j, k] * 21600.0

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
    df_24h.to_csv(r'{}\projecao-24.csv'.format(path['path_export']), sep=';', decimal=',')
    # df_tabular.to_csv(r'{}\chuva-tab.csv'.format(path_export), sep=';', decimal=',')
    print '{}: {}s'.format('Tempo total para captura dos dados de chuva', (datetime.now() - t1).total_seconds())
    return df_24h, df_tabular