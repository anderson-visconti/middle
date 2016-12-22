#!/usr/bin/env python
# -*- coding: latin-1 -*-
from netCDF4 import Dataset, num2date, MFDataset
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
from datetime import date, timedelta, datetime
from calendar import  monthrange
import shapefile

# --- variaveis --------------------------------------------------------------------------------------------------------
path_file = r'C:\Users\anderson.visconti\Desktop\netcdf'    # caminho
path_export = r'C:\Users\anderson.visconti\Desktop\export\2016121800'
path_shape = r'D:\Middle Office\Middle\Hidrologia\ShapeFiles\Rio_Parana'
nome_arquivo = [ r'prate.01.2016121800.daily.nc',
                ]                         # nome do arquivo
nome_arquivo_normais = r'precip.mon.ltm_enhanced.nc'
nomes_shape = ['Bacia6']
'teste b4444'
sub_set = {'lat': [-35, 12],
           'lon': [275, 330]
           }                                         # pontos de lat e long a serem capturados

range_data = ['2017-01-21', '2017-01-28']  # range de datas para somatorio da preciptacao - limite inferior e <
range_escala = {'inf': 0,
                'sup': 500,
                'step': 10
                }                           # Range para escala do mapa de acumulado de chuva

range_anomalia = {'inf': -200,
                'sup': 225,
                'step': 25
                }                                   # Range para escala do mapa de anomalia

empresa = 'Enex Energia'
epoch = datetime(1970, 1, 1)                        # data de referencia dados
epoch_normal = datetime(1800, 1, 1)                 # data de referencia dados normais
# ----------------------------------------------------------------------------------------------------------------------
datas = [datetime.strptime(range_data[0], '%Y-%m-%d'),
         datetime.strptime(range_data[1], '%Y-%m-%d')
         ]  # vetor com os limites das datas

segundos = [(datas[0] - epoch).total_seconds(),
            (datas[1] - epoch).total_seconds()
            ]

horas = [(datas[0] - epoch_normal).total_seconds() / 3600,
            (datas[1] - epoch_normal).total_seconds() / 3600
            ]
full_path = []
for i in range(0, len(nome_arquivo)):   # cria vetores de caminhos completos
    full_path.append(os.path.join(path_file, nome_arquivo[i]))

full_path_normais = os.path.join(path_file, nome_arquivo_normais)
file = MFDataset(full_path)  # abre todos os arquivos
file_normais = Dataset(full_path_normais, mode='r')                                     # abre arquivo netcdf com normais de preciptacao
path_shape = os.path.join(path_shape, nomes_shape[0])
# ---- Dados chuva -----------------------------------------------------------------------------------------------------
lons = file.variables['longitude'][:]                                   # array com longitude
lats = file.variables['latitude'][:]                                    # array com latitude
temps = file.variables['time'][:]                                       # array com tempo
prates = file.variables['PRATE_surface'][:]                             # array com taxa de preciptacao
data_ref = file.variables['time'].reference_date
data_ref = datetime.strptime(file.variables['time'].reference_date, '%Y.%m.%d %H:%M:%S UTC')
# ----------------------------------------------------------------------------------------------------------------------

# --- Dados normais de chuva -------------------------------------------------------------------------------------------
lons_normais = file_normais.variables['lon'][:]
lats_normais = file_normais.variables['lat'][:]
precip_normais = file_normais.variables['precip'][:]
temps_normais = file_normais.variables['time'][:]
# ------ Captura subset dos dados --------------------------------------------------------------------------------------
lat_inds = np.where((lats >= sub_set['lat'][0]) & (lats <= sub_set['lat'][1]))
lon_inds = np.where((lons >= sub_set['lon'][0]) & (lons <= sub_set['lon'][1]))
temp_inds = np.where((temps >= segundos[0]) & (temps < segundos[1]))

lat_inds_normais = np.where((lats_normais >= sub_set['lat'][0]) & (lats_normais <= sub_set['lat'][1]))
lon_inds_normais = np.where((lons_normais >= sub_set['lon'][0]) & (lons_normais <= sub_set['lon'][1]))
temp_inds_normais = datas[0].month - 1
# ----------------------------------------------------------------------------------------------------------------------

# --- Recorta data set lat/lon -----------------------------------------------------------------------------------------
lons_subset = file.variables['longitude'][lon_inds[0]]
lats_subset = file.variables['latitude'][lat_inds[0]]
prate_subset = file.variables['PRATE_surface'][temp_inds[0], lat_inds[0], lon_inds[0]]

lons_subset_normais = file_normais['lon'][lon_inds_normais[0]]
lats_subset_normais = file_normais['lat'][lat_inds_normais[0]]
precip_subset_normais = (datas[1] - datas[0]).days * file_normais['precip'][temp_inds_normais, lat_inds_normais[0], lon_inds_normais[0]]
#precip_subset_normais = (monthrange(datas[0].year, datas[0].month)[1]) * file_normais['precip'][temp_inds_normais, lat_inds_normais[0], lon_inds_normais[0]]
# ----------------------------------------------------------------------------------------------------------------------

