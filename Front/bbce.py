# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.plotly as py
from plotly import tools
import pandas as pd
import os
from datetime import datetime
import locale

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

# remoção das operações canceladas
df_completo = df_completo.loc[df_completo['flag'] == 'N']

produtos = df_completo['produto'].unique()
aggregation = {
    'preco': {
        'preco_medio': 'mean',
        'preco_max': 'max',
        'preco_min': 'min',
    },
    'mwm': {
        'mwm_soma': 'sum'
    }
}

# criação da instancia dash
app = dash.Dash()

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
            style={'width': '30%', 'display': 'inline-block', 'float': 'left'}
        ),

        html.Div([
            dcc.Dropdown(
                id='discretizacao',
                options=[
                    {'label': '30 min', 'value': '30T'},
                    {'label': '1 h', 'value': '1H'},
                    {'label': '3 h', 'value': '3H'},
                    {'label': '1 D', 'value': '1D'},
                    {'label': '1 S', 'value': '7D'}
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
                    {'label': '1 DP', 'value': 1},
                    {'label': '2 DP', 'value': 2}
                ],
                value=2
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
            display_format= 'DD-MM-YYYY'
        ),
    ],
            style={'width': '30%', 'height': '5%', 'display': 'inline-block', 'float':'center'}
    ),

    # grafico
    html.Div([
        dcc.Graph(
            id='bbce'
        )
    ]),

])

@app.callback(
    dash.dependencies.Output('bbce', 'figure'),
    [
        dash.dependencies.Input('produto', 'value'),
        dash.dependencies.Input('discretizacao', 'value'),
        dash.dependencies.Input('date_picker', 'start_date'),
        dash.dependencies.Input('date_picker', 'end_date'),
        dash.dependencies.Input('dp', 'value')
    ])
def update_figure(produto, discretizacao, start_date, end_date, dp):
    aggregation = {
        'preco': {
            'preco_medio': 'mean',
            'preco_max': 'max',
            'preco_min': 'min',
            'preco_vol': 'std'
        },
        'mwm': {
            'mwm_soma': 'sum'
        }
    }

    df_filtrado = pd.DataFrame(df_completo.loc[df_completo['produto'] == produto, :])
    df_filtrado = df_filtrado.resample(rule=discretizacao, on='tempo').agg(aggregation)
    df_filtrado.columns = df_filtrado.columns.droplevel(level=0)

    # remoção dos finais de semana
    df_filtrado = df_filtrado.loc[df_filtrado.index.dayofweek < 5, :]

    # filtro de data
    df_filtrado = df_filtrado.loc[start_date:end_date]

    # Criacao dos tracos
    trace_preco_medio = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['preco_medio'],
        name='Preco Medio',
        mode='lines+markers',
        connectgaps=False,
        line=dict(
            color='#3498DB',
            width=3.0,
        )
    )

    trace_preco_max = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['preco_max'],
        name='Preco Max',
        mode='lines',
        connectgaps=False,
        line=dict(
            dash='dot',
            width=1.5,
            color='#117A65'
        )
    )

    trace_preco_min = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['preco_min'],
        name='Preco Min',
        mode='lines',
        connectgaps=False,
        line=dict(
            dash='dot',
            width=1.5,
            color='#117A65'
        )
    )

    trace_preco_vol_p = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['preco_medio'] + df_filtrado['preco_vol'] * dp,
        name='{}*Vol+'.format(dp),
        legendgroup='Vol',
        mode='lines',
        connectgaps=False,
        line=dict(
            dash='dot',
            width=1.5,
            color='#117A65'
        )
    )

    trace_preco_vol_n = go.Scatter(
        x=df_filtrado.index,
        y=df_filtrado['preco_medio'] - df_filtrado['preco_vol'] * dp,
        name='{}*Vol-'.format(dp),
        legendgroup='Vol',
        mode='lines',
        connectgaps=False,
        line=dict(
            dash='dot',
            width=1.5,
            color='#117A65'
        )
    )

    trace_volume = go.Bar(
        x=df_filtrado.index,
        y=df_filtrado['mwm_soma'],
        text=df_filtrado['mwm_soma'],
        textposition='auto',
        name='Volume Energia',
        marker=dict(
            color='#E74C3C'
        )
    )

    fig = tools.make_subplots(
        rows=2, cols=1,
        subplot_titles=('Precos', 'Volume'),
        shared_xaxes=True
    )

    #fig = dict(data=[trace_volume])
    fig.append_trace(trace_preco_medio, 1, 1)
    #fig.append_trace(trace_preco_max, 1, 1)
    #fig.append_trace(trace_preco_min, 1, 1)
    fig.append_trace(trace_preco_vol_p, 1, 1)
    fig.append_trace(trace_preco_vol_n, 1, 1)
    fig.append_trace(trace_volume, 2, 1)

    fig['layout'].update(
        #height=600,
        #width=1200,
        title = produto,
        autosize = True,
        legend = dict(
            orientation='v'
        ),
        yaxis1=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True
        ),
        xaxis1=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True
        ),
        yaxis2=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True
        ),
        xaxis2=dict(
            autotick=True,
            showgrid=True,
            showticklabels=True
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server(debug=True)
    pass
