#!/usr/bin/env python
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource, CategoricalColorMapper, NumeralTickFormatter, CustomJS, HoverTool
from bokeh.layouts import layout, widgetbox, row, column
from bokeh.models.widgets import Select, TextInput, RangeSlider, DataTable, TableColumn, NumberFormatter, Button
from bokeh.io import curdoc
import pandas as pd
import os
from os.path import dirname, join
from datetime import datetime

# Callbacks
def update():

    df_aux =  df_2.loc[
        ((df_2.loc[:, ('ena_p', 1)] >= controls[0].value[0]) & (df_2.loc[:, ('ena_p', 1)] <= controls[0].value[1])) &
        ((df_2.loc[:, ('ena_p', 2)] >= controls[1].value[0]) & (df_2.loc[:, ('ena_p', 2)] <= controls[1].value[1])) &
        ((df_2.loc[:, ('ena_p', 3)] >= controls[2].value[0]) & (df_2.loc[:, ('ena_p', 3)] <= controls[2].value[1])) &
        ((df_2.loc[:, ('ena_p', 4)] >= controls[3].value[0]) & (df_2.loc[:, ('ena_p', 4)] <= controls[3].value[1]))
    ]
    source.data = dict(
        x=df_aux.loc[:, ('ena_p', 1)],
        y=df_aux.loc[:, ('ena_p', 2)],
        label=df_aux.loc[:, 'bins_text'],
        preco_se=df_aux.loc[:, ('preco', 1)],
        preco_s=df_aux.loc[:, ('preco', 2)],
        preco_ne=df_aux.loc[:, ('preco', 3)],
        preco_n=df_aux.loc[:, ('preco', 4)],
        ena_se_p=df_aux.loc[:, ('ena_p', 1)],
        ena_s_p=df_aux.loc[:, ('ena_p', 2)],
        ena_ne_p=df_aux.loc[:, ('ena_p', 3)],
        ena_n_p=df_aux.loc[:, ('ena_p', 4)],
        ena_se=df_aux.loc[:, ('ena', 1)],
        ena_s=df_aux.loc[:, ('ena', 2)],
        ena_ne=df_aux.loc[:, ('ena', 3)],
        ena_n=df_aux.loc[:, ('ena', 4)],
        cenario=df_aux.index
    )
    return


t = datetime.now()
path = r'C:\Onedrive\Middle Office\Middle\Decks\gevazp\2018\01\201802\export_1'
path_mlt = r'C:\Onedrive\Middle Office\Middle\Decks\gevazp\2018\01\201802/mlt.csv'
nome = r'resultados.csv'
nome_mlt = 'mlt.csv'
mes = 5
sub_ref = 1
sub_aux = 2
sub = {1:'SE', 2:'S', 3:'NE', 4:'N'}

df = pd.read_csv(
    filepath_or_buffer=open(join(dirname(__file__), nome)),
    sep=';',
    decimal=',',
)
mlt = pd.read_csv(
    filepath_or_buffer=open(join(dirname(__file__), nome_mlt)),
    sep=';',
    decimal=',',
    index_col=['mes'],
)

mlt = mlt.rename(columns={'1':1, '2':2, '3':3, '4':4})

df['mlt'] = df.apply(lambda x: mlt.loc[mes, x['submercado']], axis=1)
df['ena_p'] = df.apply(lambda x: x['ena'] / mlt.loc[mes, x['submercado']], axis=1)

df_2 = pd.pivot_table(data=df, values=['preco', 'ena', 'mlt', 'ena_p'], index=['cenario'], columns=['submercado'])
df_2.sort_values(by=('preco', sub_ref), ascending=True, inplace=True)
df_2['bins'] = pd.cut(x=df_2.loc[:, ('preco', sub_ref)], bins=np.arange(0, 400, 20), include_lowest=True, right=False)
df_2['bins_text'] = df_2['bins'].astype(str)

