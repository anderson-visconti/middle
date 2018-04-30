# !/usr/bin/env python
# -*- coding: utf-8 -*-
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly import tools
import pandas as pd
import os
from datetime import datetime
import locale
import numpy as np

# localiza nomes dos meses em pt br
locale.setlocale(locale.LC_ALL, '')

df_completo = pd.read_excel(
    io=os.path.join(os.path.dirname(__file__), 'bbce_negociacoes.xlsx'),
    header=None,
    skiprows=1,
    names=['produto', 'tempo', 'mwh', 'mwm', 'preco', 'flag']
)

# arrumação dos dados
df_completo['tempo'] = pd.to_datetime(df_completo['tempo'], dayfirst=True)
df_completo['flag'] = df_completo['flag'].str.slice(0, 1)
df_completo['submercado'] = df_completo['produto'].str.slice(0, 2)
df_completo['tipo_energia'] =  df_completo['produto'].str.slice(3, 6)
df_completo['tipo_energia'] =  df_completo['tipo_energia'].str.strip()

df_completo['tipo_periodo'] = df_completo['produto'].str.slice(6, 10)
df_completo['tipo_periodo'] = df_completo['tipo_periodo'].str.strip()
df_completo['produto'] = df_completo['produto'].str.upper()
df_completo.sort_values(by=['submercado', 'tipo_energia', 'tipo_periodo'])
df_completo['financeiro'] = df_completo['preco'] * df_completo['mwm']

# remoção das operações canceladas
df_completo = df_completo.loc[df_completo['flag'] == 'N']

produtos = df_completo['produto'].unique()
# criação da instancia dash


# Auth
VALID_USERNAME_PASSWORD_PAIRS = [
    ['anderson.visconti', 'Abrate01']
]
app = dash.Dash(__name__)
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# layout
app.layout = html.Div([
    # dropdown menus
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='produto',
                options=[{'label': i, 'value': i} for i in produtos],
                value='SE CON MEN {:%b/%y} - Preço Fixo'.format(datetime.now()).upper()
            ),
        ],
            style={'width': '50%', 'display': 'inline-block', 'float': 'left'}
        ),

        html.Div([
            dcc.Dropdown(
                id='discretizacao',
                options=[
                    {'label': '3 h', 'value': '3H'},
                    {'label': '1 D', 'value': '1D'},
                    {'label': '2 D', 'value': '2D'},
                    {'label': '1 S', 'value': '7D'},
                    {'label': '1 M', 'value': '1M'}
                ],
                value='1D'
            )

        ],
            style={'width': '10%', 'display': 'inline-block', 'float': 'center'}),

        # N desvios
        html.Div([
            dcc.Dropdown(
                id='dp',
                options=[
                    {'label': '1 D.P', 'value': 1},
                    {'label': '2 D.P', 'value': 2},
                    {'label': '3 D.P', 'value': 3}
                ],
                value=2
            )
        ],
            style={'width': '10%', 'display': 'inline-block', 'float': 'center'}),

        # Media movel e Bollinger bandas
        html.Div([
            dcc.Dropdown(
                id='media_movel',
                options=[
                    {'label': 'MM20', 'value': 20},
                    {'label': 'MM12', 'value': 12},
                    {'label': 'MM8', 'value': 8},
                    {'label': 'MM5', 'value': 5},
                    {'label': 'MM3', 'value': 3},
                ],
                value=20
            )
        ],
            style={'width': '10%', 'display': 'inline-block', 'float': 'center'})

    ]),

    # selecao de datas
    html.Div([
        dcc.DatePickerRange(
            id='date_picker',
            start_date=df_completo['tempo'].min(),
            end_date=datetime.today(),
            display_format= 'DD-MM-YYYY',
            with_portal=False
        ),

    ],
            style={'width': '50%', 'height': '5%', 'display': 'inline-block', 'float':'center'}
    ),

    # grafico
    html.Div([
        dcc.Graph(
            id='bbce'
        )
    ]),

])

@app.callback(
    dash.dependencies.Output('date_picker', 'start_date'),
    [dash.dependencies.Input('produto', 'value')]
)
def update_data_inicial(produto):
    return df_completo.loc[df_completo['produto'] == produto, 'tempo'].min()

@app.callback(
    dash.dependencies.Output('date_picker', 'end_date'),
    [dash.dependencies.Input('produto', 'value')]
)
def update_data_inicial(produto):
    return df_completo.loc[df_completo['produto'] == produto, 'tempo'].max()

@app.callback(
    dash.dependencies.Output('bbce', 'figure'),
    [
        dash.dependencies.Input('produto', 'value'),
        dash.dependencies.Input('discretizacao', 'value'),
        dash.dependencies.Input('date_picker', 'start_date'),
        dash.dependencies.Input('date_picker', 'end_date'),
        dash.dependencies.Input('dp', 'value'),
        dash.dependencies.Input('media_movel', 'value')
    ])
