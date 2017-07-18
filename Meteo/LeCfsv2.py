def config_ons(flag_escala='s'):
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
                 (170.0 / 255.0, 170.0 / 255.0, 170.0 / 255.0)]  # Escala de cores ONS

    if flag_escala == 'm':
        levels = [5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400]  # niveis para chuva
        cores = cores_ons

    if flag_escala == 's':
        levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]  # niveis para chuva
        cores = cores_ons

    if flag_escala == 'c':
        # levels = [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100, 120] # niveis para climatologia
        levels = np.arange(start=-200, stop=225, step=25)  # niveis para climatologia
        cores = 'seismic_r'
        # .get_cmap('seismic')

    return levels, cores


def make_map(lons, lats, paths, nomes, dados, periodo, flag_escala, precip_clima, lons_clima, lats_clima):
    x, y = np.meshgrid(lons, lats)

    # Interpolacao
    interpolacao = interp(datain=precip_clima, xin=lons_clima, yin=np.flipud(lats_clima), xout=x, yout=np.flipud(y))
    anomalia = (dados - interpolacao)

    #  Modelo CFSv2
    fig = plt.figure()
    #  Subplot 1
    m = Basemap(projection='merc',
                llcrnrlat=lats.min(),
                urcrnrlat=lats.max(),
                llcrnrlon=lons.min(),
                urcrnrlon=lons.max(),
                resolution='l',
                )
    m.drawmapboundary()
    m.drawcountries()
    m.drawcoastlines(linewidth=0.5)
    m.drawrivers(linewidth=0.25)

    #  Desenha estados do Brasil
    shp = m.readshapefile(os.path.join(paths['shape_estados'], nomes['shape_estados']), 'states',
                          drawbounds=True, linewidth=0.5)

    xx, yy = m(x, y)
    levels, cores = config_ons(flag_escala)

    cs = m.contourf(xx, yy, dados, levels=levels, colors=cores, extend='both', alpha=0.90)
    cbar = m.colorbar(cs, location='bottom', label='Preciptacao [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=8)
    s = '''Modelo CSFv2 - Rodada {}
    Periodo: {:%Y-%m-%d} a {:%Y-%m-%d}'''
    plt.title(s.format(nomes['chuva'][9:17], periodo['de'], periodo['ate']))

    #  Informacao da empresa
    im = plt.imread(fname=os.path.join(paths['logo'], nomes['nome_logo']))
    newax = fig.add_axes([0.59, 0.16, 0.2, 0.2], anchor='SE', zorder=+1)
    newax.imshow(im, alpha=0.8)
    newax.axis('off')

    plt.savefig(os.path.join(paths['export'], '{}_{:%Y-%m-%d}_{:%Y-%m-%d}.png'.format(nomes['chuva'][0:19],
                                                                                      periodo['de'],
                                                                                      periodo['ate']
                                                                                      )),
                bbox_inches='tight')

    #  Anomalia

    fig = plt.figure()
    #  Subplot 1
    m = Basemap(projection='merc',
                llcrnrlat=lats.min(),
                urcrnrlat=lats.max(),
                llcrnrlon=lons.min(),
                urcrnrlon=lons.max(),
                resolution='l',
                )
    m.drawmapboundary()
    m.drawcountries()
    m.drawcoastlines(linewidth=0.5)
    m.drawrivers(linewidth=0.25)

    #  Desenha estados do Brasil
    shp = m.readshapefile(os.path.join(paths['shape_estados'], nomes['shape_estados']), 'states',
                          drawbounds=True, linewidth=0.5)

    xx, yy = m(x, y)
    levels, cores = config_ons('c')
    cs = m.contourf(xx, yy, anomalia, levels=levels, cmap='bwr_r', extend='both', alpha=0.90)

    cbar = m.colorbar(cs, location='bottom', label='Anomalia [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=6)
    s = '''Anomalia CFSv2 - Rodada {}
        Periodo: {:%Y-%m-%d} a {:%Y-%m-%d}'''
    plt.title(s.format(nomes['chuva'][9:17], periodo['de'], periodo['ate']))

    #  Informacao da empresa
    im = plt.imread(fname=os.path.join(paths['logo'], nomes['nome_logo']))
    newax = fig.add_axes([0.59, 0.16, 0.2, 0.2], anchor='SE', zorder=+1)
    newax.imshow(im, alpha=0.8)
    newax.axis('off')

    plt.savefig(os.path.join(paths['export'], 'Anomalia_{}_{:%Y-%m-%d}_{:%Y-%m-%d}.png'.format(nomes['chuva'][0:19],
                                                                                               periodo['de'],
                                                                                               periodo['ate']
                                                                                               )),
                bbox_inches='tight')

    print('Encerramento da criacao do mapa')
    return fig


def loop_mapa(paths, nomes, variaveis, periodo, sub_set, flag_escala):
    from netCDF4 import Dataset, num2date, MFDataset
    import os
    import numpy as np
    import pandas as pd


    for i in periodo.keys():
        periodo[i] = pd.to_datetime(periodo[i])


        # Abre arquivos Netcdf
    file_chuva = Dataset(os.path.join(paths['chuva'], nomes['chuva']), 'r')
    file_clima = Dataset(r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Climatologia\precip.mon.ltm.nc', 'r')

    #  Dados chuva
    lons = file_chuva.variables[variaveis['csfv2'].get('lon')][:]
    lats = file_chuva.variables[variaveis['csfv2'].get('lat')][:]
    times = num2date(file_chuva.variables[variaveis['csfv2'].get('time')][:],
                     file_chuva.variables[variaveis['csfv2'].get('time')].units)

    #  Dados Climatologia
    lons_clima = file_clima.variables[variaveis['climatologia'].get('lon')][:]
    lats_clima = file_clima.variables[variaveis['climatologia'].get('lat')][:]
    times_clima = num2date(times=file_clima.variables[variaveis['climatologia'].get('time')][:],
                           units=file_clima.variables[variaveis['climatologia'].get('time')].units,
                           calendar='gregorian')

    data_ini = periodo['de']
    data_fim = periodo['ate']

    # Recorte dos dados do Brasil (CFSv2)
    lons_inds = np.squeeze(np.where((lons >= sub_set['lon'][0]) & (lons <= sub_set['lon'][1])))
    lats_inds = np.squeeze(np.where((lats >= sub_set['lat'][0]) & (lats <= sub_set['lat'][1])))
    lons = lons[lons_inds] - 360  # Ajuste para range -180 180 para plotar o shapefile dos estados
    lats = lats[lats_inds]
    times_inds = np.squeeze(np.where((times >= periodo['de']) & (times <= periodo['ate'])))

    # Recorte dos dados do Brasil (Clima)
    lons_inds_clima = np.squeeze(np.where((lons_clima >= sub_set['lon'][0]) & (lons_clima <= sub_set['lon'][1])))
    lats_inds_clima = np.squeeze(np.where((lats_clima >= sub_set['lat'][0]) & (lats_clima <= sub_set['lat'][1])))
    lons_clima = lons_clima[lons_inds_clima] - 360  # Ajuste para range -180 180 para plotar o shapefile dos estados
    lats_clima = lats_clima[lats_inds_clima]
    times_inds_clima = np.squeeze(np.where((times_clima >= periodo['de']) & (times_clima <= periodo['ate'])))

    # Precipitacao
    precip_chuva = file_chuva.variables[variaveis['csfv2'].get('precip')][times_inds, lats_inds, lons_inds] * 21600
    precip_clima = file_clima.variables[variaveis['clima'].get('precip')]
    p = np.zeros((lats_inds_clima.shape[0], lons_inds_clima.shape[0]))

    #  Cria figura
    for i in pd.date_range(start=data_ini, end=data_fim, freq='D'):
        aux = precip_clima[i.month - 1, lats_inds_clima, lons_inds_clima]
        p = np.sum([p, aux], axis=0)

    fig = make_map(lons=lons, lats=lats, paths=paths, nomes=nomes, dados=precip_chuva.sum(axis=0), periodo=periodo,
                   flag_escala=flag_escala, precip_clima=p, lons_clima=lons_clima, lats_clima=lats_clima)

    return

if __name__ == '__main__':
    import os
    import numpy as np
    from mpl_toolkits.basemap import Basemap, interp
    import matplotlib.pyplot as plt
    import pandas as pd

    paths = {'chuva': r'C:\Users\alessandra.marques\Desktop\netcdf',
             'climatologia': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Climatologia\precip.mon.ltm.nc',
             'export': r'C:\Users\alessandra.marques\Desktop\export',
             'shape_estados': r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil',
             'logo': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Previsao precipitacao conjunto'
             }

    variaveis = {'csfv2': {'lon': 'lon',
                           'lat': 'lat',
                           'time': 'time',
                           'precip': 'prate'},

                 'climatologia': {'lon': 'lon',
                                  'lat': 'lat',
                                  'time': 'time',
                                  'precip': 'precip'},

                 'clima': {'lon': 'lon',
                           'lat': 'lat',
                           'time': 'time',
                           'precip': 'precip'}}

    nomes = {'chuva': r'prate.02.2017071800.daily.nc',
             'climatologia': r'precip.mon.ltm.nc',
             'shape_estados': r'BRA_adm1',
             'nome_logo': 'logo.png'}

    # unit - 'd' para dias e 'MS' para meses
    step = {'n_periodos': 3,
            'step': 1,
            'unit': 'MS'
            }

    #  's' - escala semanal, 'm' - escala mensal, 'c' - climatologia(Anomalia)
    flag_escala = {'escala': 'm'}

    sub_set = {'lon': [285, 330],
               'lat': [-35.0, 5.5]
               }
    data_inicial = '2017-07-22'
    loop = pd.DataFrame(data=pd.date_range(data_inicial,
                                           periods=step['n_periodos'],
                                           freq='{}{}'.format(step['step'],
                                                              step['unit']
                                                              )
                                           ),
                        columns=['data_inicial']
                        )

    if step['unit'] == 'MS':
        loop['data_final'] = loop['data_inicial'].apply(lambda x: x + pd.to_timedelta(step['step'], 'M'))

    else:
        loop['data_final'] = loop['data_inicial'].apply(lambda x: x + pd.to_timedelta(step['step'], step['unit']))

    for i in loop.iterrows():
        loop_mapa(paths=paths,
                  nomes=nomes,
                  variaveis=variaveis,
                  periodo={'de': i[1]['data_inicial'], 'ate': i[1]['data_final']},
                  sub_set=sub_set,
                  flag_escala=flag_escala['escala']
                  )

    print('Fim Script')

