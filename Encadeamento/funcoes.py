def fLeSumario(FullPath):

    ''''
    Funcao que le arquivo sumario e pega valores de dos armazenamentos individuais e por REE
    '''

    file = open(FullPath,'r') # Abre arquivo
    count = 0
    countArm = 0
    vUH = []    # Matriz n x 2, n - numero de postos
    vArmRee = [] # Matriz n x 3, n - numero de REEs

    while True:
        linha = file.readline()
        if not linha: break
        # ----------mnemonico para armazenamentos iniciais -------------------------------------------------------------
        if linha.strip() == 'VOLUME UTIL DOS RESERVATORIOS':    # mnemonico para armazenamentos iniciais
            count = 0

            while count < 3:    # quantidade de 'X' que indica inicio e fim da tabela
                aux = file.readline().strip()
                if aux[0] == 'X':   # verifica se linha comeca com 'X'
                    count = count + 1

                if count == 2 and aux[0] !='X': # entre cont 2 e 3 ficam os dados contidos na tabela
                    auxUH = ' '.join(aux.split())   # tira espacos multiplos
                    auxUH = auxUH.split(' ')    # parse na string baseado no ' '
                    vUH.append([auxUH[0],auxUH[len(auxUH)-2]]) # pega dados do codigo do posto e armazenamento final do horizonte
        # --------------------------------------------------------------------------------------------------------------

        # --------------- mnemonico para armazenamentos iniciais por REE -----------------------------------------------
        if linha.strip() == 'ENERGIA ARMAZENADA NOS REEs (% EARM_MAXIMA)':
            count = 0
            while count < 3:    # quantidade de 'X' que indica inicio e fim da tabela
                aux = file.readline().strip()
                if aux[0] == 'X':   # verifica se linha comeca com 'X'
                    count = count + 1

                if count == 2 and aux[0] !='X': # entre cont 2 e 3 ficam os dados contidos na tabela
                    auxRee = ' '.join(aux.split())   # tira espacos multiplos
                    auxRee = auxRee.split(' ')    # parse na string baseado no ' '
                    vArmRee.append([auxRee[0],auxRee[1],auxRee[len(auxRee)-1]]) # pega dados do codigo do posto e armazenamento final do horizonte
        # --------------------------------------------------------------------------------------------------------------
    return vUH, vArmRee;


def fLeRelato(FullPath):
    ''''
    Autor: Anderson Visconti
    Funcao que le arquivo relato e pega valores de dos armazenamentos individuais e por REE
    Variaveis
        vUH - Matriz n x 2 , n nuemro de postos
    '''

    file = open(FullPath + '/' + 'relato.rv0','r') # Abre arquivo
    count = 0
    vCadastro = []    # Matriz n x 2, n - numero de postos
    vArm = [] # Matriz de Armazenamento
    numEstagios = 0
    f = 0

    while True:
        linha = file.readline()
        if not linha: break
        # Determinando numero de estagios
        if linha[3:50].strip()=='Total de estagios':
            numEstagios = int(float(linha[57:58])) - 1

        # -----Leitura das configuracoes dos postos---------------------------------------------------------------------
        if linha.strip() == 'Relatorio  dos  Dados  do  Cadastro  das  Usinas  Hidraulicas na Configuracao - a partir do estagio:  1 (ALTCAD)':
            count = 0
            while count < 3:  # quantidade de 'X' que indica inicio e fim da tabela
                aux = file.readline()
                if aux.strip()[0] == 'X':  # verifica se linha comeca com 'X'
                    count = count + 1

                if count == 2 and aux.strip()[0] != 'X':  # entre cont 2 e 3 ficam os dados contidos na tabela
                    auxCadastro = [int(float(aux[4:7].strip())), aux[8:20].strip(), int(float(aux[25:29].strip()))]
                    vCadastro.append(auxCadastro)
        # --------------------------------------------------------------------------------------------------------------

        # -------------Leitura dos armazenamentos da ultima semana -----------------------------------------------------
        if linha[15:24].strip() == 'SEMANA %s' %(numEstagios) and f == 0:
            count = 0
            while count < 3:    # entre 2 X e 3 ficam os dados
                aux = file.readline()

                if aux.strip()[0:1] == 'X':
                    count = count + 1

                if count == 2 and aux.strip()[0:1] != 'X':  # entre cont 2 e 3 ficam os dados contidos na tabela

                    if aux[33:38].strip() != '':
                        auxArm = [int(float(aux[4:8].strip())), aux[9:21].strip(), float(aux[33:38].strip())]

                    else:
                        auxArm = [int(float(aux[4:8].strip())), aux[9:21].strip(), 0.0]

                    vArm.append(auxArm)
            f = 1
            vArm = vArm[:-4]    # retira 4 ultimas linhas (estacoes elevatorias)
        # --------------------------------------------------------------------------------------------------------------
    print('Cadastro dos postos e armazenamtos para o final do mes capturados (Estagio %s)' %(numEstagios))
    return vCadastro,vArm;

