# *- coding: utf-8 -*-
def fLePmoDat(strPath, strNomeArqv):
    '''
    Funcao que le o arquivo pmo.dat e retira informacoes:
        Mercado Total
        Pequenas Usinas (Nao Simuladas)
    :param strPath:
    :param strNomeArqv:
    :returns vMercado - Lista contendo carga total projetada no horizonte
    :returns vPequenas - Lista contendo geracao de pequenas usinas no horizonte
    '''
    import os

    strFullPath = os.path.join(strPath, strNomeArqv)
    filePMO = open(strFullPath, 'r')

    # Inicializacao dos vetores ----------------------------------------------------------------------------------------
    vMercado = []           # Carga
    vMercadoAdic = []       # Carga Adicional - Andes X Itaipu e regiao Norte
    vPequenas = []          # Geracao de nao simuladas
    vConfigTerm = []        # Configuracao Termica
    vMaxTermica = []        # Geracao Maxima Termica
    vMinTermica = []        # Geracao Minima Termica
    vProgTermica = []       # Indisponibilidade Programada Termica
    vForcadaTermica = []    # Indisponibilidade Forcada Termica
    vCustoTermica = []      # CVU
    vCustoTermicaMes = []   # CVU - Estrutural + Conjuntural
    # ------------------------------------------------------------------------------------------------------------------
    contX = 0
    contIndisp = 0

    while True:
        linha = filePMO.readline()
        if not linha: break

        # Captura Mercado Total  ---------------------------------------------------------------------------------------
        if linha.strip() == 'DADOS DE MERCADO TOTAL DE ENERGIA (MWmedio)':
            contX = 0
            while contX <= 8:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX in [2, 4, 6, 8] and linha.strip()[0:1] != 'X':
                    aux = (' '.join(linha.split())).split(' ')
                    vMercado.append([contX / 2, aux])
                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura Mercado Adicional-------------------------------------------------------------------------------------
        if linha.strip() == 'DADOS DE CARGA ADICIONAL DE ENERGIA (MWmedio)':
            contX = 0
            while contX <= 8:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX in [2, 4, 6, 8] and linha.strip()[0:1] != 'X':
                    aux = (' '.join(linha.split())).split(' ')
                    vMercadoAdic.append([contX / 2, aux])
                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura Usinas Nao Simuladas ---------------------------------------------------------------------------------
        if linha.strip() == 'DADOS DE GERACAO DE PEQUENAS USINAS (MWmedio)':
            contX = 0
            while contX <= 8:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX in [2, 4, 6, 8] and linha.strip()[0:1] != 'X':
                    aux = (' '.join(linha.split())).split(' ')
                    vPequenas.append([contX / 2, aux])
                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura Configuracao Termica ---------------------------------------------------------------------------------
        if linha.strip() == 'CONFIGURACAO DAS USINAS TERMICAS':
            contX = 0
            while contX < 3:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX == 2 and linha.strip()[0:1] != 'X':
                    aux = [linha[2:8].strip(), linha[8:21].strip(), linha[21:33].strip()]   # Pega dados da linha
                    aux[2] = ['SUDESTE', 'SUL', 'NORDESTE', 'NORTE'].index(aux[2]) + 1  # transforma nome do subsistema em numero
                    vConfigTerm.append(aux)


                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura CVU - Estrutural + Conjuntural (Sera a disponibilidade do bloco CT)-------------------------------------------
        if linha.strip() == 'CUSTO DAS CLASSES TERMICAS ($/MWH)':
            contX = 0
            while contX < 3:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX == 2 and linha.strip()[0:1] != 'X':

                    if linha[2:9].strip() != '' and linha[2:9].strip() not in ['86', '15']:    # Pega o codigo da usina
                        CodUsinaTermica = linha[2:9].strip()    # Cod Usina Termica
                        NomeUsinaTermica= linha[9:22].strip()   # Nome Usina Termica

                    aux = [CodUsinaTermica, NomeUsinaTermica, (' '.join(linha[24:].split())).split(' ')] # Dados Cod,Nome,[Ano,Ger Max por mes]
                    vCustoTermicaMes.append(aux)

                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura Geracao Termica Maxima (Sera a disponibilidade do bloco CT)-------------------------------------------
        if linha.strip() == 'GERACAO TERMICA MAXIMA POR USINA (MWmed)':
            contX = 0
            while contX < 3:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX == 2 and linha.strip()[0:1] != 'X':

                    if linha[2:9].strip() != '' and linha[2:9].strip() not in ['86', '15']:    # Pega o codigo da usina
                        CodUsinaTermica = linha[2:9].strip()    # Cod Usina Termica
                        NomeUsinaTermica= linha[9:22].strip()   # Nome Usina Termica

                    aux = [CodUsinaTermica, NomeUsinaTermica, (' '.join(linha[24:].split())).split(' ')] # Dados Cod,Nome,[Ano,Ger Max por mes]
                    vMaxTermica.append(aux)

                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura Geracao Termica Minina (Sera a inflexibilidade do bloco CT)-------------------------------------------
        if linha.strip() == 'GERACAO TERMICA MINIMA POR USINA (MWmed)':
            contX = 0
            while contX < 3:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX == 2 and linha.strip()[0:1] != 'X':

                    if linha[2:9].strip() != '' and linha[2:9].strip() not in ['86', '15']:  # Pega o codigo da usina
                        CodUsinaTermica = linha[2:9].strip()  # Cod Usina Termica
                        NomeUsinaTermica = linha[9:22].strip()  # Nome Usina Termica

                    aux = [CodUsinaTermica, NomeUsinaTermica,
                           (' '.join(linha[24:].split())).split(' ')]  # Dados Cod,Nome,[Ano,Ger Max por mes]
                    vMinTermica.append(aux)

                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura Indisponibilidade Programada Termica (BLOCO MT?)------------------------------------------------------
        if linha.strip() == 'INDISPONIBILIDADE PROGRAMADA (%)':
            contIndisp = contIndisp + 1
            contX = 0
            while contX < 3 and contIndisp > 1:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX == 2 and linha.strip()[0:1] != 'X':

                    if linha[2:9].strip() != '':  # Pega o codigo da usina
                        CodUsinaTermica = linha[2:9].strip()  # Cod Usina Termica
                        NomeUsinaTermica = linha[9:22].strip()  # Nome Usina Termica

                    aux = [CodUsinaTermica, NomeUsinaTermica,
                           (' '.join(linha[24:].split())).split(' ')]  # Dados Cod,Nome,[Ano,Ger Max por mes]
                    vProgTermica.append(aux)

                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura Indisponibilidade Programada Termica (BLOCO MT)-------------------------------------------------------
        if linha.strip() == 'TAXA EQUIVALENTE DE INDISPONIBILIDADE FORCADA DA USINA TERMICA(%)':
            contX = 0
            while contX < 3:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX == 2 and linha.strip()[0:1] != 'X':

                    if linha[2:9].strip() != '':  # Pega o codigo da usina
                        CodUsinaTermica = linha[2:9].strip()  # Cod Usina Termica
                        NomeUsinaTermica = linha[9:22].strip()  # Nome Usina Termica

                    aux = [CodUsinaTermica, NomeUsinaTermica,
                           (' '.join(linha[24:].split())).split(' ')]  # Dados Cod,Nome,[Ano,Ger Max por mes]
                    vForcadaTermica.append(aux)

                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

        # Captura CVU das Termicas--------------------------------------------------------------------------------------
        if linha.strip() == 'DADOS DAS CLASSES TERMICAS':
            contX = 0
            while contX < 3:

                if linha.strip()[0:1] == 'X':
                    contX = contX + 1

                if contX == 2 and linha.strip()[0:1] != 'X':

                    if linha[2:9].strip() != '':  # Pega o codigo da usina
                        CodUsinaTermica = linha[2:9].strip()  # Cod Usina Termica
                        NomeUsinaTermica = linha[11:24].strip()  # Nome Usina Termica

                    aux = [CodUsinaTermica, NomeUsinaTermica,
                           (' '.join(linha[37:].split())).split(' ')]  # Dados Cod,Nome,[Ano,Ger Max por mes]
                    vCustoTermica.append(aux)

                linha = filePMO.readline()
        # --------------------------------------------------------------------------------------------------------------

    return vMercado, vPequenas, vConfigTerm, vMinTermica, vMaxTermica, vProgTermica, vForcadaTermica, vCustoTermica,\
           vMercadoAdic, vCustoTermicaMes


