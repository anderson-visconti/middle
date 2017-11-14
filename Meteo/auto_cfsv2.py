#!/usr/bin/env python

# Informacoes de escala dos mapas
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
        levels = [5, 10, 20, 40, 60, 80, 100, 150, 200, 250, 300, 350, 400]  # Niveis para chuva
        cores = cores_ons

    if flag_escala == 's':
        levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]  # Niveis para chuva
        cores = cores_ons

    if flag_escala == 'cm':
        levels = [-250, -200, -150, -100, -75, -50,  -25, -10, 10, 25, 50, 75, 100, 150, 200, 250] # Niveis para climatologia
        cores = 'seismic_r'

    if flag_escala == 'cs':
        levels = [-100, -75, -50, -40, -30, -20, -10, 10, 20, 30, 40, 50, 75, 100] # Niveis para climatologia
        cores = 'seismic_r'

    if flag_escala == 'per':
        levels = [-100, -75, -50, -35, -25, -15, -5, 5, 15, 25, 35, 50, 75, 100]
        cores = 'seismic_r'

    return levels, cores

# Monta o mapa com as configuracoes desejadas
def make_map(lons, lats, paths, nomes, dados, periodo, flag_escala, precip_clima, lons_clima, lats_clima):
    x, y = np.meshgrid(lons, lats)
    '''#Interpolacao
    interpolacao = interp(datain=precip_clima, xin=lons_clima, yin=np.flipud(lats_clima), xout=x, yout=np.flipud(y))'''

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


    m.drawcountries()
    m.drawcoastlines(linewidth=0.5)
    m.drawrivers(linewidth=0.25)


    #  Desenha estados do Brasil
    shp = m.readshapefile(os.path.join(paths['shape_estados'], nomes['shape_estados']), 'states',
                          drawbounds=True, linewidth=0.5)

    xx, yy = m(x, y)
    levels, cores = config_ons(flag_escala=flag_escala['escala'])

    cs = plt.contourf(xx, yy, dados, levels=levels, colors=cores, extend='both', alpha=0.90)
    cbar = m.colorbar(cs, location='bottom', label='Preciptacao [mm]')
    cbar.set_ticks(levels)
    cbar.ax.tick_params(labelsize=8)
    s = '''Modelo cfsv2 - Rodada {}
    Periodo: {:%Y-%m-%d} a {:%Y-%m-%d}'''
    plt.title(s.format(nomes['chuva'][9:17], periodo['de'], periodo['ate']))

    #  Informacao da empresa
    im = plt.imread(fname=os.path.join(paths['logo'], nomes['nome_logo']))
    newax = fig.add_axes([0.59, 0.16, 0.2, 0.2], anchor='SE', zorder=+1)
    newax.imshow(im, alpha=0.8)
    newax.axis('off')

    plt.savefig(os.path.join(paths['export'], '1_{}_{:%Y-%m-%d}_{:%Y-%m-%d}.png'.format(nomes['chuva'][0:19], periodo['de'], periodo['ate'])), bbox_inches='tight')

    # Retornar os tres tipos de mapas
    plt.close("all")
    print('Encerramento da criacao do mapa')
    return fig

# Monta o mapa
def anomalia(lons, lats, paths, nomes, dados, periodo, flag_escala, precip_clima, lons_clima, lats_clima):
    x, y = np.meshgrid(lons, lats)

    interpolacao = interp(datain=precip_clima, xin=lons_clima, yin=np.flipud(lats_clima), xout=x, yout=np.flipud(y))
    anomalia = (dados - interpolacao)

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
    m.drawcountries()
    m.drawcoastlines(linewidth=0.5)
    m.drawrivers(linewidth=0.25)

    #  Desenha estados do Brasil
    shp = m.readshapefile(os.path.join(paths['shape_estados'], nomes['shape_estados']), 'states',
                          drawbounds=True, linewidth=0.5)

    xx, yy = m(x, y)
    levels, cores = config_ons(flag_escala['escala_clima'])
    cs = plt.contourf(xx, yy, anomalia, levels=levels, cmap='bwr_r', extend='both', alpha=0.90)

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

    plt.savefig(os.path.join(paths['export'], '2_Anomalia_{}_{:%Y-%m-%d}_{:%Y-%m-%d}.png'.format(nomes['chuva'][0:19],
                                                                                                 periodo['de'],
                                                                                                 periodo['ate']
                                                                                                 )),
                bbox_inches='tight')
    # Retornar os tres tipos de mapas
    plt.close("all")
    print('Encerramento da criacao do mapa')
    return fig