def fEscreveDadger(Path, NomeArqv, vUH):

    '''
    Autor: Anderson Visconti
    Versao 0
    Funcao que escreve valores de armazenamento no arquivo dadger
    '''

    import os

    FullPath = Path + '/' + NomeArqv
    OldFile = open(FullPath,'r')                    # Abre arquivo em modo leitura
    NewFile = open(Path + '/' + 'dadger.new','w+')  # Abre arquivo em modo escrita
    aux =[]
    for linha in OldFile:

        if linha.strip()[0:2] == 'UH':  # Escrita Bloco UH
            aux = (' '.join(linha.split())).split(' ')

            posto = linha[4:8].strip()

            for i in range(0,len(vUH)): # Procura novo armazenamento

                if vUH[i][0] == int(float(posto)):
                    aux[3] = float(vUH[i][2])
                    break

            NewFile.write('{0:>2}  {1:>3}  {2:>2}       {3:6.2f}               {4:>1}\n'.format(*aux))

        else:
            NewFile.write(linha)

    OldFile.close()
    NewFile.close()
    os.rename(Path + '/' + NomeArqv, Path + '/' + '~' + NomeArqv)
    os.rename(Path + '/' + 'dadger.new', Path + '/' + NomeArqv)
    os.remove(Path + '/' + '~' + NomeArqv)
    print('Bloco UH atualizado')
    return

def fEscreveDger(Path, Arqv, vArmRee):
    'Funcao que escreve dados de armazenamento no arquivo dger (regua de armazenamento por REE)'

    import os

    FullPath = Path + '/' + Arqv
    OldFile = open(FullPath,'r')
    NewFile = open(Path + '/' + 'dger.new','w')
    flag = 0
    strArm = ''

    for linha in OldFile:

        if linha.strip()[0:19] == 'CALCULA VOL.INICIAL':    # Configura Dger para arm inicial na regua e nao no confhd
            NovaLinha = linha.replace(linha[24:25],'0') # Flag para utilizar a regua
            flag = 1    # Ativa escrita da nova linha

        if linha.strip()[0:14] == 'POR SUBSISTEMA': # Armazenamentos iniciais por REE

            for i in range(0,len(vArmRee)):
                strArmsAux = ' ' * (5 - len(vArmRee[i][2])) + vArmRee[i][2] + ' ' * 2
                strArm = strArm + strArmsAux

            NovaLinha = ' POR SUBSISTEMA      ' + strArm + '\n'
            flag = 1  # Ativa escrita da nova linha

        # Reescrevendo arquivo dger.dat

        if flag == 0:
            NewFile.writelines(linha)  # Escreve linha sem alteracao

        else:
            NewFile.writelines(NovaLinha)  # Escreve com novo armazenameno por REE
            flag = 0

    OldFile.close()
    NewFile.close()
    os.rename(Path + '/' + Arqv, Path + '/' + '~' + Arqv)
    os.rename(Path + '/' + 'dger.new', Path + '/' + Arqv)
    os.remove(Path + '/' + '~' + Arqv)
    print('Arquivo Dger.dat reescrito com novos armazenamentos')

    return

