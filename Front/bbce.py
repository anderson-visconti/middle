if __name__=='__main__':
    import os
    import pandas as pd
    import plotly.plotly as py
    import plotly.offline as offline
    import plotly.graph_objs as go
    from datetime import datetime
    offline.init_notebook_mode(connected=True)
    paths = {'path':r'C:\Users\ander\Desktop'
             }
    nomes = {'dados':r'ago.csv'
             }

    produto = {'inicial': '2017-08-01',
               'final': '2017-08-31'
               }
    file_dados = open(os.path.join(paths['path'], nomes['dados']), 'r')

    dados = []
    for linha in file_dados:

        if linha[0] == '-':
            data_produto = linha[4:14]

        else:
            dados_aux = linha.split(';')
            if dados_aux[1].find('.') >= 0:
                dados_aux[1] = dados_aux[1].replace('.', '')

            if dados_aux[1].find(',') >= 0:
                dados_aux[1] = dados_aux[1].replace(',', '.')

            if dados_aux[2].find(',') >= 0:
                dados_aux[2] = dados_aux[2].replace(',', '.')

            dados_aux[3] = dados_aux[3].replace('\n', '')
            dados_aux[3] = dados_aux[3].replace(',', '.')

            aux = {'data_completa': pd.to_datetime('{} {}'.format(data_produto, dados_aux[0]), format='%d/%m/%Y %H:%M'),
                   'produto_inicial': pd.to_datetime(produto['inicial']),
                   'produto_final': pd.to_datetime(produto['final']),
                   'horas_produto': float(dados_aux[1]),
                   'energia_media': float(dados_aux[2]),
                   'preco': float(dados_aux[3])
                   }
            dados.append(aux)

    df_dados = pd.DataFrame.from_dict(dados, orient='columns')
    #print df_dados
    inferior = df_dados['data_completa'].min()
    superior = df_dados['data_completa'].max()
    range_datas = pd.date_range(inferior, superior, freq='D')

    candle = []
    for i in range_datas:

        aux = df_dados.loc[(df_dados['data_completa'] >= i) &
                           (df_dados['data_completa'] < i + pd.to_timedelta(1, unit='D'))
        ]
        if aux.empty == False:
            dict_aux = {'data_completa': i,
                        'open': aux.loc[aux['data_completa'] == aux['data_completa'].min()]['preco'].values[0],
                        'high': aux['preco'].max(),
                        'low': aux['preco'].min(),
                        'close': aux.loc[aux['data_completa'] == aux['data_completa'].max()]['preco'].values[0]
                        }
            candle.append(dict_aux)

    #print candle

    candle = pd.DataFrame.from_dict(candle, orient='columns')
    candle = candle[['data_completa', 'open', 'high', 'low', 'close']]
    candle.set_index(keys=['data_completa'], inplace=True)
    trace = go.Candlestick(x=candle.index,
                           open=candle['open'],
                           high=candle['high'],
                           low=candle['low'],
                           close=candle['close'])
    data = [trace]
    layout = go.Layout(
        title='Contratos Fechados BBCE - Ago/2017',
        font=dict(
            size=16
        ),
        xaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            showline=True,
            autotick=True,
            showticklabels=True
        ),
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            showline=True,
            autotick=True,
            showticklabels=True,
            nticks=20,
            titlefont=dict(
                #family='Arial, sans-serif',
                size=8
            ),
            tickfont=dict(
                #family='Arial, sans-serif',
                size=12,
                color='black'
            )
        ),
        showlegend=False,
        updatemenus=list([
            dict(
                x=-0.05,
                y=1,
                yanchor='top',
                buttons=list([
                    dict(
                        args=['visible', [True]],
                        label='Agosto',
                        method='restyle'
                    )
                ])
            )
        ])
    )
    fig = dict(data=data)
    fig = go.Figure(data=data, layout=layout)
    offline.plot(fig, filename='bbce-agosto.html')
    pass