def fLeExpH(strPath, strNomeArqv):
    '''
    :param strPath:
    :param strNomeArqv:
    :return:
    '''
    import os

    flag = 0
    vExpansao = []      # Vetor com dados para expansao hidroenergetica
    vMaq = []        # Vetor auxiliar para dados da entrada de maquinas
    vDadosUsina = []    # Vetor com dados cadastrais da usina
    vExpAux =[]
    strFullPath = os.path.join(strPath,strNomeArqv)
    file = open(strFullPath,'r')

    while True:
        linha = file.readline()
        if not linha: break

        if linha.strip()[0:1] not in ['C', 'I', 'X'] and linha.strip()[0:4] not in ['9999']:

            if linha[0:4].strip().isdigit() and linha[0:4] != '9999':
                vDadosUsina = [linha[0:4].strip(), linha[5:18].strip(), linha[18:26].strip()]

            vExpAux = [linha[44:52].strip(),linha[52:59].strip(), linha[61:62].strip(), linha[64:65].strip()]
            vExpansao.append([vDadosUsina,vExpAux])

    return vExpansao


def fLeModifDat(strPath, strNomeArqv):

    import os
    vVE = []    # Vetor com dados para bloco VE
    vFuga = []  # Vetor com dados de canal de fuga

    strFullPath = os.path.join(strPath,strNomeArqv)
    file = open(strFullPath,'r')
    while True:
        linha = file.readline()
        if not linha: break

        if linha[0:10].strip() == 'USINA':  # Pega codigo da usina
            usina = linha[10:14].strip()

        if linha[0:10].strip() == 'VMAXT':  # Pega valores de volume maximo
            dados = (' '.join(linha[10:].split())).split(' ')
            vVE.append([usina,dados])

        if linha[0:10].strip() == 'CFUGA':  # Pega valores de canal de fuga
            dados = (' '.join(linha[10:].split())).split(' ')
            vFuga.append([usina, dados])

    return vVE, vFuga


def fLePatamarDat(strPath, strNomeArqv, intAnoInicial, intAnoFinal):
    '''

    :param strPath:
    :param strNomeArqv:
    :param intAnoInicial:
    :param intAnoFinal:
    :returns: vDuracao,vCargaPU:
        vDuracao - Lista com duracao dos patamares de carga mensalisados
        vCargaPU - Lista com PU de carga dos patamares

    '''

    import os
    strFullPath = os.path.join(strPath, strNomeArqv)
    filePMO = open(strFullPath, 'r')
    vCargaPU = []
    vDuracao = []
    vAnos = []
    contAno = 0
    filePatamares = open(os.path.join(strPath, strNomeArqv))

    for i in range(0, intAnoFinal - intAnoInicial + 1):
        vAnos.append(str(intAnoInicial + i))

    while True:
        linha = filePMO.readline()
        if not linha: break
        # Duracao dos patamares de carga -------------------------------------------------------------------------------
        if linha.strip() == 'ANO   DURACAO MENSAL DOS PATAMARES DE CARGA':

            while contAno < intAnoFinal - intAnoInicial + 1:  # horizonte presente no patamar.dat
                linha = filePatamares.readline()

                if linha.strip()[0:4].strip() in vAnos and (linha.strip()[0:1] not in ['X', 'J']):
                    ano = int(float(linha.strip()[0:4].strip()))

                    for i in range(0, 3):
                        aux = linha[6:]
                        aux = (' '.join(aux.split())).split(' ')
                        vDuracao.append([ano, i + 1, aux])
                        if i < 2:
                            linha = filePatamares.readline()

                    contAno = contAno + 1
        # --------------------------------------------------------------------------------------------------------------
        contAno = 0
        # Duracao dos patamares de carga -------------------------------------------------------------------------------
        if linha.strip() == 'ANO                       CARGA(P.U.DEMANDA MED.)':

            while contAno < intAnoFinal - intAnoInicial + 1:  # horizonte presente no patamar.dat
                linha = filePatamares.readline()

                if linha.strip()[0:4].strip() in vAnos and (linha.strip()[0:1] not in ['X', 'J']):
                    ano = int(float(linha.strip()[0:4].strip()))

                    for i in range(0, 3):
                        aux = linha[7:]
                        aux = (' '.join(aux.split())).split(' ')
                        vCargaPU.append([ano, i + 1, aux])
                        if i < 2:
                            linha = filePatamares.readline()

                    contAno = contAno + 1
        # --------------------------------------------------------------------------------------------------------------

    return vDuracao, vCargaPU


def fLeCadUHs(strPath, strNomeArqv, strDelimitador):

    import csv
    import os

    vDadosHidro = []
    strFullPath = os.path.join(strPath, strNomeArqv)

    with open(strFullPath, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=strDelimitador)

        for linha in file:

            for i in range(0,len(linha)):
                linha[i] = linha[i].strip()

            vDadosHidro.append(linha)

    return vDadosHidro


