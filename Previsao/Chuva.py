import pandas as pd
import numpy as np
from netCDF4 import Dataset, num2date, MFDataset
import os

path = r'C:\OneDrive\Middle Office\Middle\Hidrologia\Chuva-Vazao\Chuva'
nomes = {'variavel': 'cmorph','base': 'cmorph.3hr-025deg.', 'extensao':'.nc'}
nc_vars = {'chuva': 'cmorph_precip',
           'lat': 'lat',
           'lon': 'lon',
           'tempo': 'time'}

coords = {'lat':[-22, -20],
          'lon':[313.4, 316]}

tempos = {'t_inicial': '2016-12-10',
          't_final': '2016-12-10'}

temp = pd.date_range(start=tempos['t_inicial'], end=tempos['t_final'], freq='D', tz='UTC')
caminhos = []

for i in range(0, len(temp)):   # cria caminhos dos arquivos
    caminhos.append('{path}\{variavel}\{year}\{nome_base}{data_form}{extensao}'.format(
        path=path,
        variavel=nomes['variavel'],
        year=temp[i].year,
        nome_base=nomes['base'],
        data_form=temp[i].strftime('%Y%m%d'),
        extensao=nomes['extensao']))

file = MFDataset(caminhos)
lats = file.variables[nc_vars['lat']][:]  # pega latitutes
lons = file.variables[nc_vars['lon']][:]  # pega longitudes

# indices para recortar em lat/lon
lat_inds = np.where((lats >= coords['lat'][0]) & (lats <= coords['lat'][1]))
lon_inds = np.where((lons >= coords['lon'][0]) & (lons <= coords['lon'][1]))

# subset dos dados
sub_lats = lats[lat_inds[0]]
sub_lons = lons[lon_inds[0]]
sub_times =num2date (file.variables[nc_vars['tempo']][:], file.variables[nc_vars['tempo']].units)
precip = file.variables[nc_vars['chuva']][:, lat_inds[0], lon_inds[0]]
dados = []

for i in range(0, precip.shape[0]): # itera sobre o tempo
    for j in range(0, precip.shape[1]):  # itera sobre lat
        for k in range(0, precip.shape[2]):  # itera sobre lon
            dados.append([sub_times[i],
                          sub_lats[j],
                          sub_lons[k],
                          precip[i, j, k] * 3])
df_24h = pd.DataFrame()
df = pd.DataFrame(data=dados, columns=['data_3h', 'lat', 'lon', 'precip_3h'])
df_indexado = df.set_index(['data_3h', 'lat', 'lon'])
# calcula chuva acumulada em 24 h
df_24h = df_indexado.unstack(level=[1,2]).resample('D').sum().stack(level=[2,1]).swaplevel(1,2)

df_indexado.to_csv(r'C:\Users\anderson.visconti\Desktop\Nova pasta\chuva-3.csv')
df_24h.to_csv(r'C:\Users\anderson.visconti\Desktop\Nova pasta\chuva-24.csv')
pass


