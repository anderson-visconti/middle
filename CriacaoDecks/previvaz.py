# -*- coding: iso-8859-1 -*-
def worker(parametros):
    import os
    from shutil import copyfile
    import glob
    import pandas as pd

    # Preparacao
    os.chdir(parametros[1]) # muda de diretorio
    copyfile(src=parametros[3], dst=r'{}\{}'.format(parametros[1], 'encad.dat'))    # copia licenca
    map(os.remove, glob.glob("*_fut.dat"))  # remove arquivo de previsao

    # Execucao do previvaz

    print ('Executando posto -> {:>3}'.format(parametros[0]))
    os.system(r'{} > NUL'.format(parametros[2]))

    # Captura dos dados de previsao
    file = open('{}\{}_fut.dat'.format(parametros[1], parametros[0]),mode='r').read().split('\n')
    posto = int(file[1][5:10].strip())
    ve = (' '.join(file[1][25:].split())).split()
    lim_inf = (' '.join(file[2][25:].split())).split()
    lim_sup = (' '.join(file[3][25:].split())).split()

    previsao = []
    for i in range(0, 6):
        previsao.append([posto, i + 1,float(ve[i]), float(lim_inf[i]), float(lim_sup[i])])

    df_previsao = pd.DataFrame(data=previsao,
                               columns=['CodigoDoPosto', 'Semana', 'Previsao', 'LimiteInferior', 'LimiteSuperior'])
    df_previsao.set_index(['CodigoDoPosto', 'Semana'], inplace=True)

    return df_previsao


def le_banco(path):
    import pyodbc

    odbc_conn_str = r'DRIVER={Microsoft Access Driver (*.mdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;axScanRows=8;MaxBufferSize=2048;FIL={MS Access};DriverId=25;DefaultDir=C:\;DBQ=%s' %(os.path.join(path, 'Previvaz.mdb'))

    conn = pyodbc.connect(odbc_conn_str)
    df_dados_gerais = pd.read_sql_query('select * from DadosGerais', conn)
    df_opcoes = pd.read_sql('select * from DadosGerais', conn)
    df_dados_complemento = pd.read_sql_query('select * from DadosGeraisComplemento', conn)
    df_dados_semanais = pd.read_sql_query('select * from VazoesSemanais', conn)
    df_limites = pd.read_sql_query('select * from LimitesPrevisao', conn)
    df_postos = pd.read_sql_query('select * from Postos', conn)
    return df_dados_gerais, df_opcoes, df_dados_semanais, df_dados_complemento, df_limites, df_postos


def cria_arquivos(parametros):
    import os
    import numpy as np
    import pandas as pd

    print ('Criacao de arquivos para o posto -> {}'.format(parametros['dados_config']['CodigoDoPosto'])).decode('iso-8859-1')

    #  cria pasta
    path = r'{}\{}'.format(parametros['caso_export'], parametros['dados_config']['CodigoDoPosto'])

    if os.path.exists(path=path) == False:
        os.mkdir(path)

    #  cria arquivo caso.dat
    file_caso = open(os.path.join(path, 'caso.dat'), 'a')
    file_caso.write('{}.inp'.format(parametros['dados_config']['CodigoDoPosto']))
    file_caso.close()

    #  cria arquivo .inp
    file_inp = open(os.path.join(path, '{}.inp'.format(parametros['dados_config']['CodigoDoPosto'])), 'a')
    file_inp.write(
"""{}                       ! nome do arquivo de relatorio
{}                       ! impressao dos parametros ?
{}                       ! nome do arquivo que contem a serie total2
{}                       ! sh sofrera transformacao? (0:nao; l:ln/nao; 2:bc/nao; 3:ln; 4:bc; 5:automatica)
{}                      ! mes de inicio do an hidrologico
{}
{}                   ! nome do arquivo excel
{}
{}
{}
{}

{}
{}
{}                       ! usa limite? (0:nao; 1:modelo e previsao; 2:apenas na previsao)
{}                   ! nome do arquivo de limites
{}                         0=>52 Semanas; 1 => 53 Semanas
""".format(parametros['dados_gerais'].loc[parametros['index'], 'ArquivoRelatorio'],
               'N',
               parametros['dados_gerais'].loc[parametros['index'], 'ArquivoVazoesSemanais'],
               parametros['dados_gerais'].loc[parametros['index'], 'Transformacao'],
               parametros['dados_gerais'].loc[parametros['index'], 'MesInicial'],
               parametros['dados_gerais'].loc[parametros['index'], 'ArquivoPrevisoes'],
               parametros['dados_gerais'].loc[parametros['index'], 'ArquivoExcel'],
               parametros['dados_gerais'].loc[parametros['index'], 'IntervaloConfianca'],
               parametros['dados_config']['SemanaInicialPrev'],
               parametros['dados_config']['AnoInicialPrev'],
               1,
               parametros['dados_config']['AnoFinalHistorico'],
               parametros['dados_gerais'].loc[parametros['index'], 'CodigoDoPosto'],
               parametros['dados_config']['FlagLimite'],
               parametros['dados_config']['ArqLimite'],
               parametros['dados_gerais'].loc[parametros['index'], 'CasoUsa53Semanas']
               )
    )
    file_inp.close()

    #  cria arquivo .lim
    file_limite = open(os.path.join(path, '{}.lim'.format(parametros['dados_config']['CodigoDoPosto'])), 'a')
    file_limite.write(
'''{}          ! Agrupamento (1:semanal, 2:mensal, 3:trimestral, 4:semestral)
{}          ! Faixas de Vazao (1:sem divisao, 2:duas faixas, 3:tres faixas, 4:quatro faixas)
'''.format(parametros['dados_config']['Discretizacao'], parametros['dados_config']['Magnitude'])
    )

    for i in parametros['limites'].iterrows():
        file_limite.write('{:>1d} {:>5.1f} {:>4.1f}\n'.format(int(i[1]['Ordem']),
                                                        i[1]['LimiteInferior'],
                                                        i[1]['LimiteSuperior']
                                                        )

    )

    file_limite.close()

    #  cria _str.dat
    file_str = open(os.path.join(path, '{}_str.dat'.format(parametros['dados_config']['CodigoDoPosto'])), 'a', )
    s =\
