# -*- coding: latin-1 -*-
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
    os.system(r'{} > nul'.format(parametros[2]))

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
    df_dados_complemento = pd.read_sql_query('select * from DadosGeraisComplemento', conn)
    df_dados_semanais = pd.read_sql_query('select * from VazoesSemanais', conn)

    print df_dados_semanais.head()


    return df_dados_semanais, df_dados_complemento

def cria_arquivos(path, dados_complemento, dados_vazao):

    return


if __name__ == '__main__':

    from multiprocessing import cpu_count, Pool
    import os
    import pandas as pd
    from datetime import datetime
    import numpy as np
    import pyodbc

    t1 = datetime.now()
    config_exec = {'path': r'C:\ENCAD3~1.0\Previvaz\bin\previvaz',
                   'exec': r'previvaz',
                   'licenca': r'C:\OneDrive\Middle Office\Middle',
                   'nome_lic': r'encad.dat',
                   'path_export': r'C:\Encad 3.0\usu_1',
                   'file_export': r'vazoes_previstas.csv'
                   }

    path = {'caso': r'C:\Encad 3.0\usu_1\est_1\caso_1'
            }


    #f_dados_semanais, df_dados_complemento = le_banco(path['caso'])

    #print df_dados_complemento.head()
    #print df_dados_semanais.head()

    #for index in df_dados_complemento.iterrows():
    #    pass
        #dic_aux = {'cod_posto': index[1]['CodigoDoPosto'],
        #           'semana_inic': index[1]['SemanaInicialPrev'],
        #           'ano_inic': index[1]['AnoInicialPrev'],
        #           'Vazao':

        #}


    folders = pd.Series(os.listdir(path['caso']))
    folders =  folders[(folders.isin(['Previvaz.mdb', 'Previvaz.ldb']) == False)].astype(int).sort_values()
    parametros = []
    for folder in folders.values:
        if folder not in  ['Previvaz.mdb', 'Previvaz.ldb']:
            aux = [int(folder),
                   r'{}\{}'.format(path['caso'], folder),
                   r'{}\{}'.format(config_exec['path'], config_exec['exec']),
                   r'{}\{}'.format(config_exec['licenca'], config_exec['nome_lic'])
            ]

        parametros.append(aux)

    parametros = np.array(parametros)

    # Paralelismo
    #p = Pool(processes=1)
    print('Execucao de previvaz em {} processos'.format(cpu_count()))
    p = Pool(processes=cpu_count())
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
