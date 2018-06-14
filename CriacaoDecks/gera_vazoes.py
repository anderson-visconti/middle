def gerar(strPath, strNomeArquivo, strNomeArqvProj, intAnoInicial):

    strPathExport = strPath  # Caminho de exportacao (no caso, e o mesmo que o caminho de importacao)
    vProjecoes = []
    vDados = []
    vDadosNew = []

    # Leitura dos dados de vazoes projetadas -------------------------------------------------------------------------------
    file = open(os.path.join(strPath, strNomeArqvProj))

    for linha in file:
        aux = linha.split(';')

        for i in range(0, len(aux)):
            aux[i] = aux[i].strip() # Tira espacos em branco do vetor de string

        for i in range(2, len(aux)):
            aux[i] = aux[i][:-3]

        vProjecoes.append(aux)

    print('Valores projetados na memoria')
    # ----------------------------------------------------------------------------------------------------------------------

    # Leitura do VazoesC ---------------------------------------------------------------------------------------------------
    fileVazoes = open(os.path.join(strPath,strNomeArquivo),'r')

    for linha in fileVazoes:
        vDados.append((' '.join(linha.split())).split(' '))

    print('VazoesC na memoria')
    #-----------------------------------------------------------------------------------------------------------------------

    # Edicao do arquivo VazoesC --------------------------------------------------------------------------------------------
    for i in range(0, len(vDados)):
        vDadosNew.append(vDados[i])

        # Verifica se precisa fazer alteracao ------------------------------------------------------------------------------
        if int(float(vDadosNew[i][1])) == intAnoInicial:   # Itera ate achar o ano que precisa ser alterado

            for j in range(1, len(vProjecoes)):  # procura o posto no vetor de projecoes

                if int(float(vDadosNew[i][0])) == int(float(vProjecoes[j][0])):

                    for k in range(2, len(vDados[i])):    #Itera sobre o elemtento do vetor
                        vDadosNew[i][k] = vProjecoes[j][k]
        #-------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------

    # Escrita Arquivo VazoesC ----------------------------------------------------------------------------------------------
    fileExport = open(os.path.join(strPathExport,'vazoesc.new',), 'w')
    for i in range(0, len(vDadosNew)):
        aux = '{:>3} {:>4} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5}\n'.format(*vDadosNew[i])
        fileExport.write(aux)

        # Acrescenta um ano ------------------------------------------------------------------------------------------------
        if int(float(vDadosNew[i][1])) == intAnoInicial:
            vAux = vDadosNew[i]
            vAux[1] = str(intAnoInicial + 1)

            for i in range(2,len(vAux)):
                vAux[i] = '00'

            fileExport.write('{:>3} {:>4} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5}\n'.format(*vAux))


    fileExport.close()
    print('Arquivo vazoesC gerado \n')

# Variaveis-------------------------------------------------------------------------------------------------------------
#!/usr/bin/python
# - coding: utf-8 --
#
# O script acrescenta 1 ano apenas para facilitar ao ano inicial indicado e repete os valores
#
import os
strPath = [
    r'C:\Onedrive\Middle Office\Middle\Decks\Prospectivos\2018\06\p2\gevazp\vazoes',

]

strPathExport = strPath  # Caminho de exportacao (no caso, e o mesmo que o caminho de importacao)
strNomeArquivo = r'Vazoes-base.txt'  # Nome do arquivo base vazoesC
strNomeArqvProj = r'export-2018.txt'  # Nome do arquivo com vazoes projecoes
intAnoInicial = 2018  # Ano a ser alterado

for i in strPath:
    gerar(i, strNomeArquivo, strNomeArqvProj, intAnoInicial)
print('Fim')
print("-----------------------------------------------------------------------------------------------------")