def fCarregaFeriados(strPath, strNomeArqv, strDelimitador):
    '''

    :param strPath:
    :param strNomeArqv:
    :param strDelimitador:
    :return:
    '''
    import csv
    import os
    from datetime import datetime
    vFeriados = []
    strFullPath = os.path.join(strPath, strNomeArqv)

    with open(strFullPath, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=strDelimitador)
        for linha in file:

            if (file.line_num) == 1:
                vFeriados.append(linha)
            else:
                vFeriados.append(datetime.strptime(linha[0], '%d/%m/%Y'))

    vFeriados = vFeriados[1:]
    return vFeriados


def fLeDesvAguaDat(strPath, strNomeArqv):
    import os
    flag = 0
    strFullPath = os.path.join(strPath,strNomeArqv)
    fileDesv = open(strFullPath,'r')

    vDesvAgua = []
    while True:
        linha = fileDesv.readline()
        if not linha or linha[0:4].strip() == '9999':
            break

        if linha[0:1].strip() not in ['X','A']:

            if linha[103:].split('-')[0].strip() in ['Usos_Consuntivos','Vazao_Remanescente']:
                aux = linha[99:].strip().split('-')


            auxDados  = (' '.join(linha[0:94].split())).split(' ')
            vDesvAgua.append([auxDados,aux])

    return vDesvAgua


def fCalculaEstagios(strDataInicial, vMeses, EstM1, vFeriados, vAnos):
    '''
    :param strDataInicial:
    :param vMeses:
    :param EstM1:
    :param vFeriados:
    :return:
    '''
    from datetime import datetime, timedelta
    from calendar import monthrange

    DataInicial = datetime.strptime(strDataInicial, '%d/%m/%Y')
    vHorasDP = []
    ContT1 = ContT2 = 0
    ano = DataInicial.year
    aux = 0
    if vAnos[0] - vAnos[1] != 0 or DataInicial.year - vAnos[1] !=0:
        aux = 1

    UlltimoDiaM1 = monthrange(DataInicial.year, vMeses[0])

    # Primeiro mes -----------------------------------------------------------------------------------------------------
    for i in range(0, EstM1):  # itera sobre numero de estagio do primeiro mes

        for j in range(0, 7):  # itera sobre 6 dias da semana

            if DataInicial in vFeriados or DataInicial.weekday() in [6]:  # Verificacao do tipo do dia
                ContT2 = ContT2 + 1  # Quantidade de dias tipo 2

            else:
                ContT1 = ContT1 + 1  # Quantidade de tipo 1

            DataInicial = DataInicial + timedelta(days=+1)

        vEstagioAux = \
        [
        # Pesado , Medio , Leve
        0 * ContT2 + 3 * ContT1,
        5 * ContT2 + 14 * ContT1,
        19 * ContT2 + 7 * ContT1,
        ]

        vHorasDP.append([i + 1, DataInicial + timedelta(days=-7), DataInicial + timedelta(days=-1), vEstagioAux])
        ContT2 = ContT1 = 0
    # ------------------------------------------------------------------------------------------------------------------

    # Numero de dias do mes 2 no mes 1 ---------------------------------------------------------------------------------
    x = datetime(ano + aux, vMeses[1], 1)
    IntDiasMes2 = (DataInicial - datetime(ano + aux, vMeses[1], 1)).days
    # ------------------------------------------------------------------------------------------------------------------

    # Segundo mes ------------------------------------------------------------------------------------------------------
    ContT2 = ContT1 = 0
    while DataInicial.month == vMeses[1]:  # Enquanto o mes for o mesmo do apontado

        if DataInicial in vFeriados or DataInicial.weekday() in [6]:  # Verificacao do tipo do dia
            ContT2 = ContT2 + 1  # Quantidade de dias tipo 2

        else:
            ContT1 = ContT1 + 1  # Quantidade de tipo 1

        DataInicial = DataInicial + timedelta(days=+1)

    vEstagioAux = \
    [
    # Pesado , Medio , Leve
    0 * ContT2 + 3 * ContT1,
    5 * ContT2 + 14 * ContT1,
    19 * ContT2 + 7 * ContT1,
    ]
    vHorasDP.append([i + 1, DataInicial + timedelta(days=-7), DataInicial + timedelta(days=-1), vEstagioAux])
    # ------------------------------------------------------------------------------------------------------------------
    print('Numero de horas dos estagios calculados com sucessos.\n'
          'Numero de dias no segundo mes calculados com sucesso'
          )
    return vHorasDP, IntDiasMes2


def fLeConfigArvores(strPath, strArqv, strDelimitador):
    import csv
    import os

    strFullPath = os.path.join(strPath,strArqv)
    vConfigArvores = []

    with open(strFullPath, 'r') as csvfile:
        file = csv.reader(csvfile, delimiter=strDelimitador)

        for linha in file:
            vConfigArvores.append(linha)

    return vConfigArvores


