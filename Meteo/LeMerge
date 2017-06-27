
if __name__ == '__main__':
    from netCDF4 import Dataset, num2date, MFDataset
    import os
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    import glob
    import pandas as pd
    from matplotlib.patches import Polygon



    paths = {'path': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva\merge',
             'export': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Base de Figuras\Merge',
             'logo': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Previsao precipitacao conjunto'
            }

    nomes = {'nome_logo': r'logo.png'}

    #  Periodo em que se realizara o somatorio
    periodo = {'de': '2017-06-01',
              'ate': '2017-06-26'
               }

    for i in periodo.keys():
        periodo[i] = pd.to_datetime(periodo[i])


    sub_set = {'lat': [-35.0, 5.5],
               'lon': [-70.0, -30]
               }

    lista = glob.glob(os.path.join(path=os.path.join(paths['path'], '*.nc')))
    df = pd.DataFrame(lista, columns=['caminho'])
    df['data'] = df['caminho'].apply(lambda x: x[-11:-3])
    df['data'] = pd.to_datetime(df['data'], format='%Y%m%d')
    df.set_index(keys=['data'], inplace=True)

    #  Filtra para o periodo selecionado
    lista = df.loc[periodo['de']: periodo['ate'], 'caminho']

    #  Informacoes das variavies do netcdf
    file = MFDataset(lista.values)  # abre todos os arquivos
    lons = file.variables['lon'][:]  # array com longitude
    lats = file.variables['lat'][:]  # array com latitude
    precip = file.variables['prec'][:]  # array com preciptacao
    temps = num2date(file.variables['time'][:], file.variables['time'].units)

    #  Recorta dados
    lat_inds = np.where((lats >= sub_set['lat'][0]) & (lats <= sub_set['lat'][1]))
    lon_inds = np.where((lons >= sub_set['lon'][0]) & (lons <= sub_set['lon'][1]))
    lons = file.variables['lon'][lon_inds[0]]
    lats = file.variables['lat'][lat_inds[0]]
    precip = file.variables['prec'][:, lat_inds[0], lon_inds[0]]

    fig, ax = plt.subplots()
    m = Basemap(projection='merc',
                llcrnrlat=lats.min(),
                urcrnrlat=lats.max(),
                llcrnrlon=lons.min(),
                urcrnrlon=lons.max(),
                resolution='i'
                )

    #m.drawcoastlines(linewidth=1.0)
    m.drawcountries(linewidth=1.0)
    m.drawrivers(linewidth=0.40)

    #  Desenha estados do Brasil
    shp = m.readshapefile(r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil\BRA_adm1', 'states',
                          drawbounds=True
                          )

    for nshape, seg in enumerate(m.states):
        poly = Polygon(seg, facecolor='none', edgecolor='none', alpha=1.0, linewidth=1.0)
        ax.add_patch(poly)


    x, y = np.meshgrid(lons, lats)
    xx, yy = m(x, y)

    levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]  # niveis para chuva

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


    cs = m.contourf(xx, yy, precip.sum(axis=0), levels=levels, colors=cores_ons, extend='both', alpha=0.90)
    cbar = m.colorbar(cs, location='bottom', label='Preciptacao [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=8)
    s = '''Chuva Observada - MERGE
    Periodo: {:%Y-%m-%d} - {:%Y-%m-%d}'''
    plt.title(s.format(periodo['de'], periodo['ate']))

    #  Informacao da empresa
    im = plt.imread(fname=os.path.join(paths['logo'], nomes['nome_logo']))
    newax = fig.add_axes([0.50, 0.16, 0.2, 0.2], anchor='SE', zorder=+1)
    newax.imshow(im, alpha=0.8)
    newax.axis('off')
    print os.path.join(paths['export'],
                             'Observado_{:%Y%m%d}_{:%Y%m%d}.png'.format(periodo['de'], periodo['ate'])
                             )
    plt.savefig(os.path.join(paths['export'],
                             'Observado_{:%Y%m%d}_{:%Y%m%d}.png'.format(periodo['de'], periodo['ate'])
                             ),
                bbox_inches='tight'
                )
    plt.show()
    print('Fim')
    pass
