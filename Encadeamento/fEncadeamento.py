def fPreparaAmbiente(Path,QtdCenarios,DataInicial,DataFinal):
    'Funcao que prepara organizacao de pastas para receber os decks'
    import os
    from datetime import datetime

    # Determinando quantidades de meses
    Nmax = (datetime.strptime(DataFinal,'%Y-%m-%d') - datetime.strptime(DataInicial,'%Y-%m-%d')).month
    print(Nmax)

    #for i in range(0,QtdCenarios):
    #    x = 1

    return

def fEncadeamento(Path,nProc,numVersaoNewave,numVersaoDecomp):
    '''

    :param Path:
    :param nProc:
    :param numVersaoNewave:
    :param numVersaoDecomp:
    :return:
    '''
    vOpcoes = [1,1,1]

    numVersaoNewave = '22'
    numVersaoDecomp = '24'
    import os

    # Descobrindo informacoes do servidor ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------

    for cenarios in os.listdir(Path): # iteracao entre cenarios
        flag = 0  # flag para pular o primeiro mes de cada cenario
        #print os.path.join(Path, cenarios)
        PathL1 = os.path.join(Path, cenarios)

        for meses in os.listdir(PathL1):  # itercao entre meses em cada cenario
            print os.path.join(os.path.join(Path,cenarios),meses)
            PathL2 = os.path.join(os.path.join(Path,cenarios),meses)

            if flag == 0: # primeiro caso nao precisa
                # Executanto processo do newave ------------------------------------------------------------------------
                print ('Executando Newave do cenario %s do mes %s' %(cenarios,meses))
                print ('cd %s' %(os.path.join(PathL2,'newave')))

                os.chdir((os.path.join(PathL2,'newave')))
                os.system('/usr/bin/ConverteNomesArquivos')
                os.system('mpiexec -n %s /usr/bin/newave_%sL' %(nProc,numVersaoNewave))
                # ------------------------------------------------------------------------------------------------------

                # Executando processos do decomp -----------------------------------------------------------------------
                print ('Executando Decomp do cenario %s do mes %s' % (cenarios, meses))
                # ------------------------------------------------------------------------------------------------------
                flag = flag + 1

            else:
                print ('Algo')

    print ('Casos executados com sucesso!')
    return