def fEscreveDadger(strPathSource, strPathExport, strNomeArqv, vMeses, vAnos, vConfigTerm, vMinTermica, vMaxTermica,
                   vCustoTermica, EstM1, vCargaPU, vBlocoDP, IntDiasMes2, vMercado, vPequenas, vDesvAgua, vDadosHidro,
                   vConfigArvores, vRee, vVe, vCustoTermicaMes):

    import os
    from datetime import datetime
    from datetime import timedelta

    fileOriginal = open(os.path.join(strPathSource,strNomeArqv),'r')
    DadosOriginais = fileOriginal.readlines()
    fileOriginal.close()
    fileExport = open(os.path.join(strPathExport,strNomeArqv),'w')
    DadosExport = []
    vCarga =[]
    vPQ = []
    vSubsistemas = []
    vUH = []
    vAC = []
    flag = 0
    for i in range(0,len(DadosOriginais)):

        # Reescreve Comentarios ----------------------------------------------------------------------------------------
        if DadosOriginais[i].find('BLOCO') != -1 or DadosOriginais[i].find('EXPANSAO 2º MES') !=-1 or DadosOriginais[i].find('CVAR') != -1:
            fileExport.write('&----------------------------------------------------------------\n'
                             + DadosOriginais[i]+
                             '&----------------------------------------------------------------\n')
        #---------------------------------------------------------------------------------------------------------------

        # Blocos que so serao repetidos --------------------------------------------------------------------------------
        if DadosOriginais[i][0:2] in ['SB','UH','UE','CD','TX','GP','NI','FU', 'CQ', 'CV', 'AC', 'AR', 'EZ', 'CA',
                                      'EA','IR', 'CI', 'VI', 'QI', 'FI', 'FT']:

            if DadosOriginais[i][0:2] == 'SB':  # Pega informacoes do subsistema
                vSubsistemas.append((' '.join(DadosOriginais[i].split())).split(' '))

            if DadosOriginais[i][0:2] == 'UH':  # Pega Configuracao de usinas atuais
                vUH.append((' '.join(DadosOriginais[i].split())).split(' '))

            if DadosOriginais[i][0:2] == 'EA' and flag == 0:  # Escree
                fileExport.write(DadosOriginais[i - 2])
                fileExport.write(DadosOriginais[i - 1])
                flag = 1

            if DadosOriginais[i][0:2] == 'AC' and flag == 0:  # Escree
                vAC.append((' '.join(DadosOriginais[i].split())).split(' '))

            fileExport.write(DadosOriginais[i])
        # --------------------------------------------------------------------------------------------------------------

        # Reescreve informacoes apenas alterando intervalos ------------------------------------------------------------
        if DadosOriginais[i][0:2] in ['IT','IA','RE', 'LU', 'HQ', 'LQ','HV', 'LV', 'HA', 'LA']:

            # Bloco IT -------------------------------------------------------------------------------------------------
            if DadosOriginais[i][0:2].strip() == 'IT':
                aux = ' '.join(DadosOriginais[i].split()).split(' ')

                if DadosOriginais[i][4:7].strip() != '1':
                    aux = ' '.join(DadosOriginais[i].split()).split(' ')
                    aux[1] = str(EstM1 + 1)

                fileExport.write('{:>2}  {:>2}   {:>3}  {:>2}   {:>5}{:>5}{:>5}{:>5}{:>5}{:>5}\n'.format(*aux))
            #-----------------------------------------------------------------------------------------------------------

            # Bloco IA (provisorio) ------------------------------------------------------------------------------------
            if DadosOriginais[i][0:2].strip() == 'IA':

                if DadosOriginais[i][4:7].strip() != '1':
                    aux = DadosOriginais[i].replace(DadosOriginais[i][4:6], '{:>2}'.format(str(EstM1 + 1)))

                else:
                    aux = DadosOriginais[i]

                fileExport.write(aux)
            #-----------------------------------------------------------------------------------------------------------

            # Blocos RE , HQ, HV  e HA----------------------------------------------------------------------------------
            if DadosOriginais[i][0:2].strip() in ['RE', 'HQ', 'HV', 'HA']:
                DadosOriginais[i-1] # Rescreve 1 linha anterior
                aux = DadosOriginais[i].replace(DadosOriginais[i][-2:], str(EstM1 + 1) + '\n')

                for k in range(4, 0, -1):

                    if DadosOriginais[i - k][0:1] == '&':  # reescreve somente se for comentario
                        fileExport.write(DadosOriginais[i - k])  # Resscreve ate 4 linhas de comentarios

                fileExport.write(aux)

            if DadosOriginais[i][0:2] in ['LU', 'LQ', 'LV', 'LA']:

                if int(float(DadosOriginais[i][9:11].strip())) > EstM1 + 1:
                    aux2= DadosOriginais[i][0:10]
                    aux = aux2 + str(EstM1 + 1) + DadosOriginais[i][11:]

                else:
                    aux = DadosOriginais[i]

                fileExport.write(aux)
            #-----------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------

        # Blocos que serao reescritos completamente --------------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() in ['&TE', '&CT', '&DP', '&PQ', '&DT', '&MP', '&MT', '&FD', '&VE', '&RQ', '&VE']:

            # Bloco TE -------------------------------------------------------------------------------------------------
            if DadosOriginais[i][0:4].strip() == '&TE':
                fileExport.write('TE  Prospectivo %s-%s / %s-%s - RV0 - Script automatico\n' % (
                vMeses[0], vAnos[0], vMeses[1], vAnos[1]))
            # ----------------------------------------------------------------------------------------------------------

            # Bloco CT -------------------------------------------------------------------------------------------------
            if DadosOriginais[i][0:4].strip() == '&CT':
                fileExport.write('&CT\n')

                for aux in range(4,0,-1):
                    fileExport.write(DadosOriginais[i-aux])

                for i in range(0,len(vConfigTerm)): # Itera sobre todas as termicas cadastradas

                    for j in range(0,len(vMaxTermica)): # Itera sobre a sazo de ger. max e ger.min

                        if vConfigTerm[i][0] == vMaxTermica[j][0] and str(vAnos[0]) == vMaxTermica[j][2][0]: # Verifica Cod da usina e ano
                            vDisponibilidade = \
                                [int(float(vMaxTermica[j][2][vMeses[0]])),  # Primeiro estagio
                                 int(float(vMaxTermica[j + (vAnos[1] - vAnos[0])][2][vMeses[1]])) # Segundo estagio
                                ]

                            vInflexbilidade = \
                                [int(float(vMinTermica[j][2][vMeses[0]])),  # Primeiro estagio
                                 int(float(vMinTermica[j + (vAnos[1] - vAnos[0])][2][vMeses[1]]))  # Segundo estagio
                                 ]

                            custo = [float(vCustoTermicaMes[j][2][vMeses[0]]),
                                     float(vCustoTermicaMes[j + (vAnos[1] - vAnos[0])][2][vMeses[1]])
                                     ]

                            aux1 = \
                            'CT' + '{:>5}'.format(vConfigTerm[i][0]) + \
                            '{:>4}'.format(str(vConfigTerm[i][2])) + ' ' * 3 + \
                            '{:10.10}'.format(vConfigTerm[i][1]) + \
                            '{:>2}'.format(str(1)) + ' ' * 3 + \
                            str('{:4d}'.format(vInflexbilidade[0])) + '.' + \
                            str('{:4d}'.format(vDisponibilidade[0])) + '.' + \
                            '{:>10}'.format(custo[0]) + \
                            str('{:4d}'.format(vInflexbilidade[0])) + '.' + \
                            str('{:4d}'.format(vDisponibilidade[0])) + '.' + \
                            '{:>10}'.format(custo[0]) + \
                            str('{:4d}'.format(vInflexbilidade[0])) + '.' + \
                            str('{:4d}'.format(vDisponibilidade[0])) + '.' + \
                            '{:>10}'.format(custo[0]) +'\n'

                            aux2 = \
                            'CT' + '{:>5}'.format(vConfigTerm[i][0]) + \
                            '{:>4}'.format(str(vConfigTerm[i][2])) + ' ' * 3 + \
                            '{:10.10}'.format(vConfigTerm[i][1]) + \
                            '{:>2}'.format(str(EstM1+1)) + ' ' * 3 + \
                            str('{:4d}'.format(vInflexbilidade[1])) + '.' + \
                            str('{:4d}'.format(vDisponibilidade[1])) + '.' + \
                            '{:>10}'.format(custo[1]) + \
                            str('{:4d}'.format(vInflexbilidade[1])) + '.' + \
                            str('{:4d}'.format(vDisponibilidade[1])) + '.' + \
                            '{:>10}'.format(custo[1]) + \
                            str('{:4d}'.format(vInflexbilidade[1])) + '.' + \
                            str('{:4d}'.format(vDisponibilidade[1])) + '.' + \
                            '{:>10}'.format(custo[1]) +'\n'
                            fileExport.write(aux1)
                            fileExport.write(aux2)
                            break
            #-----------------------------------------------------------------------------------------------------------

            # Bloco DP -------------------------------------------------------------------------------------------------
            if DadosOriginais[i][0:4].strip() == '&DP':
                fileExport.write('&DP\n')
                # Reescreve Cabecalho do bloco de carga ----------------------------------------------------------------
                for aux in range(5,0,-1):
                    fileExport.write(DadosOriginais[i-aux])
                # ------------------------------------------------------------------------------------------------------

                # Pega P.U. de carga dos meses -------------------------------------------------------------------------
                for j in range(0, len(vCargaPU)):

                    if vCargaPU[j][0] == vAnos[0]:
                        vPU = \
                            [
                                [
                                    float(vCargaPU[j][2][vMeses[0] - 1]),
                                    float(vCargaPU[j + 1][2][vMeses[0] - 1]),
                                    float(vCargaPU[j + 2][2][vMeses[0] - 1])
                                ],
                                [
                                    float(vCargaPU[j + 3 * (vAnos[1] - vAnos[0])][2][vMeses[1] - 1]),
                                    float(vCargaPU[j + 1 + 3 * (vAnos[1] - vAnos[0])][2][vMeses[1] - 1]),
                                    float(vCargaPU[j + 2 + 3 * (vAnos[1] - vAnos[0])][2][vMeses[1] - 1])
                                ]
                            ]
                        break
                #-------------------------------------------------------------------------------------------------------

                # Pega Carga -------------------------------------------------------------------------------------------
                for i in range(1,5): # Itera para 4 submercados

                        for j in range(0,len(vMercado)):    # Pega carga do mes

                            if i == int(vMercado[j][0]) and str(vAnos[0]) == vMercado[j][1][0]:
                               vCarga.append([float(vMercado[j][1][vMeses[0]]),float(vMercado[j + vAnos[1] - vAnos[0]][1][vMeses[1]])])
                               break
                #-------------------------------------------------------------------------------------------------------

                # Escreve Bloco DP -------------------------------------------------------------------------------------
                for i in range(1,EstM1 + 2):    # Itera sobre estagios do primeiro mes
                    Mes2 = 0

                    if i == EstM1 + 1:
                        Mes2 = 1

                    for j in range(0,len(vSubsistemas)):    # Itera sobre subsistemas + Fict

                        if vSubsistemas[j][2] != 'FC':
                            aux = \
                            'DP' + ' ' * 2 + \
                            '{:2d}'.format(i) + \
                            ' ' * 3 + '{:>2}'.format(vSubsistemas[j][1]) + \
                            ' ' * 3 + '3' + ' ' * 4 + \
                            '{:10.1f}'.format(vPU[Mes2][0] * vCarga[j][Mes2]) + \
                            '{:10.1f}'.format(vBlocoDP[i-1][3][0]) + \
                            '{:10.1f}'.format(vPU[Mes2][1] * vCarga[j][Mes2]) + \
                            '{:10.1f}'.format(vBlocoDP[i-1][3][1]) + \
                            '{:10.1f}'.format(vPU[Mes2][2] * vCarga[j][Mes2]) + \
                            '{:10.1f}'.format(vBlocoDP[i-1][3][2]) +'\n'

                            fileExport.write(aux)

                        else:
                            aux = \
                            'DP' + ' ' * 2 + \
                            '{:2d}'.format(i) + \
                            ' ' * 3 + '{:>2}'.format(vSubsistemas[j][1]) + \
                            ' ' * 3 + '3' + ' ' * 4 + \
                            '{:10.1f}'.format(0 * vCarga[j-1][Mes2]) + \
                            '{:10.1f}'.format(vBlocoDP[i-1][3][0]) + \
                            '{:10.1f}'.format(0 * vCarga[j-1][Mes2]) + \
                            '{:10.1f}'.format(vBlocoDP[i-1][3][1]) + \
                            '{:10.1f}'.format(0 * vCarga[j-1][Mes2]) + \
                            '{:10.1f}'.format(vBlocoDP[i-1][3][2]) + '\n'

                            fileExport.write(aux)


                    fileExport.write('&\n')
                #-------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # Bloco PQ -----------------------------------------------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&PQ':
            fileExport.write('&PQ\n')

            # Pega valores de geracao ----------------------------------------------------------------------------------
            for i in range(0,len(vSubsistemas)):    # Itera sobre subsistemas

                for j in range(0,len(vPequenas)):   # Itera sobre o vetor de pequenas

                    if float(vSubsistemas[i][1]) == vPequenas[j][0] and str(vAnos[0]) == vPequenas[j][1][0]:
                        vPQ.append\
                        (
                            [
                                int(float(vPequenas[j][1][vMeses[0]])), # Primeiro estagio
                                int(float(vPequenas[j + (vAnos[1] - vAnos[0])][1][vMeses[1]]))  # Segundo estagio
                            ]
                        )
                        break
            # ----------------------------------------------------------------------------------------------------------

            # Escreve bloco PQ -----------------------------------------------------------------------------------------
            for i in range(0,len(vSubsistemas)-1):

                for j in range(0,len(vBlocoDP)):
                    Mes2 = 0

                    if j == len(vBlocoDP) - 1:
                        Mes2 = 1

                    vaux = ['SUDESTE', 'SUL', 'NORDESTE', 'NORTE']

                    aux = \
                    'PQ' + ' ' * 2 + \
                    '{:<11}'.format(vaux[i]) + \
                    '{:>1}'.format(vSubsistemas[i][1]) + ' ' * 3 + \
                    '{:2d}'.format(j + 1) + ' ' * 3 + \
                    '{:5d}'.format(vPQ[i][Mes2]) + \
                    '{:5d}'.format(vPQ[i][Mes2]) + \
                    '{:5d}'.format(vPQ[i][Mes2]) + '\n'

                    fileExport.write(aux)
            # ----------------------------------------------------------------------------------------------------------

        # Bloco DT -----------------------------------------------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&DT':
            fileExport.write('&DT\n')
            # Escreve bloco DT -----------------------------------------------------------------------------------------
            aux = \
            'DT' + ' ' * 2 + \
            '{:02d}'.format(vBlocoDP[0][1].day) + ' ' * 3 + \
            '{:02d}'.format(vBlocoDP[0][1].month) + ' ' * 3 + \
            '{:4d}'.format(vBlocoDP[0][1].year) + '\n'
            fileExport.write(aux)
            #-----------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------

        # Bloco MP - Utiliza (1 - IP) * (1 - TEIF) do CadUH (HIDR)------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&MP':
            fileExport.write('&MP\n')

            for i in range(0,len(vUH)):

                for j in range(0,len(vDadosHidro)):

                    if vUH[i][1] == vDadosHidro[j][0]:
                        ip = (1.0 - float(vDadosHidro[j][39].replace(',','.'))/100.0) * \
                             (1.0 - float(vDadosHidro[j][38].replace(',','.'))/100.0)
                        aux = 'MP' + ' ' * 2 + '{:>3}'.format(vUH[i][1]) + ' ' * 2

                        for z in range(0,EstM1 + 1):
                            aux = aux + '{:3.3f}'.format(ip)

                        fileExport.write(aux + '\n')

        #---------------------------------------------------------------------------------------------------------------

        # Bloco MT(Retira pq por deafult considera tudo 1)--------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&MT':
            fileExport.write('&MT\n')
            fileExport.write('&----------------------------------------------------\n')
            fileExport.write('&MT - Disponibilidade de termicas definidas em CT\n')
            fileExport.write('&MT\n')
            fileExport.write('&----------------------------------------------------\n')
        # --------------------------------------------------------------------------------------------------------------

        # Bloco FC -----------------------------------------------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&FC':
            fileExport.write('FC' + ' ' * 2 + 'NEWV21' + ' ' * 4 + '../newave/cortesh.dat\n')
            fileExport.write('FC' + ' ' * 2 + 'NEWCUT' + ' ' * 4 + '../newave/cortes.dat\n&\n')

        # --------------------------------------------------------------------------------------------------------------

        # Bloco TI -----------------------------------------------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&TI':
            fileExport.write('&TI\n')

            for cab in range(3,-1,-1):
                fileExport.write(DadosOriginais[i - cab])


            for i in range(0,len(vUH)):

                for j in range(0,len(vDesvAgua)):

                    if vUH[i][1] == vDesvAgua[j][0][1] and vDesvAgua[j][1][0].strip() == 'Usos_Consuntivos':
                        vIrrigacao = [
                            abs(float(vDesvAgua[j][0][vMeses[0] + 1])),   # primeiro mes
                            abs(float(vDesvAgua[j + (vAnos[1] - vAnos[0])][0][vMeses[1] +1]))    # segundo mes
                            ]
                        aux = 'TI  %s  ' %('{:>3}'.format(vUH[i][1]))

                        for k in range(0,EstM1 + 1):
                            if k < EstM1:
                                aux = aux + '{:5.1f}'.format(vIrrigacao[0])
                            else:
                                aux = aux + '{:5.1f}'.format(vIrrigacao[1]) +'\n'

                        fileExport.write(aux)
                        break

        # --------------------------------------------------------------------------------------------------------------

        # Bloco RQ -----------------------------------------------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&RQ':
            fileExport.write('&RQ\n')

            for i in range(0,len(vRee)):    # Itera sobre REEs declarados
                aux = 'RQ  ' + '{:>2}'.format(vRee[i]) + ' ' * 3

                for j in range(0,EstM1 + 1):    # Itera sobre numero de estagios

                    if j < EstM1:   # Estagios do primeiro mes
                        aux = aux + '{:>5}'.format('100')

                    else:
                        aux = aux + ' ' * 1 + '{:>5}'.format('0.'+'\n')

                fileExport.write(aux)
        #---------------------------------------------------------------------------------------------------------------

        # Bloco VE -----------------------------------------------------------------------------------------------------
        if DadosOriginais[i][0:4].strip() == '&VE':
            fileExport.write('&VE\n')
            auxDataM1 = datetime(vAnos[0],vMeses[0], 1)
            auxDataM2 = datetime(vAnos[1], vMeses[1], 1)

            for i in range(0,len(vUH)):
                dados = [100.0,100.0]
                # Procura Valores --------------------------------------------------------------------------------------
                for j in range(0,len(vVe)):

                    if int(vUH[i][1]) == int(vVe[j][0]):

                        if auxDataM1 >= datetime(int(float(vVe[j][1][1])),int(float(vVe[j][1][0])),1):
                            dados[0] = float(vVe[j][1][2])

                        if auxDataM2 >= datetime(int(float(vVe[j][1][1])),int(float(vVe[j][1][0])),1):
                            dados[1] = float(vVe[j][1][2])


                #-------------------------------------------------------------------------------------------------------

                # Escreve registro VE ----------------------------------------------------------------------------------
                aux = 'VE' + ' ' * 2 + '{:>3}'.format(vUH[i][1]) + ' ' * 2

                for k in range(0,EstM1 + 1):

                    if k < EstM1:
                        aux = aux + str('{:5.1f}'.format(dados[0]))

                    else:
                        aux = aux + str('{:5.1f}'.format(dados[1])) + '\n'

                fileExport.write(aux)

                #-------------------------------------------------------------------------------------------------------
        #---------------------------------------------------------------------------------------------------------------

        # Bloco de configuracao do gerador de cenarios -----------------------------------------------------------------
        if DadosOriginais[i].strip() == '&   DADOS PARA O PROGRAMA CONFIGURADOR DO ARQUIVO DE CENARIOS DE VAZOES:':
            fileExport.write('&\n&   DADOS PARA O PROGRAMA CONFIGURADOR DO ARQUIVO DE CENARIOS DE VAZOES:\n&\n&\n&\n')
            fileExport.write('& VAZOES                              (COLUNAS: 40 A 70)\n')
            fileExport.write('& ARQ. DE VAZOES PREVISTAS - HIDROL => PREVS.RV0\n')
            fileExport.write('& HISTORICO DE VAZOES      - HIDROL => %d VAZOES.DAT\n' %(vAnos[0] - 2))
            fileExport.write('& ARQ. DE POSTOS           - HIDROL => POSTOS.DAT\n')
            fileExport.write('& MES INICIAL DO ESTUDO             => ' + '{:02d}'.format(vMeses[0]) + '{:>7}'.format(vAnos[0]) +  '\n')
            fileExport.write('& MES FINAL DO ESTUDO               => ' + '{:02d}'.format(vMeses[1]) + '{:>7}'.format(vAnos[1])  + '\n')
            fileExport.write('& ANO INICIAL DO ESTUDO             => ' + '{:4d}'.format(vAnos[0]) + '\n')
            fileExport.write('& NO. SEMANAS NO MES INIC. DO ESTUDO=> ' + '{:04d} 0000'.format(EstM1) + '\n')
            fileExport.write('& NO. DIAS DO MES 2 NA ULT. SEMANA  => ' + '{:1d}'.format(IntDiasMes2) + '\n')
            fileExport.write('& ESTRUTURA DA ARVORE               => %s\n' %(vConfigArvores))
            fileExport.write('& UTILIZA AGREGACAO                 => S\n')
            fileExport.write('& ORDEM MAXIMA PARP                 => 11\n')
            fileExport.write('& USA PROPAGACAO LINEAR             => 2\n')
            #-----------------------------------------------------------------------------------------------------------


    print ('Arquivo %s - PMO - %d / %d' %(strNomeArqv,vMeses[0],vAnos[0]))
    fileExport.close()
    return vUH, vAC

