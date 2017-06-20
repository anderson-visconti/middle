# -*- coding: iso-8859-1 -*-
def make_map(df_dados, nome_modelo, data_inicial, periodo_soma, path_export):
    from matplotlib.patches import Polygon
    fig, ax = plt.subplots()
    m = Basemap(projection='merc',
                llcrnrlat=-35,
                urcrnrlat=9.0,
                llcrnrlon=-78,
                urcrnrlon=-30,
                resolution='i'
                )
    m.ax = ax
    m.drawcoastlines(linewidth=0.15)
    m.drawcountries(linewidth=0.15)
    m.drawrivers(linewidth=0.3)
    #  Desenha estados brasileiros

    shp = m.readshapefile(r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil\BRA_adm1', 'states', drawbounds=True)
    for nshape, seg in enumerate(m.states):
        poly = Polygon(seg, facecolor='none', edgecolor='none', alpha=1.0)
        ax.add_patch(poly)

    #  Preparação do mapa
    lons, lats = df_dados.index.get_level_values('lon').unique(), \
                 df_dados.index.get_level_values('lat').unique()

    x, y = np.meshgrid(lons, lats)
    precip = df_dados.unstack(level=[0])
    xx, yy = m(x, y)
    levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]  # níveis para chuva
    cores_ons = [(255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),
                 (225.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0),
                 (180.0 / 255.0, 240.0 / 255.0, 250.0 / 255.0),
                 (40.0 / 255.0, 130.0 / 255.0, 240.0 / 255.0),
                 (20.0 / 255.0, 100.0 / 255.0, 210.0 / 255.0),
                 (103.0 / 255.0, 254.0 / 255.0, 133.0 / 255.0),
                 (24.0 / 255.0, 215.0 / 255.0, 6.0 / 255.0),
                 (30.0 / 255.0, 180.0 / 255.0, 30.0 / 255.0),
                 (255.0 / 255.0, 232.0 / 255.0, 120.0 / 255.0),
                 (255.0 / 255.0, 192.0 / 255.0, 60.0 / 255.0),
                 (255.0 / 255.0, 96.0 / 255.0, 0.0 / 255.0),
                 (225.0 / 255.0, 20.0 / 255.0, 0.0 / 255.0),
                 (251.0 / 255.0, 94.0 / 255.0, 107.0 / 255.0),
                 (170.0 / 255.0, 170.0 / 255.0, 170.0 / 255.0)
                 ]  #  Escala de cores ONS
    s = '''Modelo {} - Rodada {:%d-%m-%Y}
        Periodo de {:%d-%m-%Y} a {:%d-%m-%Y}'''
    plt.title(s.format(nome_modelo, data_inicial, periodo_soma['de'], periodo_soma['ate']))

    cs = m.contourf(xx, yy, precip.values, levels=levels, colors=cores_ons, extend='both')
    cbar = m.colorbar(cs, location='bottom', label='Preciptacao [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=8)
    plt.savefig(os.path.join(path_export, '{:%Y%m%d}-{}.png'.format(data_inicial, nome_modelo)),
                bbox_inches='tight'
                )
    return m, ax


def draw_states(ax, shapefile):
        shp = m.readshapefile(shapefile, 'states', drawbounds=True)
        for nshape, seg in enumerate(m.states):
            poly = Polygon(seg, facecolor='none', edgecolor='none', alpha=1.0)
            ax.add_patch(poly)

        return


def importa_dados(full_path, cols, types, data):
    import pandas as pd

    df_dados = pd.read_fwf(\
        filepath_or_buffer=full_path,
        delim_whitespace=True,
        decimal=',',
        names=cols,
        dtype=types
    )
    df_dados['data'] = pd.to_datetime(data)
    df_dados.set_index(['data', 'lon', 'lat'], inplace=True)

    return df_dados


def importa_config(full_path, cols):
    import pandas as pd

    df_config = pd.read_csv(filepath_or_buffer=full_path,
                            usecols=cols,
                            decimal=',',
                            sep=';'
                            )

    #df_config_eta = pd.DataFrame(df_config[df_config.modelo == 'eta'])
    #df_config_gesf = pd.DataFrame(df_config[df_config.modelo == 'gesf'])

    return df_config


def calcula_pesos(df_precip_eta, df_precip_gesf, df_config, df_pesos):
    import pandas as pd

    for i in df_config.iterrows():  #  itera sobre os pontos

        if i[1].modelo == 'eta':

            for j in df_precip_eta.index.get_level_values('data').unique(): #  itera sobre os dias

                df_precip_eta.set_value(index=(j, i[1].lon, i[1].lat),
                                        col='precip',
                                        value=df_precip_eta.loc[(j, i[1].lon, i[1].lat)] * \
                                              df_pesos[(df_pesos['nome_bacia'] == i[1]['nome_bacia']) &
                                                       (df_pesos['dia_proj']== (j- data_inicial).days)
                                              ]['eta'].values[0]
                                        )
        else:

            for j in df_precip_gesf.index.get_level_values('data').unique():  # itera sobre os dias

                df_precip_gesf.set_value(index=(j, i[1].lon, i[1].lat),
                                        col='precip',
                                        value=df_precip_gesf.loc[(j, i[1].lon, i[1].lat)] * \
                                              df_pesos[(df_pesos['nome_bacia'] == i[1]['nome_bacia']) &
                                                       (df_pesos['dia_proj'] == (j - data_inicial).days)
                                                       ]['gesf'].values[0]
                                        )

    return df_precip_eta, df_precip_gesf


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    import os
    from datetime import datetime
    t = datetime.now()

    cols = ['lon', 'lat', 'precip']
    types = {'lon': np.float, 'lat': np.float, 'precip': np.float}
    cols_config = ['cod', 'modelo', 'nome_bacia', 'sub_bacia', 'lat', 'lon']
    types_config = {'cod': str,
                    'modelo': str,
                    'nome_bacia': str,
                    'sub_bacia': str,
                    'lat': np.float,
                    'lon': np.float
                    }

    path = {'ETA':r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\Chuva-Vazao\Chuva\ETA',
            'GESF':r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\Chuva-Vazao\Chuva\GESF'
            }

    data_inicial = '2017-06-14'

    periodo_soma = {'de': '2017-06-15',
                    'ate': '2017-06-25'}

    file_config = {'path_config': r'C:\Users\ander\Desktop',
                   'nome': r'pontos_grade.csv',
                   'path_pesos': r'C:\Users\ander\Desktop',
                   'nome_pesos': r'pesos_projecao.csv',
                   'path_export': r'C:\Users\ander\Desktop'}


    for i in periodo_soma.keys():
        periodo_soma[i] = pd.to_datetime(periodo_soma[i])


    data_inicial = pd.to_datetime(data_inicial, infer_datetime_format=True)
    df_precip_eta = pd.DataFrame()
    df_precip_gesf = pd.DataFrame()

    #  Importa dados de chuva
    for i in path.keys():
        cont = 1
        arquivos = os.listdir(os.path.join(path[i], '{:%Y%m%d}'.format(data_inicial)))

        for j in arquivos:
            df_aux = importa_dados(full_path=os.path.join(path[i], '{:%Y%m%d}'.format(data_inicial), j),
                                   cols=cols,
                                   types=types,
                                   data=data_inicial + pd.to_timedelta(1 * cont, 'd'))

            if i == 'ETA':
                df_precip_eta = pd.concat([df_precip_eta, df_aux])
                cont += 1

            else:
                df_precip_gesf = pd.concat([df_precip_gesf, df_aux])
                cont += 1

    #  Importa dados de configuração
    df_config = importa_config(\
        full_path=os.path.join(file_config['path_config'], file_config['nome']),
        cols=cols_config
    )

    #  Importa pesos de projeção
    df_pesos = pd.read_csv(os.path.join(file_config['path_pesos'], file_config['nome_pesos']),
                           sep=';',
                           decimal=','
                           )

    #  Calcula pesos
    df_precip_eta, df_precip_gesf = calcula_pesos(df_precip_eta=df_precip_eta,
                                                  df_precip_gesf=df_precip_gesf,
                                                  df_config=df_config,
                                                  df_pesos=df_pesos
                                                  )
    df_conjunto =pd.DataFrame(df_precip_eta)

    #  Monta preciptação por conjunto
    for i in df_precip_eta.index.get_level_values('data').unique(): # itera sobre os dias

        for j in df_config['nome_bacia'].unique():  # itera sobre todas as bacias
            pontos_eta = df_config.loc[((df_config['nome_bacia'] == j) & (df_config['modelo']== 'eta')),
                                       ['lon', 'lat']
            ].values
            pontos_gesf = df_config.loc[((df_config['nome_bacia'] == j) & (df_config['modelo']== 'gesf')),
                                        ['lon', 'lat']
            ].values
            chuva_eta = 0.0
            chuva_gesf = 0.0

            for k in pontos_eta:    #  itera sobre os pontos de grade do ETA
                chuva_eta = chuva_eta + df_precip_eta.loc[i, k[0], k[1]].values

            for k in pontos_gesf:   #  itera sobre os pontos de grade do gesf
                chuva_gesf = chuva_gesf + df_precip_gesf.loc[i, k[0], k[1]].values

            chuva_media = (chuva_eta/len(pontos_eta) + chuva_gesf/len(pontos_gesf)) # determina chuva de conjunto

            for k in pontos_eta:    #  atualiza valor da chuva media de conjunto na grade do ETA
                df_conjunto.set_value(index=(i, k[0], k[1]),
                                      col='precip',
                                      value= chuva_media)

    #  Seleciona dados para acumular
    df_precip_eta = df_precip_eta.loc[periodo_soma['de']:periodo_soma['ate']]
    df_precip_gesf = df_precip_gesf.loc[periodo_soma['de']:periodo_soma['ate']]
    df_precip_conjunto = pd.DataFrame(df_conjunto.loc[periodo_soma['de']:periodo_soma['ate']])

    #  Acumula preciptacao no periodo
    df_acumulado_eta = pd.DataFrame(df_precip_eta.groupby(level=[1, 2]).sum())
    df_acumulado_gesf = pd.DataFrame(df_precip_gesf.groupby(level=[1, 2]).sum())
    df_acumulado_conjunto = pd.DataFrame(df_precip_conjunto.groupby(level=[1, 2]).sum())

    #  Mapa Conjunto
    m, ax = make_map(df_dados=df_acumulado_conjunto,
                     nome_modelo='Previsao por Conjunto',
                     data_inicial=data_inicial,
                     periodo_soma=periodo_soma,
                     path_export=file_config['path_export']
                     )
    #  Mapa ETA
    m, ax = make_map(df_dados=df_acumulado_eta,
                     nome_modelo='ETA',
                     data_inicial=data_inicial,
                     periodo_soma=periodo_soma,
                     path_export=file_config['path_export']
                     )
    #  Mapa GESF
    m, ax = make_map(df_dados=df_acumulado_gesf,
                     nome_modelo='GESF',
                     data_inicial=data_inicial,
                     periodo_soma=periodo_soma,
                     path_export=file_config['path_export']
                     )

    print('Tempo total: {}s'.format((datetime.now() - t).total_seconds()))
    print('Termino do script')
    pass