# Montando modelo para plot
source = ColumnDataSource(dict(
    x=df_2.loc[:, ('ena_p', sub_ref)],
    y=df_2.loc[:, ('ena_p', sub_aux)],
    label=df_2.loc[:, 'bins_text'],
    preco_se=df_2.loc[:, ('preco', 1)],
    preco_s=df_2.loc[:, ('preco', 2)],
    preco_ne=df_2.loc[:, ('preco', 3)],
    preco_n=df_2.loc[:, ('preco', 4)],
    ena_se_p=df_2.loc[:, ('ena_p', 1)],
    ena_s_p=df_2.loc[:, ('ena_p', 2)],
    ena_ne_p=df_2.loc[:, ('ena_p', 3)],
    ena_n_p=df_2.loc[:, ('ena_p', 4)],
    ena_se=df_2.loc[:, ('ena', 1)],
    ena_s=df_2.loc[:, ('ena', 2)],
    ena_ne=df_2.loc[:, ('ena', 3)],
    ena_n=df_2.loc[:, ('ena', 4)],
    cenario=df_2.index
    )
)

# Mapeamento das cores por categorias
color_mapper = CategoricalColorMapper(
    factors=df_2['bins_text'].unique(),
    palette=Category20[20]
)

p = figure(
    title='Faixas de PLD {} Vs {} - Mes: {}'.format(sub[sub_ref], sub[sub_aux], mes),
    tools='save,pan,wheel_zoom,box_zoom,reset,crosshair,lasso_select',
    toolbar_location="above",
    sizing_mode='scale_width'
)

# Formatacao hovertool
hover = HoverTool(
    tooltips=[
        ("cenario", "@cenario"),
        ("SE", "@ena_se_p{0.0%} - @ena_se{0,0.0}"),
        ("SU", "@ena_s_p{0.0%} - @ena_s{0,0.0}"),
        ('NE', '@ena_ne_p{0.0%} - @ena_ne{0,0.0}'),
        ('NO', '@ena_n_p{0.0%} - @ena_n{0,0.0}'),
        ('preco', '@preco_se{0.00}')
    ]
)
p.add_tools(hover)

# Legenda dos eixos
p.xaxis.axis_label = 'ENA {} [MWm]'.format(sub[sub_ref])
p.yaxis.axis_label = 'ENA {} [MWm]'.format(sub[sub_aux])

# Formatacao eixos principal
p.xaxis[0].formatter = NumeralTickFormatter(format="0.0%")
p.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")

# Formatacao eixo secundario
p.ygrid.minor_grid_line_color = 'navy'
p.ygrid.minor_grid_line_alpha = 0.1
p.xgrid.minor_grid_line_color = 'navy'
p.xgrid.minor_grid_line_alpha = 0.1

p.circle(
    x='x',
    y='y',
    source=source,
    color={'field': 'label', 'transform': color_mapper},
    legend='label',
    size=8
)

# Criacao dos sliders
controls = []
for i in range(1, 5):
    slicer = RangeSlider(
        start=0,
        end=df_2.loc[:, ('ena_p', i)].max(),
        value=(
            df_2.loc[:, ('ena_p', i)].min(),
            df_2.loc[:, ('ena_p', i)].max()
        ),
        title='ENA {}'.format(sub[i]),
        step=0.01
    )
    controls.append(slicer)

# Construcao da tabela
df_table = pd.DataFrame(df_2.loc[:, 'ena_p'])

columns = [
    TableColumn(field='cenario', title='Cenario'),
    TableColumn(field='ena_se_p', title='ENA SE', formatter=NumberFormatter(format="0.0%")),
    TableColumn(field='ena_s_p', title='ENA S', formatter=NumberFormatter(format="0.0%")),
    TableColumn(field='ena_ne_p', title='ENA NE', formatter=NumberFormatter(format="0.0%")),
    TableColumn(field='ena_n_p', title='ENA N', formatter=NumberFormatter(format="0.0%")),
    TableColumn(field='preco_se', title='Preco [R$/MWh]', formatter=NumberFormatter(format="0,0.00")),
]
data_table = DataTable(
    source=source,
    columns=columns,
    sizing_mode='scale_width'
)


# Criacao botao de download
button = Button(label="Download", button_type="success")
inputs = widgetbox(*controls)
input_2 = widgetbox(button)
button.callback = CustomJS(args=dict(source=source),
                               code=open(join(dirname(__file__), 'download.js')).read())

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

# Criacao layout
l = layout([
    [inputs, input_2],
    [p, data_table],
    ],
    sizing_mode='scale_width',
)
curdoc().add_root(l)
output_file(r"C:/Users/anderson/Desktop/scatter.html")
print((datetime.now() - t).total_seconds())
show(l)