def fEscreveConfhd(Path, vUH, vCadastro):
    '''
    Autor: Anderson Visconti
    Funcao que escreve armazenamentos no arquivo confhd
    '''

    import os

    FullPath = Path + '/' + 'confhd.dat'
    OldFile = open(FullPath, 'r')
    NewFile = open(Path + '/' + 'confhd.new', 'w')
    cont = 0

    for linha in OldFile:
        cont = cont + 1
        NovaLinha = linha

        if cont > 2:
            usina = int(float(linha[1:5].strip()))
            nome = linha[6:19].strip()
            posto = int(float(linha[19:24].strip()))
            fator = 1.0

            if nome[0:4] == 'FICT':

                if usina == 291:    # serra da mesa ficticia 0.55 do valor de serra da mesa
                    fator = 0.55

                for i in range(0,len(vCadastro)):   # procura pela usina original para substituicao

                    if posto == vCadastro[i][2]:
                        usina = int(float(vCadastro[i][0]))
                        break

            for i in range(0,len(vUH)):

                if usina == vUH[i][0]:
                    arm = '{0:6.2f}'.format(vUH[i][2] * fator)
                    NovaLinha = linha.replace(linha[35:41],arm)
                    break

        NewFile.writelines(NovaLinha)

    OldFile.close()
    NewFile.close()
    os.rename(FullPath,Path + '/' + '~confhd.dat')
    os.rename(Path + '/' + 'confhd.new',FullPath)
    os.remove(Path + '/' + '~confhd.dat')
    print ('Arquivo confhd.dat atualizado com sucesso')
    return

