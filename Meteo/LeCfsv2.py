def config_ons(flag_escala='s'):
    if flag_escala == 'm':
        levels = [5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400]  # niveis para chuva

    if flag_escala == 's':
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
    return levels, cores_ons


def make_map(lons, lats, paths, nomes, dados, periodo, flag_escala):
    x, y = np.meshgrid(lons, lats)

    fig = plt.figure()
    #  Subplot 1
    m = Basemap(projection='merc',
                llcrnrlat=lats.min(),
                urcrnrlat=lats.max(),
                llcrnrlon=lons.min(),
                urcrnrlon=lons.max(),
                resolution='i',
                )
    m.drawmapboundary()
    m.drawcountries()
    m.drawcoastlines(linewidth=0.5)
    m.drawrivers(linewidth=0.25)
    #  Desenha estados do Brasil
    shp = m.readshapefile(os.path.join(paths['shape_estados'], nomes['shape_estados']), 'states',
                          drawbounds=True, linewidth=0.5)

    xx, yy = m(x, y)
    levels, cores_ons = config_ons(flag_escala)
    cs = m.contourf(xx, yy, dados, levels=levels, colors=cores_ons, extend='both', alpha=0.90)
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

    print('Encerramento da criacao do mapa')
    return fig


def loop_mapa(paths, nomes, variaveis, periodo, sub_set, flag_escala):
    from netCDF4 import Dataset, num2date, MFDataset
    import os
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    import pandas as pd
    '''
    paths = {'chuva': r'C:\Users\anderson.visconti\Desktop\netcdf',
             'clima': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Climatologia',
             'export': r'C:\Users\anderson.visconti\Desktop\export\2017062800',
             'shape_estados': r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil'
             }

    variaveis = {'csfv2': {'lon': 'lon',
                           'lat': 'lat',
                           'time': 'time',
                           'precip': 'prate'
                           },

                 'clima': {'lon': 'lon',
                           'lat': 'lat',
                           'time': 'time',
                           'precip': 'precip'
                           }
                 }

    nomes = {'chuva': r'prate.01.2017062800.daily.nc',
             'clima': r'precip.mon.ltm.nc',
             'shape_estados': r'BRA_adm1'
             }

    #  Periodo para somar
    periodo = {'de': '2017-08-01',
               'ate': '2017-09-01',
               }
    step = 5

    sub_set = {'lon': [285, 330],
               'lat': [-35.0, 5.5]
              }    
    
    pd.to_timedelta(step, unit='d')
    '''

    for i in periodo.keys():
        periodo[i] = pd.to_datetime(periodo[i])

    # Abre arquivos Netcdf
    file_chuva = Dataset(os.path.join(paths['chuva'], nomes['chuva']), 'r')
    file_clima = Dataset(os.path.join(paths['clima'], nomes['clima']), 'r')

    #  Dados chuva
    lons = file_chuva.variables[variaveis['csfv2'].get('lon')][:]
    lats = file_chuva.variables[variaveis['csfv2'].get('lat')][:]
    times = num2date(file_chuva.variables[variaveis['csfv2'].get('time')][:],
                     file_chuva.variables[variaveis['csfv2'].get('time')].units
                     )

    # Recorte dos dados
    lons_inds = np.squeeze(np.where((lons >= sub_set['lon'][0]) & (lons <= sub_set['lon'][1])))
    lats_inds = np.squeeze(np.where((lats >= sub_set['lat'][0]) & (lats <= sub_set['lat'][1])))
    lons = lons[lons_inds] - 360  # Ajuste para range -180 180 para plotar o shapefile dos estados
    lats = lats[lats_inds]
    times_inds = np.squeeze(np.where((times >= periodo['de']) & (times <= periodo['ate'])))
    precips = file_chuva.variables[variaveis['csfv2'].get('precip')][times_inds, lats_inds, lons_inds] * 21600

    #  Cria figura
    fig = make_map(lons=lons, lats=lats, paths=paths, nomes=nomes, dados=precips.sum(axis=0), periodo=periodo,
                   flag_escala=flag_escala)
    return


if __name__ == '__main__':
    from netCDF4 import Dataset, num2date, MFDataset
    import os
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    import pandas as pd

    paths = {'chuva': r'C:\Users\anderson.visconti\Desktop\netcdf',
             'clima': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Climatologia',
             'export': r'C:\Users\anderson.visconti\Desktop\export\2017070500',
             'shape_estados': r'C:\OneDrive\Middle Office\Middle\Hidrologia\ShapeFiles\brasil',
             'logo': r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Previsao precipitacao conjunto'
             }

    variaveis = {'csfv2': {'lon': 'lon',
                           'lat': 'lat',
                           'time': 'time',
                           'precip': 'prate'
                           },

                 'clima': {'lon': 'lon',
                           'lat': 'lat',
                           'time': 'time',
                           'precip': 'precip'
                           }
                 }

    nomes = {'chuva': r'prate.02.2017070500.daily.nc',
             'clima': r'precip.mon.ltm.nc',
             'shape_estados': r'BRA_adm1',
             'nome_logo': 'logo.png'
             }


    # unit - 'd' para dias e 'MS' para meses
    step = {'n_periodos': 9,
            'step': 7,
            'unit': 'd'
            }

    #  's' - escala semanal, 'm' - escala mensal
    flag_escala = {'escala': 's'}

    sub_set = {'lon': [285, 330],
               'lat': [-35.0, 5.5]
               }

    data_inicial = '2017-07-01'
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
                  periodo={'de':i[1]['data_inicial'], 'ate':i[1]['data_final']},
                  sub_set=sub_set,
                  flag_escala=flag_escala['escala']
                  )

    print('Fim Script')

