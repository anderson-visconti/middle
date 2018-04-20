import os
import pandas as pd
import glob
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Category20
from bokeh.models import HoverTool, CrosshairTool
from bokeh.models import ColumnDataSource

path = os.path.dirname(os.path.realpath(__file__))
arquivos = glob.glob(os.path.join(path, '*.csv'))
df_previsao = pd.DataFrame()

for i, arquivo in enumerate(arquivos):
    ano = os.path.basename(arquivo)[6:10]
    df = pd.read_csv(filepath_or_buffer=arquivo, sep=';', skiprows=57, decimal=',')
    df['ano'] = int(ano)
    df_previsao = pd.concat([df_previsao, df])

df_previsao = df_previsao[df_previsao['Data'] != 'MEDIA']
df_previsao['Data'] = pd.to_datetime(df_previsao['Data'], dayfirst=True)
df_previsao['ENA_Percentual_MLT'] = df_previsao['ENA_Percentual_MLT'] / 100
df_previsao = df_previsao[df_previsao['Nome'] == 'SUDESTE']
df_previsao = df_previsao[df_previsao['Tipo'] == 'Submercado']
df_previsao['ano'] = df_previsao['ano'].apply(lambda x: str(x))
df_plot = df_previsao[['Data', 'Nome', 'ENA_MWmes', 'ano']]
df_plot = df_plot.pivot(index='Data', columns='ano', values='ENA_MWmes')
source = ColumnDataSource(df_plot)

output_file("line.html")
p = figure(x_axis_type='datetime', sizing_mode='scale_height')

for i, coluna in enumerate(df_plot):
    p.line(
        x='Data',
        y=coluna,
        source=source,
        line_color=Category20[20][i],
        legend=coluna
    )

show(p)

'''
hover = HoverTool(
    tooltips=[
        ('data', '$sx{%F}'),
        ('ENA', '$y{0,0.0}'),
    ],
    mode='vline',
    formatters={'$sx': 'datetime', 'ENA': 'printf'}
)

cross_hair = CrosshairTool()
tools = [cross_hair, hover]

p = figure(x_axis_type='datetime', tools=tools, sizing_mode='scale_height')

# add a line renderer
xs = []
ys = []
cores = df_plot['ano'].unique().size

for j, ano in enumerate(df_plot['ano'].unique()):
    xs.append(df_plot.loc[df_plot['ano'] == ano, 'Data'])
    ys.append(df_plot.loc[df_plot['ano'] == ano, 'ENA_MWmes'])

p.multi_line(
    xs=xs,
    ys=ys,
    color=Category20[cores]
)
show(p)
'''