# -*- coding: latin-1 -*-
def make_map():

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


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    import os

    cols = ['lon', 'lat', 'precip']
    types = {'lon': np.float, 'lat': np.float, 'precip': np.float}

    path = {'ETA':r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\Chuva-Vazao\Chuva\ETA',
            'GESF':r'C:\OneDrive\Middle Office\Middle\Hidrologia\Relatorios\Chuva-Vazao\Chuva\GESF'
            }

    data_inicial = '2017-06-14'
    periodo_soma = {'de': '2017-06-15',
                    'ate': '2017-06-20'}

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
                df_precip_gesf = pd.concat([df_precip_eta, df_aux])
                cont += 1

    #  Seleciona daddos para acumular
    df_precip_eta = df_precip_eta.loc[periodo_soma['de']:periodo_soma['ate']]
    df_precip_gesf = df_precip_gesf.loc[periodo_soma['de']:periodo_soma['ate']]

    #  Acumula preciptacao no periodo
    df_acumulado_eta = pd.DataFrame(df_precip_eta.groupby(level=[1, 2]).sum())
    df_acumulado_gesf = pd.DataFrame(df_precip_gesf.groupby(level=[1, 2]).sum())


    lons, lats = df_acumulado_eta.index.get_level_values('lon').unique(), \
                 df_acumulado_eta.index.get_level_values('lat').unique()

    x, y = np.meshgrid(lons, lats)
    #df_teste['precip']  = df_teste['precip'].apply(lambda x: x * 100.0)
    precip =  df_acumulado_eta.unstack(level=[0])
    #precip = df_acumulado_eta.pivot(index='lat', columns='lon', values='precip').values

    m, ax = make_map()
    draw_states(ax, shapefile=r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil\BRA_adm1')
    xx, yy = m(x, y)
    levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]
    cores_ons = [(255.0/255.0, 255.0/255.0, 255.0/255.0),
                 (225.0/255.0, 255.0/255.0, 255.0/255.0),
                 (180.0/255.0, 240.0/255.0, 250.0/255.0),
                 (40.0/255.0, 130.0/255.0, 240.0/255.0),
                 (20.0/255.0, 100.0/255.0, 210.0/255.0),
                 (103.0/255.0, 254.0/255.0, 133.0/255.0),
                 (24.0/255.0, 215.0/255.0, 6.0/255.0),
                 (30.0/255.0, 180.0/255.0, 30.0/255.0),
                 (255.0/255.0, 232.0/255.0, 120.0/255.0),
                 (255.0/255.0, 192.0/255.0, 60.0/255.0),
                 (255.0/255.0, 96.0/255.0, 0.0/255.0),
                 (225.0/255.0, 20.0/255.0, 0.0/255.0),
                 (251.0/255.0, 94.0/255.0, 107.0/255.0),
                 (170.0/255.0, 170.0/255.0, 170.0/255.0)
                 ]
    s = '''Modelo ETA - Rodada {:%d-%m-%Y}
    Periodo de {:%d-%m-%Y} a {:%d-%m-%Y}'''
    plt.title(s.format(data_inicial, periodo_soma['de'], periodo_soma['ate']))

    cs = m.contourf(xx, yy, precip.values, levels=levels, colors=cores_ons, extend='both')
    cbar = m.colorbar(cs, location='bottom', label='Preciptacao [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=8)
    #plt.savefig(r'C:\OneDrive\Middle Office\Middle\Hidrologia\teste.png')
    plt.show()


    pass
