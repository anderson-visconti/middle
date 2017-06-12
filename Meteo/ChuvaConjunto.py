def importa_dados(paths, nomes, data_inicial):
    import pandas as pd
    from datetime import datetime, timedelta
    import os

    data_inicial = datetime.strptime(data_inicial, '%d/%m/%Y')
    dados = pd.DataFrame()
    for path in paths.keys():  # itera sobre pastas
        i = 1
        if path not in  [r'pontos_grade', r'remocao_vies', r'remover', r'export']:
            for arquivos in os.listdir(paths[path]):  # itera sobre arquivos
                dados_temp = pd.read_fwf(filepath_or_buffer=r'{caminho}\{p1}{p2:%d%m%y}{p3}{p4:%d%m%y}{extensao}'.
                                         format(caminho=paths[path],
                                                p1=nomes[path][0],
                                                p2=data_inicial,
                                                p3=nomes[path][1],
                                                p4=data_inicial + timedelta(days=i),
                                                extensao=nomes[path][2]
                                                ),
                                         delim_whitespace=True,
                                         names=['lon', 'lat', 'precip']
                                         )

                dados_temp['data'] = data_inicial + timedelta(days=i)
                dados_temp['modelo'] = path
                dados = pd.concat([dados, dados_temp], axis=0)
                i = i + 1
    return dados


def importa_config(paths, sep, decimal):
    import pandas as pd

    df = pd.read_csv(filepath_or_buffer=paths, sep=sep, decimal=decimal
                                  )

    return df



    return


def remove_vies(df_dados, config_remocao, sub_bacia, df_grade_sub_bacia):
    import pandas as pd

    df_sub_bacia = pd.DataFrame()
    #  filtra subbacia
    for i in df_grade_sub_bacia.iterrows():
        df_aux  = pd.DataFrame(df_dados.loc[
                                   (df_dados.lon == float(i[1].lon)) &
                                   (df_dados.lat == float(i[1].lat)) &
                                   (df_dados.modelo == i[1].modelo)
                               ]
        )
        df_sub_bacia = pd.concat([df_sub_bacia, df_aux])

    # valor medio dos 10 dias
    media_diaria = []
    for i in df_sub_bacia.data.unique():
        media_diaria_aux = {'data': i,
                           'media': pd.Series(df_sub_bacia.loc[df_sub_bacia.data == i, 'precip']).mean()
                            }
        media_diaria.append(media_diaria_aux)

    df_media_diaria = pd.DataFrame(media_diaria)

    #  Verifica se precisa ajustar por equacao do 2 grau
    if df_media_diaria['media'].sum() <= config_remocao.iloc[0]['limite_remocao']:
        limite_remocao = config_remocao.iloc[0]['a'] * df_media_diaria.media.sum()  ** 2 + \
                         config_remocao.iloc[0]['b'] * df_media_diaria.media.sum()
    else:
        limite_remocao = df_media_diaria.media.sum()

    #  Verifica se remocao passa do limite dos 10 dias
    if limite_remocao <= config_remocao.iloc[0]['lim_10_dias']:
        limite_10_dias = limite_remocao
    else:
        limite_10_dias = config_remocao.iloc[0]['lim_10_dias']

    #  Discretizacao da preciptacao com vies e limite_10_dias
    df_media_diaria['media_vies'] = df_media_diaria['media'] * (limite_10_dias / limite_remocao)

    #  Aplicacao do limite diario
    df_media_diaria['limite_diario'] = df_media_diaria['media_vies'].apply(
        lambda x: config_remocao.iloc[0]['lim_diario'] if x >= config_remocao.iloc[0]['lim_diario'] else x)

    #  Determinacao do coef beta para cada dia
    df_media_diaria['beta'] = df_media_diaria.apply(
        lambda x: x['limite_diario'] / x['media'] if x['media'] > 0 else 0 , axis=1
    )

    # Transposicao da remocao para pontos de grade
    df_sub_bacia['precip_vies'] = df_sub_bacia.precip.apply(lambda x: x * 0)
    for dia in df_media_diaria.data.unique():
        df_sub_bacia['precip_vies'] = df_sub_bacia.apply(
            lambda x: x['precip'] * df_media_diaria.loc[df_media_diaria.data == dia]['beta'] if \
            x['data'] == dia else x['precip'],
            axis=1
        )

    return  df_sub_bacia