def fEscreveDadgnl(strPath, strArqv, strPathExport, EstM1, strDataInicial, vMeses, vFeriados):

    import os
    from datetime import datetime, timedelta

    contGS = contGL = 0
    ContT2 = ContT1 = 0

    strFullPath = os.path.join(strPath,strArqv)
    strFullPathExport = os.path.join(strPathExport,strArqv)

    file = open(strFullPath,'r')
    fileExport = open(strFullPathExport,'w')
    DadosOriginais = file.readlines()
    file.close()
    vHoras = []
    DataInicial = datetime.strptime(strDataInicial, '%d/%m/%Y')

    # Determinando Horas -----------------------------------------------------------------------------------------------
    for j in range(0, 9):  # 9 semanas de despacho antecipado
        semana = DataInicial
        for k in range(0, 7):  # 7 dias na semana

            if DataInicial in vFeriados or DataInicial.weekday() in [6]:  # Verificacao do tipo do dia
                ContT2 = ContT2 + 1  # Quantidade de dias tipo 2

            else:
                ContT1 = ContT1 + 1  # Quantidade de tipo 1

            DataInicial = DataInicial + timedelta(days=+ 1)

            if DataInicial.month > vMeses[1] and j == 8:
                break

        vEstagioAux = \
            [
                # Pesado , Medio , Leve
                0 * ContT2 + 3 * ContT1,
                5 * ContT2 + 14 * ContT1,
                19 * ContT2 + 7 * ContT1,
            ]
        vHoras.append([vEstagioAux,semana])
        ContT1 = ContT2 = 0  # Reinicializa contadores

    #-------------------------------------------------------------------------------------------------------------------


    # Escrevendo Arquivo dadgnl-----------------------------------------------------------------------------------------
    for i in range(0,len(DadosOriginais)):
        # Reescreve comentarios blocos ---------------------------------------------------------------------------------
        if DadosOriginais[i].find('BLOCO') != -1:

            for cab in range(-1,4,+1):
                fileExport.write(DadosOriginais[i + cab])
        #---------------------------------------------------------------------------------------------------------------

        # Blocos que serao apenas repetidos ----------------------------------------------------------------------------
        if DadosOriginais[i][0:2].strip() in ['TG','NL']:
            fileExport.write(DadosOriginais[i])
        #---------------------------------------------------------------------------------------------------------------

        # Blocos que serao reescritos ----------------------------------------------------------------------------------
        if DadosOriginais[i][0:2] in ['GS','GL']:
            # Bloco GS -------------------------------------------------------------------------------------------------
            if DadosOriginais[i][0:2] == 'GS' and contGS == 0:
                fileExport.write('GS   1   %d\n' %(EstM1))
                fileExport.write('GS   2   %d\n' % (9 - EstM1))
                fileExport.write('GS   3   %d\n' % (EstM1))
                contGS = 1
            #-----------------------------------------------------------------------------------------------------------

            # Bloco GL -------------------------------------------------------------------------------------------------
            if DadosOriginais[i][0:2] == 'GL':
                vAux = (' '.join(DadosOriginais[i].split())).split(' ')
                aux = \
                vAux[0] + ' ' * 2 + \
                '{:>3}'.format(vAux[1]) + ' ' * 2 + \
                '{:>2}'.format(vAux[2]) + ' ' * 3 + \
                '{:>2}'.format(vAux[3]) + ' ' * 3 + \
                '{:>10}'.format(vAux[4]) + \
                '{:>5}'.format(vHoras[int(float(vAux[3])) - 1][0][0]) + \
                '{:>10}'.format(vAux[6]) + \
                '{:>5}'.format(vHoras[int(float(vAux[3])) - 1][0][1]) + \
                '{:>10}'.format(vAux[8]) + \
                '{:>5}'.format(vHoras[int(float(vAux[3])) -1][0][2]) + ' ' * 1 + \
                vHoras[int(float(vAux[3])) - 1][1].strftime('%d%m%Y') + '\n'
                fileExport.write(aux)

                if int(float(vAux[3])) == 9:
                    fileExport.write('&\n')
            #-----------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------------------

    fileExport.close()
    return


