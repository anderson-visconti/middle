#!/usr/bin/python
# *- coding: utf-8 -*-

def calcula_posto(posto, df_vazpast):

    if posto[0] == 298:
        print posto[1].head()
        for i in posto[1]:

            print(i)

    return df_vazpast

if __name__ == '__main__':
    import os
    import pandas as pd

    # Variaveis-------------------------------------------------------------------------------------------------------------
    path = r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2017\05\01\vazoes'         # Caminho onde esta arquivo vazeosC base e arquivo de projecao
    path_export = r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2017\05\01\vazoes'   # Caminho onde de exportacao
    nome_arquivo = r'Vazoes-base.txt'                                       # Nome do arquivo base vazoesC
    nome_arqv_proj = r'export-2017.txt'                                      # Nome do arquivo com vazoes projecoes
    ano_inicial = 2017                                                 # Ano a ser alterado
    # ----------------------------------------------------------------------------------------------------------------------
    df_vazoes = pd.read_fwf(filepath_or_buffer=os.path.join(path, nome_arquivo),
                             delim_whitespace=True,
                             names=['posto', 'ano', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                             index_col =['posto', 'ano']
                             )

    df_vazpast = pd.read_csv(filepath_or_buffer=os.path.join(path_export, nome_arqv_proj),
                            delimiter=';',
                            names=['posto', 'nome', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            skiprows=1
                             )

    df_vazpast.set_index(['posto'], inplace=True)

    for i in df_vazpast.iterrows():




        pass