def precip_conjunto(df_dados, config_conjunto):
    return


def cria_mapa(df_dados):
    return


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import os

    paths = {'gesf': r'C:\Users\ander\Desktop\GEFS_precipitacao10d',
             'eta': r'C:\Users\ander\Desktop\Eta40_precipitacao10d',
             'pontos_grade': r'C:\Users\ander\Desktop',
             'remocao_vies': r'C:\Users\ander\Desktop',
             'remover': r'C:\Users\ander\Desktop',
             'export': r'C:\Users\ander\Desktop'
             }

    nomes = {'gesf':[r'GEFS_p', r'a', r'.dat'],
             'eta': [r'ETA40_p', r'a', r'.dat'],
             'pontos_grade': [r'pontos_grade', r'.csv'],
             'remocao_vies': [r'remocao_vies', r'.csv'],
             'remover': [r'remover', r'.csv'],
             'export': [r'dados_vies', r'.csv']
             }

    data_inicial = r'09/05/2017'
    mes_previsao = 5

    #  importa dados de chuva
    df_dados = importa_dados(paths=paths, nomes=nomes, data_inicial=data_inicial)

    #  importa pontos de grade
    df_pontos_grade = importa_config(paths=r'{}\{}{}'.
                                           format(paths['pontos_grade'],
                                                  nomes['pontos_grade'][0],
                                                  nomes['pontos_grade'][1]
                                                  ),
                                           sep=';',
                                           decimal=',',
                                           )

    #  importa dados de remocao de vies
    df_remocao_vies = importa_config(paths=r'{}\{}{}'.
                                     format(paths['remocao_vies'],
                                            nomes['remocao_vies'][0],
                                            nomes['remocao_vies'][1]
                                            ),
                                     sep=';',
                                     decimal=',',
                                     )

    #  importa bacias que estao habilitadas para remocao de vies
    df_remover = importa_config(paths=r'{}\{}{}'.
                                     format(paths['remover'],
                                            nomes['remover'][0],
                                            nomes['remover'][1]
                                            ),
                                     sep=';',
                                     decimal=','
                                     )

    df_liberados = df_remover[df_remover.flag == 1]

    #   remocao de vies em todas as bacias liberadas
    df_sub_bacia_vies = pd.DataFrame()
    for item in df_liberados['sub_bacia']:
        df_aux = remove_vies(df_dados=df_dados,
                             config_remocao=df_remocao_vies[(df_remocao_vies['sub_bacia'] == item) &
                                                            (df_remocao_vies['mes_inicial'] == mes_previsao)],
                             sub_bacia=item,
                             df_grade_sub_bacia=df_pontos_grade[df_pontos_grade['sub_bacia'] == item]
                             )

        df_sub_bacia_vies = pd.concat([df_sub_bacia_vies, df_aux])

    df_final = df_dados
    df_final['precip_vies'] = df_final['precip']
    df_dados.set_index(keys=['modelo', 'data', 'lat', 'lon'], inplace=True)
    for i in df_sub_bacia_vies.iterrows():
        df_final.set_value(index=(i[1].modelo, i[1].data, i[1].lat, i[1].lon),
                           col='precip_vies',
                           value=i[1]['precip_vies']
                           )

    df_final.to_csv(path_or_buf=r'{}\{}{}'.format(paths['export'], nomes['export'][0], nomes['export'][1]),
                    sep=';',
                    decimal=','
    )

    pass

