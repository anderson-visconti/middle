#!/usr/bin/env python
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource, CategoricalColorMapper, NumeralTickFormatter, CustomJS, HoverTool, Label
from bokeh.models.widgets import Select, TextInput, RangeSlider, DataTable, TableColumn, NumberFormatter, Button
from bokeh.layouts import layout, widgetbox, row, column, Spacer
from bokeh.io import curdoc
import pandas as pd
import os
from os.path import dirname, join
from datetime import datetime

t = datetime.now()
path = r'C:\Onedrive\Middle Office\Middle\Decks\gevazp\2018\01\201802\export_1'
path_mlt = r'C:\Onedrive\Middle Office\Middle\Decks\gevazp\2018\01\201802/mlt.csv'
nome = r'resultados.csv'
nome_mlt = 'mlt.csv'
mes = 7
sub_ref = 1
sub_aux = 2
ena_partida = {
    'SE':0.78,
    'S':0.63,
    'NE':0.37,
    'N':0.79
}
arm_partida = {
    'SE': 0.414,
    'S': 0.627,
    'NE': 0.373,
    'N': 0.689
}
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
df_2['bins'] = pd.cut(x=df_2.loc[:, ('preco', sub_ref)], bins=np.arange(0, 600, 40), include_lowest=True, right=False)
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
    sizing_mode='stretch_both'
)

# Construcao histograma
hist, edges = np.histogram(df_2.loc[:, ('preco', 1)], density=False, bins=np.arange(0, 600, 40))
hist = hist / len(df_2.loc[:, ('preco', 1)])

hist_source = ColumnDataSource(dict(
    top=hist,
    left=edges[:-1],
    right=edges[1:],
    #text=df_2['bins_text'].unique()
))

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


# Mapeamento das cores por categorias
color_mapper = CategoricalColorMapper(
    factors=df_2['bins_text'].unique(),
    palette=Category20[20]
)

# Grafico scatter
p.circle(
    x='x',
    y='y',
    source=source,
    color={'field': 'label', 'transform': color_mapper},
    legend='label',
    size=8
)
# Informacao de partida
text_ena = Label(
    x=10,
    y=550,
    x_units='screen',
    y_units='screen',
    background_fill_color='#E74C3C',
    background_fill_alpha=0.85,
    text_baseline="middle",
    text_color='#F4F6F6',
    text='''ENA - SE: {SE:3.1%} S: {S:3.1%} NE: {NE:3.1%} N: {N:3.1%}'''.format(**ena_partida)
)
text_arm = Label(
    x=10,
    y=530,
    x_units='screen',
    y_units='screen',
    background_fill_color='#E74C3C',
    background_fill_alpha=0.85,
    text_baseline="middle",
    text_color='#F4F6F6',
    text='''ARM - SE: {SE:3.1%} S: {S:3.1%} NE: {NE:3.1%} N: {N:3.1%}'''.format(**arm_partida)
)

p.add_layout(text_ena)
p.add_layout(text_arm)

# Criacao histograma
p2 = figure(
    title='Histograma PLD {} Mes: {}'.format(sub[sub_ref], mes),
    tools='save,pan,wheel_zoom,box_zoom,reset,crosshair',
    toolbar_location="above",
    sizing_mode='scale_width',
    #y_range=(0, 1.0)
)

p2.quad(bottom=0, left='left', right='right', top='top', color="#3498DB", line_color="white", source=hist_source)
hist_hover = HoverTool(
    tooltips=[
        ('Classe', '[@left, @right['),
        ('Frequencia', '@top{0.0%}')
    ]
)
text_2 = Label(
    x=10,
    y=520,
    x_units='screen',
    y_units='screen',
    background_fill_color='#E74C3C',
    background_fill_alpha=0.85,
    text_baseline="middle",
    text_color='#F4F6F6',
    text='''
    Mediana: {:3.1f}
    Media: {:3.1f}
    p5: {:3.1f}
    p95: {:3.1f}
    '''.format(
        np.median(df_2.loc[:, ('preco', 1)]),
        np.mean(df_2.loc[:, ('preco', 1)]),
        np.percentile(df_2.loc[:, ('preco', 1)], 5.0),
        np.percentile(df_2.loc[:, ('preco', 1)], 95.0),
    )
)
p2.add_tools(hist_hover)
p2.add_layout(text_2)

# Formatacao eixos principal
p2.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")

# Formatacao eixo secundario
p2.ygrid.minor_grid_line_color = 'navy'
p2.ygrid.minor_grid_line_alpha = 0.1
p2.xgrid.minor_grid_line_color = 'navy'
p2.xgrid.minor_grid_line_alpha = 0.1

# Criacao dos objetos

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
        step=0.01,
        callback_policy='mouseup'
    )
    controls.append(slicer)

# Criacao botao de download
button = Button(label="Download", button_type="success")
inputs = widgetbox(*controls)
input_2 = widgetbox(button)
button.callback = CustomJS(
    args=dict(source=source),
    code=open(join(dirname(__file__), 'download.js')).read()
)

# Criacao layout do painel
l = layout([
    [inputs, input_2],
    [p, p2],
    [data_table, Spacer()],
    ],
    sizing_mode='scale_width',
)
#l = column(
#    row(inputs, input_2, sizing_mode='scale_width'),
#    row(p, p2, sizing_mode='scale_width'),
#    row(data_table, Spacer(), sizing_mode='scale_width'),
#    sizing_mode='scale_width'
#)
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

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

    # Construcao histograma
    hist, edges = np.histogram(df_aux.loc[:, ('preco', 1)], density=False, bins=np.arange(0, 600, 40))
    hist = hist / len(df_aux.loc[:, ('preco', 1)])

    hist_source.data = dict(
        top=hist,
        left=edges[:-1],
        right=edges[1:],
        # text=df_2['bins_text'].unique()
    )
    text_2.text = '''
    Mediana: {:3.1f}
    Media: {:3.1f}
    p5: {:3.1f}
    p95: {:3.1f}
    '''.format(
        np.median(df_aux.loc[:, ('preco', 1)]),
        np.mean(df_aux.loc[:, ('preco', 1)]),
        np.percentile(df_aux.loc[:, ('preco', 1)], 5.0),
        np.percentile(df_aux.loc[:, ('preco', 1)], 95.0),
    )
    return

curdoc().add_root(l)
output_file(r"C:/Users/anderson/Desktop/scatter.html")
print((datetime.now() - t).total_seconds())
show(l)
