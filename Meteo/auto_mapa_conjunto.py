#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
def importa_dados(full_path, cols):
    df_dados = pd.read_csv(filepath_or_buffer=full_path,
                           #colspecs=[(0, 6), (8, )]
                           delim_whitespace=True,
                           decimal='.',
                           names=cols
                           )

    df_dados['data'] = pd.to_datetime(full_path[-10:-4], format='%d%m%y') - pd.to_timedelta(arg=1, unit='D')

    df_dados.set_index(['data', 'lon', 'lat'], inplace=True)
    return df_dados

def make_map(dados, file_config, nome_modelo, datas):
    fig = plt.figure()
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
    cs = plt.contourf(xx, yy, precip.values, levels=levels, colors=cores_ons, extend='both')
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
    plt.close('all')
    return

def get_config_ons(flag='s'):
    if flag == 's':
        levels = [1, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]  # niveis para chuva

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

def Cria_pastas():
    # Cria as pastas onde salvar os arquivos
    if not os.path.exists(path['exportar']) == True:
        cria_pasta_figuras = os.mkdir(path['exportar'])

    if not os.path.exists(path['ETA']) == True:
        cria_pasta_ETA = os.mkdir(path['ETA'])

    if not os.path.exists(path['GESF']) == True:
        cria_pasta_GESF = os.mkdir(path['GESF'])

def Unzip(local_ETA, local_GESF):

    # ETA
    data1 = local_ETA.read()
    # Salva o arquivo
    with open(os.path.join(path['ETA'], file_ETA), mode='wb') as code:
        code.write(data1)
    # Unzip
    zip_ref1 = zipfile.ZipFile(os.path.join(path['ETA'], file_ETA), 'r')
    zip_ref1.extractall(path['ETA'])
    zip_ref1.close()

    # GESF
    data2 = local_GESF.read()
    # Salva o arquivo
    with open(os.path.join(path['GESF'], file_GESF), mode='wb') as code:
        code.write(data2)
    # Unzip
    zip_ref2 = zipfile.ZipFile(os.path.join(path['GESF'], file_GESF), 'r')
    zip_ref2.extractall(path['GESF'])
    zip_ref2.close()

def envia_email(de, para):
    msg = MIMEMultipart()
    msg['From'] = de
    msg['To'] = ', '.join(para)
    msg['Subject'] = 'Projecao de chuva GESF e ETA - {:%d/%m/%Y}'.format(datetime.now())

    figuras = glob.glob(os.path.join(file_config['path_export'], '*.png'))
    nomes = []
    for fig in figuras:
        with open(fig, 'rb') as f:
            mime = MIMEImage(f.read())
        file = os.path.basename(f.name)

        nomes.append(file)
        mime.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(mime)

        mime.add_header('Content-ID', '<{}>'.format(file))

        msg.attach(mime)

    msgText = MIMEText('<br><td><img src="cid:{}"><td><td><img src="cid:{}"><td><br><br><br><br>'
                       'E-mail enviado automaticamente. Qualquer erro, entrar em contato com '
                       'alessandra.marques@enexenergia.com.br'.format(*nomes), 'html')
    msg.attach(msgText)
    raw = msg.as_string()


    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login('multivac.gerenciador@gmail.com', '@brate01')
    smtp.sendmail(de, para, raw)
    smtp.quit()