def fEncadeamento(Path, PathScript, nProc, nNos, numVersaoNewave, numVersaoDecomp, iniciaMPD, fileNos, dBinarios,
                  lista_email) :
    '''
    Autor: Anderson Visconti
    Versao: 0
    Funcao gerar encadeamento Newave-Decomp-Newave
    Variavies
        Path - String de Caminho ate os cenarios
        PathScript - String do caminho de onde estao os arquivos auxiliares nwlistop e deco.prm
        nProc - String de Numero de processadores ex: '16'
        numVersaoNewave - String da Versao do Newave a ser rodada ex: '22'
        numVersaoDecomp - String de Numero da versao do decomp a ser rodada ex: '24'
    '''

    import os

    # Inicia MPD -------------------------------------------------------------------------------------------------------
    if iniciaMPD == 1:  # Caso flag, iniciara processo MPDBOOT
        fIniciaMPD(PathScript=PathScript, nNos=nNos, fileNos=fileNos)
    # ------------------------------------------------------------------------------------------------------------------

    for cenarios in os.listdir(Path):                       # Iteracao entre cenarios
        vResultados = []                                    # Inicializa vetor de resultados
        vArmazenamentos = []                                # Inicializa vetor com armazenamentos
        flag = 0                                            # flag para pular o primeiro mes de cada cenario
        PathL1 = os.path.join(Path, cenarios)
        listaMes = os.listdir(PathL1)

        for i in range(0, len(listaMes)):                    # Ordena pastas para excecucao em sequencia
            listaMes[i] = int(float(listaMes[i]))
            print(listaMes[i])
        listaMes.sort()
        print(listaMes)

        for meses in range(0, len(listaMes)):                # itercao entre meses em cada cenario
            PathL2 = os.path.join(os.path.join(Path, cenarios), str(listaMes[meses]))
            # Executanto processo do newave ----------------------------------------------------------------------------
            print ('Executando Newave do cenario %s do mes %s' %(cenarios,meses + 1))
            print ('cd %s' %(os.path.join(PathL2, 'newave')))
            os.chdir((os.path.join(PathL2, 'newave')))                          # Entra na pasta
            os.system('cp {0} ./'.format(os.path.join(PathScript, fileNos)))     # Copia arquivo com nos para pasta

            if flag >= 1:   # Pula o primeiro mes
                print ('Escrevendo armazenamentos no arquivo confhd.dat')
                #fEscreveDger(Path=os.path.join(PathL2,'newave'),Arqv='dadger.rv0',vArmRee=vArmRee)  # Escreve armazenamento no dger.dat
                os.system('{0}/ConverteNomesArquivos'.format(dBinarios['newave']))  # Converte arquivos para minusculo e unix
                fEscreveConfhd(Path=os.path.join(PathL2, 'newave'), vUH=vArm, vCadastro=vCadastro)

            print ((os.path.join(PathL2, 'newave')))
            os.system('{0}/ConverteNomesArquivos'.format(dBinarios['newave'])) # Converte arquivos para minusculo e unix
            os.system('mpiexec -n %s %s/newave%s_L >> log.txt' %(nProc, dBinarios['newave'], numVersaoNewave)) # executa newave
            #os.system('mpiexec -n %s -f %s %s/newave%s_L >> log.txt' %(nProc, fileNos, dBinarios['newave'], numVersaoNewave)) # executa newave
            os.system('cp %s ./' %(os.path.join(PathScript, 'nwlistop.dat')))    # copia arquivo nwlisotp.dat
            os.system('{0}/nwlistop{1}_L >> log.txt'.format(dBinarios['newave'], numVersaoNewave))   #executa nwlitop.dat
            # ----------------------------------------------------------------------------------------------------------

            # Executando processos do decomp ---------------------------------------------------------------------------
            print ('Executando Decomp do cenario %s do mes %s' % (cenarios, listaMes[meses]))
            os.chdir((os.path.join(PathL2, 'decomp')))  # Entra na pasta
            os.system('cp {0} ./'.format(os.path.join(PathScript, fileNos)))  # Copia arquivo com nos para pasta

            if flag >= 1:  # Pula o primeiro mes
                print ('Escrevendo armazenamentos no dadger.rv0')
                os.system('{0}/convertenomesdecomp_{1}'.format(dBinarios['decomp'], numVersaoDecomp))
                fEscreveDadger(Path=os.path.join(PathL2, 'decomp'), NomeArqv='dadger.rv0', vUH=vArm)  # Escreve armazenamento no dadger.rv0

            print((os.path.join(PathL2, 'decomp')))
            os.system('{0}/convertenomesdecomp_{1}'.format(dBinarios['decomp'], numVersaoDecomp))
            os.system('cp %s ./' %(os.path.join(PathScript,'deco.prm')))
            os.system('mpiexec -n %s %s/decomp_%s >> log.txt' % (nProc, dBinarios['decomp'], numVersaoDecomp))
            [vResultados, vArmazenamentos] = fResultadosDecomp(strPath=PathL2, cenarios=cenarios,
                                                               listaMes=listaMes[meses], vResultados=vResultados,
                                                               vArmazenamentos=vArmazenamentos)

            [vCadastro, vArm] = fLeRelato(os.path.join(PathL2,'decomp'))     # Pega dados do relato.v0
            #[vUH,vArmRee] = fLeSumario((os.path.join(PathL2, 'decomp')))   # Le sumario.rv0 (funcao existe, porem nao usada)
            # ----------------------------------------------------------------------------------------------------------
            flag = flag + 1

        print ('Decks de Newave e Decomp do mes %s do cenario %s executados' %(meses,cenarios))
        fCriaArquivCSV(PathL1=PathL1, vResultados =vResultados, cenarios=cenarios, vArmazenamentos=vArmazenamentos)  # Cria arquivo CSV com dados do cenario rodaddo
        fEnviaEmail(cenarios=cenarios, listaMes=listaMes, PathL1=PathL1, lista_email=lista_email)  # Envia e-mail de acompanhamento

    print('Casos executados com sucesso')

    # para nos alocados MPD --------------------------------------------------------------------------------------------
    if iniciaMPD == 1:
        os.system('mpdallexit')
    #------------------------------------------------------------------------------------------------------------------
    return