# --- Calcula Anomalia -------------------------------------------------------------------------------------------------
prate_subset_soma = 21600 * prate_subset.sum(axis=0)
#export = open(os.path.join(path_export, 'export.txt'),'w')

for lat in range(0, lats_subset.shape[0]):  # itera sobre lats do subset de dados de chuva
    dist_lat = np.abs(lats_subset_normais - lats_subset[lat])
    menor_lat = np.argmin(dist_lat)

    for lon in range(0, lons_subset.shape[0]):  # itera sobre lons do array de chuva
        dist_lon = np.abs(lons_subset_normais - lons_subset[lon])
        menor_lon = np.argmin(dist_lon)
        prate_subset_soma[lat, lon] = prate_subset_soma[lat, lon] - precip_subset_normais[menor_lat, menor_lon]
# ----------------------------------------------------------------------------------------------------------------------
fig = plt.figure(frameon=True)
# --- Estrutura do mapa de acumulado -----------------------------------------------------------------------------------

mapa = Basemap(llcrnrlon=lons_subset[0],
               llcrnrlat=lats_subset[0],
               urcrnrlon=lons_subset[lons_subset.size - 1],
               urcrnrlat=lats_subset[lats_subset.size - 1],
               projection='mill',
               lon_0=0.5 * (lons_subset[0] + lons_subset[lons_subset.size - 1]),
               lat_0=0.5 * (abs(lats_subset[0]) + abs(lats_subset[lats_subset.size - 1])),
               resolution='c'
               )

mapa.drawcoastlines(linewidth=1.50)
mapa.drawcountries(linewidth=1.50)
mapa.drawstates()
lons, lats = np.meshgrid(lons_subset, lats_subset)
x, y = mapa(lons, lats)
clevs = np.arange(range_escala['inf'], range_escala['sup'], range_escala['step'])
cs = mapa.contourf(x, y, 21600 * prate_subset.sum(axis=0), clevs, cmap='Paired', extend="both")
cbar = mapa.colorbar(cs, location='bottom', pad="5.0%")
cbar.set_label('Preciptacao [mm]')
plt.suptitle('{0} - Modelo CFS - Rod:{3:%Y-%m-%d %HZ}\n'
         '{1} 00Z - {2} 00Z'.format(empresa, datas[0].__format__('%d/%m/%Y'), datas[1].__format__('%d/%m/%Y'), data_ref),
             fontweight='bold', fontsize=10)

fig.savefig('{0}\{1:%Y%m%d%H%M}-{2:%Y-%m-%d}-{3:%Y-%m-%d}'.format(path_export, data_ref, datas[0], datas[1]),
            bbox_inches='tight')

# ----------------------------------------------------------------------------------------------------------------------

# ---- estrutura do mapa de anomalia -----------------------------------------------------------------------------------
fig = plt.figure(frameon=True)
mapa_anomalia = Basemap(llcrnrlon=lons_subset_normais[0],
               llcrnrlat=lats_subset_normais[lats_subset_normais.size - 1],
               urcrnrlon=lons_subset_normais[lons_subset_normais.size - 1],
               urcrnrlat=lats_subset_normais[0],
               projection='mill',
               lon_0=0.5 * (lons_subset_normais[0] + lons_subset_normais[lons_subset_normais.size - 1]),
               lat_0=0.5 * (abs(lats_subset_normais[0]) + abs(lats_subset_normais[lats_subset_normais.size - 1])),
               resolution='c'
               )

mapa_anomalia.drawcoastlines(linewidth=1.50)
mapa_anomalia.drawcountries(linewidth=1.50)
mapa_anomalia.drawstates(linewidth=1.00)
lons_anomalia, lats_anomalia = np.meshgrid(lons_subset, lats_subset)
x_anomalia, y_anomalia = mapa_anomalia(lons_anomalia, lats_anomalia)
# ----------------------------------------------------------------------------------------------------------------------
clevs_anomalia = np.arange(range_anomalia['inf'], range_anomalia['sup'], range_anomalia['step'])
cs_anomalia = mapa_anomalia.contourf(x_anomalia, y_anomalia, prate_subset_soma, clevs_anomalia, cmap='bwr_r', extend="both")
cbar_anomalia = mapa_anomalia.colorbar(cs_anomalia, location='bottom', pad="5.0%")
cbar_anomalia.set_label('Anomalia de Preciptacao')
plt.suptitle('{0} - Modelo CFS - Rod:{3:%Y-%m-%d %HZ}\n'
          'Anomalia - {1} 00Z - {2} 00Z'.format(empresa, datas[0].__format__('%d/%m/%Y'), datas[1].__format__('%d/%m/%Y'), data_ref),
             fontweight='bold', fontsize=10
          )

fig.savefig('{0}\{1:%Y%m%d%H%M}-{2:%Y-%m-%d}-{3:%Y-%m-%d}-anomalia'.format(path_export, data_ref, datas[0], datas[1]),
            bbox_inches='tight')

print('Imagem salva em {0}'.format(path_export))