'''      {posto:>3d}
 {ano_inicial} {ano_final}  {drenagem}\n'''
    file_str.write(s.format(posto=int(parametros['dados_config']['CodigoDoPosto']),
                            ano_inicial=parametros['postos'].loc[parametros['index'] ,'AnoInicial'],
                            ano_final=parametros['postos'].loc[parametros['index'] ,'AnoFinal'],
                            drenagem=parametros['postos'].loc[parametros['index'] ,'AreaDeDrenagem'])
                   )

    for ano in pd.Series(parametros['dados']['Ano'].unique()).sort_values():

        for i in range(1, 7):
            dados = pd.DataFrame(parametros['dados'].loc[(parametros['dados'].Semana >= 1 + 9 * (i - 1)) &
                                                     (parametros['dados'].Semana <= 9 * i) &
                                                     (parametros['dados'].Ano == ano)

                                                     ]).sort_values(['Semana'])

            linha = np.array(dados.Vazao).astype(int)

            if len(linha) < 9:  #  completa com zeros as linha faltante
                for k in range(9 - len(linha)):
                    linha = np.append(linha, 0)

            linha = np.append(linha, int(ano))
            s = '  {0:>5}.  {1:>5}.  {2:>5}.  {3:>5}.  {4:>5}.  {5:>5}.  {6:>5}.  {7:>5}.  {8:>5}.    {9:>5}\n'
            file_str.write(s.format(*linha))

    file_str.close()

    return


if __name__ == '__main__':

    from multiprocessing import cpu_count, Pool
    import os
    import pandas as pd
    from datetime import datetime
    import numpy as np
    import pyodbc

    t1 = datetime.now()
    print(r'Execucao em {} processos'.format(cpu_count()))
    p = Pool(processes=cpu_count())
    p = Pool(processes=1)


    config_exec = {'path': r'C:\ENCAD3~1.0\Previvaz\bin\previvaz',
                   'exec': r'previvaz',
                   'licenca': r'C:\OneDrive\Middle Office\Middle',
                   'nome_lic': r'encad.dat',
                   'path_export': r'C:\Encad 3.0\usu_1',
                   'file_export': r'vazoes_previstas.csv'
                   }

    path = {#'caso': r'C:\Encad 3.0\usu_1\est_1\caso_1',
            'caso': r'C:\Encad 3.0\usu_1\est_1\caso_1',
            'caso_export': r'C:\Encad 3.0\usu_1\est_1\caso_1'
            }

    df_dados_gerais, df_opcoes, df_dados_semanais, df_dados_complemento, df_limites, df_postos = le_banco(path['caso'])
    dados_arquivos = []

    for index in df_dados_complemento.iterrows():

        dic_aux = {'dados_gerais':df_dados_gerais[df_dados_gerais['CodigoDoPosto'] == index[1]['CodigoDoPosto']],
                   'opcoes': df_opcoes[df_opcoes['CodigoDoPosto'] == index[1]['CodigoDoPosto']],
                   'dados_config': index[1],
                   'index':index[0],
                   'dados': df_dados_semanais[df_dados_semanais['CodigoDoPosto'] == index[1]['CodigoDoPosto']],
                   'limites': df_limites[df_limites['Codigo'] == index[1]['CodigoDoPosto']],
                   'caso_export': path['caso_export'],
                   'postos': df_postos[df_postos['CodigoDoPosto'] == index[1]['CodigoDoPosto']]
                   }

        dados_arquivos.append(dic_aux)

    print('Preparacao dos arquivos de configuracao')
    result = p.map(func=cria_arquivos, iterable=dados_arquivos)

    folders = pd.Series(os.listdir(path['caso']))
    folders =  folders[(folders.isin(['Previvaz.mdb', 'Previvaz.ldb']) == False)].astype(int).sort_values()
    parametros = []

    parametros = []
    folders = os.listdir(path['caso'])
    for folder in folders:
        if folder not in  ['Previvaz.mdb', 'Previvaz.ldb']:
            aux = [int(folder),
                   r'{}\{}'.format(path['caso'], folder),
                   r'{}\{}'.format(config_exec['path'], config_exec['exec']),
                   r'{}\{}'.format(config_exec['licenca'], config_exec['nome_lic']),

            ]

        parametros.append(aux)

    parametros = np.array(parametros)

    # Paralelismo
    print('\nExecucao de previvaz\n')
    result = p.map(func=worker, iterable=parametros)
    p.close()
    df_previsao = pd.DataFrame()
    for item in result:
        df_previsao = pd.concat([df_previsao, item], axis=0)

    df_previsao.to_csv(path_or_buf=r'{}\{}'.format(config_exec['path_export'], config_exec['file_export']),
                       sep=';',
                       decimal=','
                       )

    print ('Processo Finalizado')
    print ('Tempo Total: {}s'.format((datetime.now() - t1).total_seconds()))