def fEscreveExpansao(strPathExport, strNomeArqv, vExpansao, vMeses, vAnos, vUH, vAC):

    import os
    from datetime import date
    import locale

    locale.setlocale(locale.LC_ALL, '')                                     # utiliza informacoes locais
    strFullPath = os.path.join(strPathExport, 'dadger.new')
    file = open(strFullPath,'w')
    vDatas = [date(vAnos[0], vMeses[0], 1), date(vAnos[1], vMeses[1], 1)]   # Datas com estagios do primeiro e segundo mes
    flag = 0

    # Iterando sobre vetor do bloco AC ---------------------------------------------------------------------------------
    for i in range(len(vAC)):

        if vAC[i][2] in ['NUMCON']:

            # Primeiro mes ---------------------------------------------------------------------------------------------
            if len(vAC[i]) == 6:
                vAC[i][4] = date(vAnos[0], vMeses[0], 1).strftime('%b').upper() # Insere primeiro mes
                vAC[i].append(vAnos[0])                                         # Insere ano do primeiro mes
            # ----------------------------------------------------------------------------------------------------------

            # Segundo mes ----------------------------------------------------------------------------------------------
            else:
                vAC[i][4] = date(vAnos[0], vMeses[1], 1).strftime('%b').upper()  # Insere segundo mes
                vAC[i].append('')           # String vazia para indicar que nao coloca semana
                vAC[i].append(vAnos[1])     # Coloca ano da data de entrada
            # ----------------------------------------------------------------------------------------------------------

        if vAC[i][2] in ['POTEFE']:

            # Primeiro mes ---------------------------------------------------------------------------------------------
            if len(vAC[i]) == 7:
                vAC[i][5] = date(vAnos[0], vMeses[0], 1).strftime('%b').upper()  # Insere primeiro mes
                vAC[i].append(vAnos[0])  # Insere ano do primeiro mes
            # ----------------------------------------------------------------------------------------------------------

            # Segundo mes ----------------------------------------------------------------------------------------------
            else:
                vAC[i][5] = date(vAnos[0], vMeses[1], 1).strftime('%b').upper()  # Insere segundo mes
                vAC[i].append('')  # String vazia para indicar que nao coloca semana
                vAC[i].append(vAnos[1])  # Coloca ano da data de entrada
            # ----------------------------------------------------------------------------------------------------------

        if vAC[i][2] == 'NUMMAQ':

            if len(vAC[i]) == 7:                                                    # Identifica se e primeiro mes
                vAC[i][5] = date(vAnos[0], vMeses[0], 1).strftime('%b').upper()     # Insere segundo mes
                vAC[i].append(vAnos[0])                                             # Insere ano do primeiro mes
                vMaq = [0, 0]                                                       # Vetor de contador de maquinas

            else:
                vAC[i][5] = date(vAnos[1], vMeses[0], 1).strftime('%b').upper()  # Insere segundo mes
                vAC[i].append(vAnos[1])  # Insere ano do primeiro mes

                # Contagem de maquinas ---------------------------------------------------------------------------------
                for j in range(len(vExpansao)): # Itera sobre dados de expansao
                    vAux = vExpansao[j][1][0].split('/')    # Quebra para formar data do vetor de expansao

                    if len(vAux) >= 2:
                        x = date(int(float(vAux[1])), int(float(vAux[0])), 1)

                    # Primeiro mes -------------------------------------------------------------------------------------
                    if vAC[i][1] == vExpansao[j][0][0] \
                            and vDatas[0] >= date(int(float(vAux[1])), int(float(vAux[0])), 1) \
                            and vAC[i][3] == vExpansao[j][1][2]:
                        vMaq[0] = vMaq[0] + 1
                    # --------------------------------------------------------------------------------------------------

                    # Segundo mes --------------------------------------------------------------------------------------
                    if vAC[i][1] == vExpansao[j][0][0] \
                            and vDatas[1] >= date(int(float(vAux[1])), int(float(vAux[0])), 1) \
                            and vAC[i][3] == vExpansao[j][1][2]:
                        vMaq[1] = vMaq[1] + 1
                    # --------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------

                # Escrevendo expansao ---------------------------------------------------------------------------------
                if len(vAC[i]) == 8:    # Verifica se e primeiro mes
                    vAC[i][3] = str(int(float(vAC[i][3])) + vMaq[0])

                else:
                    vAC[i][3] = str(int(float(vAC[i][3])) + vMaq[1])
                #-------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    flagReescrita = 0
    fileBase = open(os.path.join(strPathExport, 'dadger.rv0'),'r')

    while True:
        linha = fileBase.readline()

        if not linha:
            break

        if linha[0:2] == 'AC' and flagReescrita == 0:
            flagReescrita = 1

            for i in range(len(vAC)):

                if vAC[i][2] in ['COFEVA']:
                    file.write('{:>2}  {:>3}  {:>6}      {:>4} {:>4}                         \n'.format(*vAC[i]))

                if vAC[i][2] in ['VOLMAX', 'VOLMIN']:
                    file.write('{:>2}  {:>3}  {:>6}    {:>10}\n'.format(*vAC[i]))

                if vAC[i][2] in ['JUSMED']:

                    if len(vAC[i]) == 6:
                        file.write('{:>2}  {:>3}  {:>6}    {:>10}                                        {:>3}  {:>1}\n'.format(*vAC[i]))

                    else:
                        file.write('{:>2}  {:>3}  {:>6}    {:>10}                                        {:>3}  \n'.format(*vAC[i]))

                if vAC[i][2] in ['NUMPOS', 'NUMJUS', 'JUSENA']:
                    file.write('{:>2}  {:>3}  {:>6}      {:>3}\n'.format(*vAC[i]))

                if vAC[i][2] in ['DESVIO']:
                    file.write('{:>2}  {:>3}  {:>6}      {:>3}    {:>6}\n'.format(*vAC[i]))

                if vAC[i][2] in ['VSVERT']:
                    file.write('{:>2}  {:>3}  {:>6}       {:>7}\n'.format(*vAC[i]))

                if vAC[i][2] in ['VAZMIN']:
                    if len(vAC[i]) > 3:
                        file.write('{:>2}  {:>3}  {:>6}       {:>9}                         \n'.format(*vAC[i]))

                    else:
                        file.write('{:>2}  {:>3}  {:>6}\n'.format(*vAC[i]))

                if vAC[i][2] in ['NUMCON']:

                    if flag == 0:
                        file.write('&-----------------------------------------------------------------------\n&'
                                   '                           EXPANSAO - Calculo automatico de expansao\n&'
                                   '------------------------------------------------------------------------\n')
                        flag = 1

                    file.write('{:>2}  {:>3}  {:>6}        {:>1}                                             {:>3}  {:>1} {:4d}\n'\
                               .format(*vAC[i]))

                if vAC[i][2] in ['POTEFE']:
                    file.write(
                        '{:>2}  {:>3}  {:>6}        {:>1}    {:>6}                                   {:>3}  {:>1} {:4d}\n' \
                        .format(*vAC[i]))

                if vAC[i][2] in ['NUMMAQ']:

                    if len(vAC[i])== 8:     # Identifica linha referente ao primeiro mes
                        file.write('{:>2}  {:>3}  {:>6}        {:>1}   {:>2}                                        {:>3}  {:>1} {:4d}\n'\
                                   .format(*vAC[i]))

                    else:
                        '{:>2}  {:>3}  {:>6}        {:>1}   {:>2}                                        {:>3}    {:>4}\n'\
                            .format(*vAC[i])

            #-------------------------------------------------------------------------------------------------------------------
        if linha[0:2] != 'AC':
            file.write(linha)


    fileBase.close()
    file.close()

    os.rename(src=os.path.join(strPathExport, 'dadger.rv0'),dst=os.path.join(strPathExport, 'dadger-old.rv0'))
    os.rename(strFullPath, os.path.join(strPathExport, 'dadger.rv0'))
    os.remove(os.path.join(strPathExport, 'dadger-old.rv0'))
    return