def fCvar(Path,PathScript,nProc):
    '''
    Autor: Anderson Visconti
    Versao: 0
    Funcao gerar encadeamento Newave-Decomp-Newave
    Variavies
        Path - String de Caminho ate os cenarios
        PathScript - String do caminho de onde estao os arquivos auxiliares nwlistop e deco.prm
        nProc - String de Numero de processadores ex: '16'
    '''

    import os
    import subprocess

    for cenarios in os.listdir(Path): # iteracao entre cenarios
        flag = 0  # flag para pular o primeiro mes de cada cenario
        PathL1 = os.path.join(Path, cenarios)
        listaMes = os.listdir(PathL1)

        for i in range(0,len(listaMes)):
            listaMes[i] = int(float(listaMes[i]))
        listaMes.sort()

        for meses in range(0,len(listaMes)):  # itercao entre meses em cada cenario
            PathL2 = os.path.join(os.path.join(Path,cenarios),str(listaMes[meses]))
            # Executanto processo do newave ----------------------------------------------------------------------------
            print ('Executando Newave do cenario %s do mes %s' %(cenarios,meses + 1))
            print ('cd %s' %(os.path.join(PathL2,'newave')))

            os.chdir((os.path.join(PathL2,'newave')))   # Entra na pasta
            print ((os.path.join(PathL2,'newave')))
            os.system('/usr/bin/ConverteNomesArquivos') # Converte arquivos para minusculo e unix

            # Pega versao do newave ------------------------------------------------------------------------------------
            fileDger = open(PathL2 + '/' + 'newave/' + 'dger.dat','r')
            numVersaoNewave = fileDger.readline()[-3:].strip()
            fileDger.close()
            #-----------------------------------------------------------------------------------------------------------

            os.system('mpiexec -n %s /usr/bin/newave%s_L' %(nProc,numVersaoNewave)) # executa newave
            os.system('cp %s ./' %(os.path.join(PathScript,'nwlistop.dat')))    # copia arquivo nwlisotp.dat
            os.system('/usr/bin/nwlistop%s_L' %(numVersaoNewave))   #executa nwlitop.dat
            # ----------------------------------------------------------------------------------------------------------

            # Executando processos do decomp ---------------------------------------------------------------------------
            print ('Executando Decomp do cenario %s do mes %s' % (cenarios, listaMes[meses]))
            os.chdir((os.path.join(PathL2, 'decomp')))
            os.system('/usr/bin/convertenomesdecomp_24')
            # Pegando versao do decomp ---------------------------------------------------------------------------------
            fileRelato = open(PathL2 + '/' + 'decomp/' + 'relato.rv0')

            for i in range(0,3):
                linha = fileRelato.readline()

            numVersaoDecomp = linha[59:61].strip()
            print(numVersaoDecomp)
            fileRelato.close()
            #-----------------------------------------------------------------------------------------------------------

            os.system('cp %s ./' %(os.path.join(PathScript,'deco.prm')))
            os.system('mpiexec -n %s /usr/bin/decomp_%s' % (nProc, numVersaoDecomp))
            # ----------------------------------------------------------------------------------------------------------
            print ('Decks de Newave e Decomp do mes %s do cenario %s executados' %(listaMes[meses],cenarios))

    print ('Casos executados com sucesso')

    return

def fIniciaMPD(PathScript, nNos, fileNos):

    import os
    fullpath = os.path.join(PathScript, fileNos)    # string completa com para o arquivo com nos
    os.chdir('{0}'.format(PathScript))
    #os.system('cd {}'.format(PathScript))
    os.system('mpdboot -n {0} -f {1}'.format(nNos, fileNos))

    return

