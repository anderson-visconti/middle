# -*- coding: iso-8859-1 -*-
def importa_dados(full_path, cols):
    df_dados = pd.read_fwf(filepath_or_buffer=full_path,
                           delim_whitespace=True,
                           decimal=',',
                           names=cols
                           )

    df_dados['data'] = pd.to_datetime(full_path[-10:-4], format='%d%m%y') - pd.to_timedelta(arg=1, unit='D')

    df_dados.set_index(['data', 'lon', 'lat'], inplace=True)

    return df_dados

def make_map(dados, file_config, nome_modelo, datas):
    fig, ax = plt.subplots()
    m = Basemap(projection='merc',
                llcrnrlat=-35,
                urcrnrlat=9.0,
                llcrnrlon=-78,
                urcrnrlon=-30,
                resolution='i'
                )
    m.drawcoastlines(linewidth=0.15)
    m.drawcountries(linewidth=0.15)
    m.drawrivers(linewidth=0.3)
    shp = m.readshapefile(os.path.join(file_config['path_shape_file'], file_config['nome_shape_file']),
                          'states', drawbounds=True
                          )
    lons, lats = dados.index.get_level_values('lon').unique(), \
                 dados.index.get_level_values('lat').unique()

    x, y = np.meshgrid(lons, lats)
    precip = dados.unstack(level=[0])
    xx, yy = m(x, y)
    levels, cores_ons = get_config_ons(flag='s')

    s = '''Modelo {} - Rodada {:%d-%m-%Y}
            Periodo de {:%d-%m-%Y} a {:%d-%m-%Y}'''
    plt.title(s.format(nome_modelo, datas['data_inicial'], datas['de'], datas['ate']))
    cs = m.contourf(xx, yy, precip.values, levels=levels, colors=cores_ons, extend='both')
    cbar = m.colorbar(cs, location='bottom', label='Preciptacao [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=8)
    im = plt.imread(fname=os.path.join(file_config['path_logo'], file_config['nome_logo']))
    newax = fig.add_axes([0.58, 0.16, 0.2, 0.2], anchor='SE', zorder=+1)
    newax.imshow(im)
    newax.axis('off')
    plt.savefig(os.path.join(file_config['path_export'], '{:%Y%m%d}-{}.png'.format(datas['data_inicial'],
                                                                                   nome_modelo)),
                bbox_inches='tight'
                )

    return fig

def get_config_ons(flag='s'):
    if flag == 's':
        levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]  # nÃ­veis para chuva

    if flag == 'm':
        levels = [5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400]  # niveis para chuva

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
                 ]  # Escala de cores ONS
    return levels, cores_ons

if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    import os
    import glob


    path = {'ETA':r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\Chuva\ETA',
            'GESF':r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\Chuva\GESF'
            }

    datas = {'data_inicial': '2017-08-07',
                    'de': '2017-08-12',
                    'ate': '2017-08-18'
                    }

    file_config = {'path_export': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Base de Figuras\Conjunto\20170807',
                   'path_logo':r'C:\OneDrive\Middle Office\Middle\Hidrologia\Base de Figuras',
                   'nome_logo':r'Logo.png',
                   'path_shape_file':r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil',
                   'nome_shape_file':r'BRA_adm1'
                   }


    for i in datas.keys():
        datas[i] = pd.to_datetime(datas[i])

    df_precip_eta = pd.DataFrame()
    df_precip_gesf = pd.DataFrame()
    df_dados_aux = pd.DataFrame()

    #  Importa dados de chuva
    for i in path.keys():
        # lista arquivos
        files = glob.glob(os.path.join(path[i], '{:%Y%m%d}'.format(datas['data_inicial']), '*'))
        if i == 'ETA':
            for j in files:
                df_dados_aux = importa_dados(full_path=j, cols=['lon', 'lat', 'precip'])
                df_precip_eta = pd.concat(objs=[df_precip_eta, df_dados_aux])

        if i == 'GESF':
            for j in files:
                df_dados_aux = importa_dados(full_path=j, cols=['lon', 'lat', 'precip'])
                df_precip_gesf = pd.concat(objs=[df_precip_eta, df_dados_aux])


    # Filtrando datas
    eta_slice = pd.DataFrame(df_precip_eta.loc[datas['de']:datas['ate']])
    gesf_slice = pd.DataFrame(df_precip_gesf.loc[datas['de']: datas['ate']])

    eta_soma =pd.DataFrame(eta_slice.groupby(by=['lon', 'lat']).sum())
    gesf_soma =pd.DataFrame(gesf_slice.groupby(by=['lon', 'lat']).sum())

    eta_soma.to_csv(os.path.join(file_config['path_export'], 'eta_soma.csv'), sep=';', decimal=',')
    eta_slice.to_csv(os.path.join(file_config['path_export'], 'eta_diario.csv'), sep=';', decimal=',')
    fig = make_map(dados=gesf_soma, file_config=file_config, nome_modelo='GESF', datas=datas)
    fig = make_map(dados=eta_soma, file_config=file_config, nome_modelo='ETA', datas=datas)

    print('FIM')
    pass
