def filtra_valores(tipo, nome):
    df_plot = df_previsao[
        (df_previsao['Tipo'] == tipo)&
        (df_previsao['Nome'] == nome)
    ]

    df_plot = df_plot[['Data', 'Nome', 'ENA_MWmes', 'ano']]

    return df_plot

if __name__=='__main__':
    import os
    import pandas as pd
    import glob
    from math import pi
    import plotly
    from plotly import tools
    import plotly.plotly as py
    import plotly.graph_objs as go

    path = os.path.dirname(os.path.realpath(__file__))
    arquivos = glob.glob(os.path.join(path, '*.csv'))
    df_previsao = pd.DataFrame()

    for i, arquivo in enumerate(arquivos):
        ano = os.path.basename(arquivo)[6:10]
        df = pd.read_csv(filepath_or_buffer=arquivo, sep=';', skiprows=57, decimal=',')
        df['ano'] = int(ano)
        df_previsao = pd.concat([df_previsao, df])

    # Carregdamento de todos os dados
    df_previsao = df_previsao[df_previsao['Data'] != 'MEDIA']
    df_previsao['Data'] = pd.to_datetime(df_previsao['Data'], dayfirst=True)
    df_previsao['ENA_Percentual_MLT'] = df_previsao['ENA_Percentual_MLT'] / 100
    x=df_previsao['Tipo'].unique()

    fig = tools.make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            'Sudeste',
            'Sul',
            'Nordeste',
            'Norte'
        )
    )
    traces_submercado = []

    # Iterando sobre todos
    for j, submercado in enumerate(df_previsao.loc[df_previsao['Tipo'] == 'Submercado', 'Nome'].unique()):

        if submercado != 'SIN':
            df_plot = filtra_valores(tipo='Submercado', nome=submercado)
            traces = []

            # Itera sobre os anos
            for i, ano in enumerate(df_plot.loc[:,'ano'].unique()):
                traces = (
                    dict(
                        type='scatter',
                        x=df_plot.loc[df_plot['ano'] == ano, 'Data'],
                        y=df_plot.loc[df_plot['ano'] == ano, 'ENA_MWmes'],
                        mode='lines',
                        name=str(ano)
                    )
                )

                if submercado == 'SUDESTE':
                    fig.append_trace(traces, 1, 1)

                elif submercado == 'SUL':
                    fig.append_trace(traces, 1, 2)

                elif submercado == 'NORDESTE':
                    fig.append_trace(traces, 2, 1)

                elif submercado == 'NORTE':
                    fig.append_trace(traces, 2, 2)

    fig['layout'].update(showlegend=False, title='ENAS PLAN4_IA')
    plotly.offline.plot(fig, filename='cabeleira.html')