def fEnviaEmail(cenarios, listaMes, PathL1, lista_email):

    import os
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    import datetime

    vDados = [PathL1, cenarios, listaMes, datetime.datetime.now()]
    filename = r'precos-{0}.csv'.format(cenarios)
    filename_arm = r'armazenamentos-{0}.csv'.format(cenarios)
    f = file(os.path.join(PathL1, filename))
    f_arm = file(os.path.join(PathL1, filename_arm))
    attachment = MIMEText(f.read())                     # criando anexo
    attachment_arm = MIMEText(f_arm.read())  # criando anexo
    FromEmail = 'multivac.gerenciador@gmail.com'        # email que enviara
    password = '@brate01'                               # senha para autenticacao no servidor de email
    servidor = 'smtp.gmail.com'                         # Servidor smpt
    porta = 587                                         # porta do servidor
    toEmail = lista_email                               # email(s) de envio
    msg = MIMEMultipart()
    msg['From'] = FromEmail
    msg['To'] = ", ".join(toEmail)
    msg['Subject'] = "Sistema de Gerenciamento Multivac 2000"

    # Criacao da mensagem --------------------------------------------------------------------------------------------
    body = '''
    Email de acompanhamento referente ao caso:\n
    Caminho: {0}
    Cenario: {1}
    Mes: {2}
    Horario: {3:%d-%m-%Y %H:%M}


    ** Obs: e-mail enviado de forma automatica. Em caso de bugs, entre em contato com o administrador
    '''.format(*vDados)

    msg.attach(MIMEText(body, 'plain'))                                                 # Anexa mensagem no corpo do email
    attachment_arm.add_header('Content-Disposition', 'attachment', filename=filename_arm)  # Anexa arquivo CSV de armazenamentos
    msg.attach(attachment_arm)  # Anexa arquivo CSV de armazenamentos

    attachment.add_header('Content-Disposition', 'attachment', filename=filename)       # Anexa arquivo CSV
    msg.attach(attachment)                                                              # Anexa arquivo CSV


    # ------------------------------------------------------------------------------------------------------------------

    # Envio da mensagem ------------------------------------------------------------------------------------------------
    server = smtplib.SMTP(servidor, porta)
    server.starttls()
    server.login(FromEmail, password)
    text = msg.as_string()
    server.sendmail(FromEmail, toEmail, text)
    server.quit()
    # ------------------------------------------------------------------------------------------------------------------
    return

def fResultadosDecomp(strPath, cenarios, listaMes, vResultados, vArmazenamentos):

    import os
    cont = 0

    #vResultados = []
    arm_final = vArmazenamentos
    cont_subsistema = 1
    # Leitura dados decomp -------------------------------------------------------------------------------------------------
    strPathDecomp = os.path.join ((os.path.join(strPath,'decomp')), 'relato.rv0') #(os.path.join(strPath,'decomp'))
    fileDecomp = open(strPathDecomp,'r')
    #fileExportDecomp = open(os.path.join(strPath,'custo.txt'),'w')
    for linha in fileDecomp:

        if linha.find('SEMANA {0:d}'.format(cont + 1)) != -1:
            cont = cont + 1

        if linha.find('Custo marginal de operacao do subsistema') != -1:
            vResultados.append([cenarios,
                               listaMes,
                               cont,
                               linha[44:46].strip(),
                               linha[47:69].strip()]
                               )

    # ----
        if linha.find('%EARM') != -1:
            arm_final.append([cenarios, listaMes, cont, cont_subsistema, float(linha[66:71].strip())/100

            ])
            cont_subsistema += +1

        if cont_subsistema > 4:    # reinicia contagem dos subsistemas
            cont_subsistema = 1
    #-------------------------------------------------------------------------------------------------------------------
    fileDecomp.close()
#-----------------------------------------------------------------------------------------------------------------------
    return vResultados, arm_final

def fCriaArquivCSV(PathL1, vResultados, cenarios, vArmazenamentos):

    import os
    strFullPath = os.path.join(PathL1,'precos-{0}.csv'.format(cenarios))
    full_path_arm = os.path.join(PathL1,'armazenamentos-{0}.csv'.format(cenarios))
    file = open(strFullPath, 'w')
    file_arm = open(full_path_arm, 'w')
    file.write('cenario;mes;semana;subsistema;preco\n')
    file_arm.write('cenario;mes;semana;subsistema;armazenamento\n')

    for linha in vResultados:
        linha[4] = linha[4].replace(".", ",")
        file.write('{0};{1};{2};{3};{4}\n'.format(*linha))

    file.close()

    for linha in vArmazenamentos:
        file_arm.write('{0};{1};{2};{3};{4}\n'.format(*linha))

    file_arm.close()
    return

def fRodaGevazp(path_base, path_caso, mes, ano,):
    '''

    :param path_base:
    :param path_caso:
    :param mes:
    :param ano:
    :return:
    '''
    import os

    gevazp_dat = open(os.path.join(path_base, 'gevazp.dat'))

    return