if __name__ == '__main__':
    import pandas as pd
    import urllib2
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import glob
    import zipfile
    import os
    import smtplib
    from datetime import datetime, timedelta
    from mpl_toolkits.basemap import Basemap
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    plt.switch_backend('agg')
    # URL dos arquivos
    URLETA = r'https://agentes.ons.org.br/images/operacao_integrada/meteorologia/eta/Eta40_precipitacao10d.zip'
    URLGESF = r'https://agentes.ons.org.br/images/operacao_integrada/meteorologia/global/GEFS_precipitacao10d.zip'
    # Nome dos arquivos
    file_ETA = 'Eta40_precipitacao10d.zip'
    file_GESF = 'GEFS_precipitacao10d.zip'

    # Caminhos
    path = {'ETA':
                r'/home/middle/scripts-meteo/conjunto/eta/{:%Y%m%d}'.format(datetime.now()),
            'GESF':
                r'/home/middle/scripts-meteo/conjunto/gesf/{:%Y%m%d}'.format(datetime.now()),
            'exportar':
                r'/home/middle/scripts-meteo/conjunto/export/{:%Y%m%d}'.format(datetime.now())}
    hoje = datetime.today()
    if hoje.weekday() == 5:
        de = (hoje + timedelta(7))
        ate = de + timedelta(6)

    else:
        dif = 5 - hoje.weekday()
        de = (hoje + timedelta(dif))
        ate = de + timedelta(6)

    datas = {'data_inicial': hoje,
             'de': de,
             'ate': ate}

    # Funcao para criar pastas onde salvar as imagens
    Cria_pastas()

    # Unzip
    local_ETA = urllib2.urlopen(URLETA)
    local_GESF = urllib2.urlopen(URLGESF)
    Unzip(local_ETA, local_GESF)

    file_config = {'path_export':
                       r'/home/middle/scripts-meteo/conjunto/export/{:%Y%m%d}'.format(datetime.now()),
                   'path_logo':r'/home/middle/scripts-meteo/config/logo',
                   'nome_logo':r'Logo.png',
                   'path_shape_file':r'/home/middle/scripts-meteo/config/shapefile',
                   'nome_shape_file':r'BRA_adm1'
                   }

    for i in datas.keys():
        datas[i] = pd.to_datetime(datas[i])

    df_precip_eta = pd.DataFrame()
    df_precip_gesf = pd.DataFrame()
    df_dados_aux = pd.DataFrame()
    df_dados_gesf_aux = pd.DataFrame()

    #  Importa dados de chuva
    for i in path.keys():
        # lista arquivos
        files = glob.glob(os.path.join(path[i], '*.dat'))
        if i == 'ETA':
            for j in files:
                df_dados_aux = importa_dados(full_path=j, cols=['lon', 'lat', 'precip'])
                df_precip_eta = pd.concat(objs=[df_precip_eta, df_dados_aux])

        if i == 'GESF':
            for j in files:
                df_dados_gesf_aux = importa_dados(full_path=j, cols=['lon', 'lat', 'precip'])
                df_precip_gesf = pd.concat(objs=[df_precip_gesf, df_dados_gesf_aux])

    # Ordenando os indices
    df_precip_eta.sort_index(level=['data'], inplace=True)
    df_precip_gesf.sort_index(level=['data'], inplace=True)


    # Filtrando datas
    eta_slice = pd.DataFrame(df_precip_eta.loc[datas['de']:datas['ate']])
    gesf_slice = pd.DataFrame(df_precip_gesf.loc[datas['de']:datas['ate']])


    eta_soma = pd.DataFrame(eta_slice.groupby(by=['lon', 'lat']).sum())
    gesf_soma = pd.DataFrame(gesf_slice.groupby(by=['lon', 'lat']).sum())
    eta_soma.to_csv(os.path.join(file_config['path_export'], 'eta_soma.csv'), sep=';', decimal=',')
    eta_slice.to_csv(os.path.join(file_config['path_export'], 'eta_diario.csv'), sep=';', decimal=',')
    gesf_soma.to_csv(os.path.join(file_config['path_export'], 'gesf_soma.csv'), sep=';', decimal=',')
    gesf_slice.to_csv(os.path.join(file_config['path_export'], 'gesf_diario.csv'), sep=';', decimal=',')

    #  Criacao de figuras
    make_map(dados=gesf_soma, file_config=file_config, nome_modelo='GESF', datas=datas)
    make_map(dados=eta_soma, file_config=file_config, nome_modelo='ETA', datas=datas)

    ########### Enviar email com as figuras #####################

    de = 'multivac.gerenciador@gmail.com'
    #para = ['alessandra.marques@enexenergia.com.br']
    para = ['alessandra.marques@enexenergia.com.br',
            'albert.ramcke@enexenergia.com.br',
            'anderson.visconti@enexenergia.com.br',
            'andre.pagan@enexenergia.com.br',
            'rodolfo.cabral@enexenergia.com.br',
            'ramon.nunes@enexenergia.com.br',
            'karla.assuncao@enexenergia.com.br',
            'marques.landeira@gmail.com']

    envia_email(de, para)

    print('Fim do script')
    pass