# Faz um looping dos mapas Mensal e Semanal
def loop_mapa(paths, nomes, variaveis, periodo, sub_set, flag_escala):
    from netCDF4 import Dataset, num2date
    import os
    import numpy as np
    import pandas as pd

    for i in periodo.keys():
        periodo[i] = pd.to_datetime(periodo[i])


    # Abre arquivos Netcdf
    file_chuva = Dataset(os.path.join(paths['chuva'], nomes['chuva']), 'r')
    file_clima = Dataset(os.path.join(paths['climatologia'], nomes['climatologia']), 'r')


    #  Dados chuva
    lons = file_chuva.variables[variaveis['cfsv2'].get('lon')][:]
    lats = file_chuva.variables[variaveis['cfsv2'].get('lat')][:]
    times = num2date(file_chuva.variables[variaveis['cfsv2'].get('time')][:],
                    file_chuva.variables[variaveis['cfsv2'].get('time')].units)

    #  Dados Climatologia
    lons_clima = file_clima.variables[variaveis['climatologia'].get('lon')][:]
    lats_clima = file_clima.variables[variaveis['climatologia'].get('lat')][:]
    times_clima = num2date(times=file_clima.variables[variaveis['climatologia'].get('time')][:],
                     units=file_clima.variables[variaveis['climatologia'].get('time')].units,
                     calendar='julian')

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
    precip_chuva = file_chuva.variables[variaveis['cfsv2'].get('precip')][times_inds, lats_inds, lons_inds] * 21600
    precip_clima = file_clima.variables[variaveis['clima'].get('precip')]
    p = np.zeros((lats_inds_clima.shape[0], lons_inds_clima.shape[0]))

    #  Cria figura
    for i in pd.date_range(start=data_ini, end=data_fim, freq='D'):
        aux = precip_clima[i.month - 1, lats_inds_clima, lons_inds_clima]
        p = np.sum([p, aux], axis=0)


    fig_cfs = make_map(lons=lons, lats=lats, paths=paths, nomes=nomes, dados=precip_chuva.sum(axis=0), periodo=periodo,
                   flag_escala=flag_escala, precip_clima=p, lons_clima=lons_clima, lats_clima=lats_clima)

    fig_anomalia = anomalia(lons=lons, lats=lats, paths=paths, nomes=nomes, dados=precip_chuva.sum(axis=0), periodo=periodo,
                   flag_escala=flag_escala, precip_clima=p, lons_clima=lons_clima, lats_clima=lats_clima)

    return

# Cria as pastas onde salvar os arquivos e imagens
def pastas():
    dia = r'/home/middle/scripts-meteo/cfsv2/{:%Y%m%d}00'.format(datetime.now())
    mes = r'/home/middle/scripts-meteo/cfsv2/{:%Y%m%d}00/Mensal'.format(datetime.now())
    semana = r'/home/middle/scripts-meteo/cfsv2/{:%Y%m%d}00/Semanal'.format(datetime.now())
    if not os.path.exists(dia) == True:
        pasta_diaria = os.mkdir(dia)
    if not os.path.exists(mes) == True:
        pasta_Mensal = os.mkdir(mes)
    if not os.path.exists(semana) == True:
        pasta_Semanal = os.mkdir(semana)