def update_figure(produto, discretizacao, start_date, end_date, dp, media_movel):
    aggregation = {
        'preco': {
            'preco_medio': 'mean',
            'preco_max': 'max',
            'preco_min': 'min',
            'preco_vol': 'std'
        },
        'mwm': {
            'mwm_soma': 'sum'
        },
        'financeiro': {
            'financeiro_soma': 'sum'
        }
    }

    df_filtrado = pd.DataFrame(df_completo.loc[df_completo['produto'] == produto, :])
    df_filtrado = df_filtrado.resample(rule=discretizacao, on='tempo').agg(aggregation)
    df_filtrado.columns = df_filtrado.columns.droplevel(level=0)

    # remoção dos finais de semana
    df_filtrado = df_filtrado.loc[df_filtrado.index.dayofweek < 5, :]

    # filtro de data
    df_filtrado = df_filtrado.loc[start_date:end_date]

    # preco medio ponderado
    df_filtrado['preco_medio'] = df_filtrado['financeiro_soma'] / df_filtrado['mwm_soma']

    # criacao da MM e bollinger bands
    df_filtrado['media_movel'] = \
        df_filtrado['preco_medio'].rolling(
            min_periods=1,
            center=False,
            window=media_movel
        ).mean()

    df_filtrado['media_movel_c'] = \
        df_filtrado['preco_medio'].rolling(
            min_periods=1,
            center=True,
            window=media_movel
        ).mean()

    df_filtrado['vol_p'] = df_filtrado['preco_medio'] + \
                           dp * df_filtrado['preco_vol'].rolling(
        min_periods=1,
        center=False,
        window=media_movel
    ).std()

    df_filtrado['vol_n'] = df_filtrado['preco_medio'] - \
                           dp * df_filtrado['preco_vol'].rolling(
        min_periods=1,
        center=False,
        window=media_movel
    ).std()

    df_filtrado['mm_volume'] = df_filtrado['mwm_soma'].rolling(
        min_periods=1,
        center=False,
        window=media_movel
    ).mean()

    df_filtrado.to_csv(
        path_or_buf=os.path.join(os.path.dirname(__file__), 'export.csv'),
        decimal=',',
        sep=';'
    )

    # Criacao dos tracos
    trace_preco_medio = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['preco_medio'],
        name='Preco Medio',
        mode='lines+markers',
        connectgaps=False,
        line=dict(
            color='#3498DB',
            width=3.5,
        )
    )

    trace_preco_vol_p = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['vol_p'],
        name='{}*Vol+'.format(dp),
        legendgroup='Vol',
        mode='lines',
        connectgaps=False,
        line=dict(
            dash='dot',
            width=1.75,
            color='#117A65'
        )
    )

    trace_preco_vol_n = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['vol_n'],
        name='{}*Vol-'.format(dp),
        legendgroup='Vol',
        mode='lines',
        connectgaps=False,
        line=dict(
            dash='dot',
            width=1.75,
            color='#117A65'
        )
    )

    trace_media_movel = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['media_movel'],
        name='MM{}'.format(media_movel),
        mode='lines',
        connectgaps=False,
        line=dict(
            dash='line',
            width=1.75,
            color='#FF00CC'
        )
    )

    trace_volume = go.Bar(
        x=df_filtrado.index,
        y=df_filtrado['mwm_soma'],
        name='Volume',
        marker=dict(
            color='#E74C3C'
        )
    )

    trace_media_movel_volume = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['mm_volume'],
        name='MM{} - Volume'.format(media_movel),
        mode='lines',
        connectgaps=False,
        line=dict(
            width=1.75,
            color='#F4D03F'
        )
    )

    fig = tools.make_subplots(
        rows=2, cols=1,
        shared_xaxes=True
    )
    fig.append_trace(trace_preco_medio, 1, 1)
    fig.append_trace(trace_preco_vol_p, 1, 1)
    fig.append_trace(trace_preco_vol_n, 1, 1)
    fig.append_trace(trace_media_movel, 1, 1)
    fig.append_trace(trace_volume, 2, 1)
    fig.append_trace(trace_media_movel_volume, 2, 1)

    # Definicao do layout da figura
    fig['layout'].update(
        title = produto,
        autosize = True,
        legend = dict(
            orientation='v',
            font=dict(
                size=10
            )
        ),
        yaxis1=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True,
            title='R$/MWh',
            titlefont=dict(
                size=12
            ),
            domain=[0.25, 1.0],
            hoverformat='.2f'
        ),
        xaxis1=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True,
            domain=[0, 1.0],

        ),
        yaxis2=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True,
            title='MWmedio',
            titlefont=dict(
                size=12
            ),
            domain=[0.0, 0.20],
            hoverformat='.2f'
        ),
        xaxis2=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True,
            domain=[0, 1.0],

        )
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