# Cria os mapas Mensais
def mensal():
    from datetime import datetime
    import pandas as pd

    paths = {'chuva': r'/home/middle/scripts-meteo/cfsv2/netcdf',
             'climatologia': r'/home/middle/scripts-meteo/config/precip',
             'export': r'/home/middle/scripts-meteo/cfsv2/{:%Y%m%d}00/Mensal'.format(
                 datetime.now()),
             'shape_estados': r'/home/middle/scripts-meteo/config/shapefile',
             'logo': r'/home/middle/scripts-meteo/config/logo'
             }

    variaveis = {'cfsv2': {'lon': 'lon',
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

    nomes = {'chuva': r'prate.02.{:%Y%m%d}00.daily.nc'.format(datetime.now()),
             'climatologia': r'precip.mon.ltm.nc',
             'shape_estados': r'BRA_adm1',
             'nome_logo': 'Logo.png'}

    # unit - 'd' para dias e 'MS' para meses
    step = {'n_periodos': 4,
            'step': 1,
            'unit': 'MS'
            }

    #  's' - escala semanal,
    #  'm' - escala mensal,
    #  'cm' - climatologia mensal,
    #  'cs' - climatologia semanal.
    flag_escala = {'escala': 'm',
                   'escala_clima': 'cm'}

    sub_set = {'lon': [285, 330],
               'lat': [-35.0, 5.5]
               }
    data_inicial = '{:%Y-%m}-01'.format(datetime.now())
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
                  flag_escala=flag_escala
                  )

# Cria os mapas semanais
def semanal():
    from datetime import datetime
    import pandas as pd

    paths = {'chuva': r'/home/middle/scripts-meteo/cfsv2/netcdf',
             'climatologia': r'/home/middle/scripts-meteo/config/precip',
             'export': r'/home/middle/scripts-meteo/cfsv2/{:%Y%m%d}00/Semanal'.format(
                 datetime.now()),
             'shape_estados': r'/home/middle/scripts-meteo/config/shapefile',
             'logo': r'/home/middle/scripts-meteo/config/logo'
             }

    variaveis = {'cfsv2': {'lon': 'lon',
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

    nomes = {'chuva': r'prate.02.{:%Y%m%d}00.daily.nc'.format(datetime.now()),
             'climatologia': r'precip.mon.ltm.nc',
             'shape_estados': r'BRA_adm1',
             'nome_logo': 'Logo.png'}

    # unit - 'd' para dias e 'MS' para meses
    step = {'n_periodos': 8,
            'step': 7,
            'unit': 'd'
            }

    #  's' - escala semanal,
    #  'm' - escala mensal,
    #  'cm' - climatologia mensal,
    #  'cs' - climatologia semanal.
    flag_escala = {'escala': 's',
                   'escala_clima': 'cs'}

    sub_set = {'lon': [285, 330],
               'lat': [-35.0, 5.5]
               }

    data_inicial = datetime.today()
    if data_inicial.weekday() == 5:        
        data_inicial = (data_inicial + timedelta(7))
        ate = data_inicial + timedelta(6)


    else:
        dif = 5 - data_inicial.weekday()
        data_inicial = (data_inicial + timedelta(dif))
        ate = data_inicial + timedelta(6)

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
                  flag_escala=flag_escala)

# Envia imagens para o email
def envia_email(de, para, men, sem):
    msg = MIMEMultipart()
    msg['From'] = de
    msg['To'] = ', '.join(para)
    msg['Subject'] = 'Projecao de chuva CFSv2 - {:%d/%m/%Y}'.format(datetime.now())

    figuras = glob.glob(os.path.join(men, '*.png'))
    figuras1 = glob.glob(os.path.join(sem, '*.png'))
    nomes = []

    for figs in figuras:
        with open(figs, 'rb') as f:
            mime = MIMEImage(f.read())
        file = os.path.basename(f.name)
        nomes.append(file)
        mime.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(mime)
        mime.add_header('Content-ID', '<{}>'.format(file))
    for figs in figuras1:
        with open(figs, 'rb') as f:
            mime = MIMEImage(f.read())
        file = os.path.basename(f.name)

        nomes.append(file)
        mime.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(mime)

        mime.add_header('Content-ID', '<{}>'.format(file))

    # HTML do corpo do email
    msgText = MIMEText('<body>'
                       '<a href="http://ec2-34-224-35-9.compute-1.amazonaws.com/cfsv2/">Visite nosso site.</a>'
                       '<table>'
                       '<th colspan = "4"><b><font size="6" color="red">Projecao Mensal</font></b></th>'
                       '<tr>'
                       '<br>'
                       '<td><img src="cid:{0}" width="95%"></td>'
                       '<td><img src="cid:{2}" width="95%"></td>'
                       '<td><img src="cid:{4}" width="95%"></td>'
                       '<td><img src="cid:{6}" width="95%"></td>'
                       '</tr>'
                       '<tr>'
                       '<td><img src="cid:{1}" width="95%"></td>'
                       '<td><img src="cid:{3}" width="95%"></td>'
                       '<td><img src="cid:{5}" width="95%"></td>'
                       '<td><img src="cid:{7}" width="95%"></td>'
                       '</tr>'
                       '<th colspan = "4"><b><font size="6" color="red">Projecao Semanal</font></b></th>'
                       '<tr>'
                       '<td><img src="cid:{8}" width="95%"></td>'
                       '<td><img src="cid:{10}" width="95%"></td>'
                       '<td><img src="cid:{12}" width="95%"></td>'
                       '<td><img src="cid:{14}" width="95%"></td>'
                       '</tr>'
                       '<tr>'
                       '<td><img src="cid:{9}" width="95%"></td>'
                       '<td><img src="cid:{11}" width="95%"></td>'
                       '<td><img src="cid:{13}" width="95%"></td>'
                       '<td><img src="cid:{15}" width="95%"></td>'
                       '</tr>'
                       '<tr>'
                       '<td><img src="cid:{16}" width="95%"></td>'
                       '<td><img src="cid:{18}" width="95%"></td>'
                       '<td><img src="cid:{20}" width="95%"></td>'
                       '<td><img src="cid:{22}" width="95%"></td>'
                       '</tr>'
                       '<tr>'
                       '<td><img src="cid:{17}" width="95%"></td>'
                       '<td><img src="cid:{19}" width="95%"></td>'
                       '<td><img src="cid:{21}" width="95%"></td>'
                       '<td><img src="cid:{23}" width="95%"></td>'
                       '</tr>'
                       '</table><br><br><br><br>'
                       '<p>E-mail enviado automaticamente. Qualquer erro, entrar em contato com '
                       'alessandra.marques@enexenergia.com.br</p>'
                       '</body>'.format(*nomes), 'html')

    msg.attach(msgText)
    raw = msg.as_string()
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login('multivac.gerenciador@gmail.com', '@brate01')
    smtp.sendmail(de, para, raw)
    smtp.quit()

# Converte o arquivo grib em netcdf
def converte():
    from datetime import datetime
    import urllib2
    import os
    path = r'/home/middle/scripts-meteo/cfsv2/netcdf'
    prate = 'prate.02.{:%Y%m%d}00.daily.grb2'.format(datetime.now())
    URLGRIB = r'http://ftpprd.ncep.noaa.gov/data/nccf/com/cfs/prod/cfs/cfs.{:%Y%m%d}/00/time_grib_02/prate.02.{:%Y%m%d}00.daily.grb2'.format(datetime.now(), datetime.now())
    f = urllib2.urlopen(URLGRIB)
    html = f.read()
    with open(os.path.join(path, prate), mode='wb') as code:
        code.write(html)

   
    os.chdir(path)
    os.system('cdo -f nc copy prate.02.{:%Y%m%d}00.daily.grb2 prate.02.{:%Y%m%d}00.daily.nc'.format(datetime.now(),datetime.now()))

#Funcao HTML estatico
def html(men, sem, caminho_base):

    figuras = glob.glob(os.path.join(men, '*.png'))
    figuras1 = glob.glob(os.path.join(sem, '*.png'))
    nome = []

    for f in figuras:
        nome.append(f)

    for f in figuras1:
        nome.append(f)

    f = open(caminho_base + r"/index.html", "w")
    f2 = open(caminho_base + r"/cfsv2_base.html", "r").read()

    
    f.write(f2.format(*nome))
    f.write("Rodada {:%Y-%m-%d} - Membro PRATE.02".format(datetime.now()))
    f.close()
    return

# Chama todas as funcoes
if __name__ == '__main__':
    import pandas as pd
    import urllib2
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import glob
    import smtplib
    import matplotlib.pyplot as plt
    import pandas as pd
    from datetime import datetime, timedelta
    from mpl_toolkits.basemap import Basemap
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from datetime import datetime
    from mpl_toolkits.basemap import Basemap, interp
    plt.switch_backend('agg')


    # Caminho onde esta salva as imagens
    men = r'/home/middle/scripts-meteo/cfsv2/{:%Y%m%d}00/Mensal'.format(datetime.now())
    sem = r'/home/middle/scripts-meteo/cfsv2/{:%Y%m%d}00/Semanal'.format(datetime.now())
    
    # Caminho do HTML base
    caminho_base = r'/home/middle/scripts-meteo'

    # Informacoes de email
    de = 'multivac.gerenciador@gmail.com'

    #para = ['alessandra.marques@enexenergia.com.br']

    '''para = ['alessandra.marques@enexenergia.com.br', 
            'anderson.visconti@enexenergia.com.br']'''

    para = ['alessandra.marques@enexenergia.com.br',
            'anderson.visconti@enexenergia.com.br',
            'andre.pagan@enexenergia.com.br',
            'rodolfo.cabral@enexenergia.com.br',
            'ramon.nunes@enexenergia.com.br',
            'albert.ramcke@enexenergia.com.br',
            'marques.landeira@gmail.com']

    print('....................................................Script comecou a rodar............................................')
    converte()
    print('Converteu')
    
    pastas()
    print('Criou as pastas')
    
    semanal()
    print('Terminou previsao semanal')
    
    mensal()
    print('Terminou previsao mensal')

    #html(men, sem, caminho_base)
    #print('Atualizou HTML')

    envia_email(de, para, men, sem)
    print('E-mail enviado')

    print('Fim Script')