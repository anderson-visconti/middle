#!/usr/bin/python
# *- coding: utf-8 -*-
__author__ = 'Anderson Visconti'
'''
Script principal com as configuracoes para geracao de decks rv0 prospectivos
'''
from fCriacao import *

# Caminhos -------------------------------------------------------------------------------------------------------------
# Caminho para onde estao os arquivos que servirao de base
strPath = r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2017\01\0-base'
# Caminho para exportacao dos arquivos criados
strPathExport = r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2017\01\0-base\201705'
# ----------------------------------------------------------------------------------------------------------------------

# Variaveis de Configuracao---------------------------------------------------------------------------------------------
intAnoInicial = 2017                    # Ano Inicial do Deck do Newave a ser baseado
intAnoFinal = 2021                      # Ano Final do Deck do Newave a ser baseado
strDataInicial = '29/04/2017'           # Data Inicial do PMO a ser gerado
vMeses = [5, 6]                        # Vetor com meses do PMO a ser gerado [0] - Mes do estagio 1 e [1] - Mes do ultimo estagio
vAnos = [2017, 2017]                    # Vetor com Anos do PMO a ser gerado [0] - Ano do estagio 1 e [1] - Ano do ultimo estagio
EstM1 = 5                               # Numero de semanas do primeiro mes do PMO a ser gerado
vRee = [1, 6, 7, 5, 10, 2, 3, 4, 8]     # Ordem dos REEs
# ----------------------------------------------------------------------------------------------------------------------
# Leitura dos dados no pmo.dat
[vMercado, vPequenas, vConfigTerm, vMinTermica, vMaxTermica,
 vProgTermica, vForcadaTermica, vCustoTermica, vMercadoAdic] = fLePmoDat(strPath, 'pmo.dat')
# Leitura do arquivo patamar.dat
[vDuracao, vCargaPU] = fLePatamarDat(strPath, 'patamar.dat', intAnoInicial, intAnoFinal)
# Carrega arquivo de feridados
vFeriados = fCarregaFeriados(strPath, 'feriados.csv', ';')
# Determina Horas para Bloco DP
[vBlocoDP, IntDiasMes2] = fCalculaEstagios(strDataInicial=strDataInicial, vMeses=vMeses, EstM1=EstM1, vFeriados=vFeriados,vAnos=vAnos)
# Le Arquivo dsvagua.dat
vDesvAgua = fLeDesvAguaDat(strPath=strPath, strNomeArqv='DSVAGUA.DAT')
# Le arquivo CadUhs
vDadosHidro = fLeCadUHs(strPath, strNomeArqv='CadUsH_A03-2016.csv', strDelimitador=';')
# Carrega configuracao de cenarios sinteticos
vConfigArvore = fLeConfigArvores(strPath=strPath , strArqv='arvores.csv', strDelimitador=';')
# Carrega configuracao do volume de espera
vVE = fLeModifDat(strPath, 'MODIF.DAT')
# Carrega dados de expansao
vExpansao = fLeExpH(strPath,'EXPH.DAT')

[vUH, vAC] = fEscreveDadger(strPathSource=strPath, strPathExport=strPathExport, strNomeArqv='dadger.rv0', vMeses=vMeses,
                            vAnos=vAnos, vConfigTerm=vConfigTerm, vMinTermica=vMinTermica,
                            vMaxTermica=vMaxTermica, vCustoTermica=vCustoTermica, EstM1=EstM1, vCargaPU=vCargaPU,
                            vBlocoDP=vBlocoDP, IntDiasMes2=IntDiasMes2, vMercado=vMercado, vPequenas=vPequenas,
                            vDesvAgua=vDesvAgua, vDadosHidro=vDadosHidro, vConfigArvores=vConfigArvore[vMeses[0]][1],
                            vRee=vRee, vVe=vVE
                            )

fEscreveDadgnl(strPath, 'dadgnl.rv0', strPathExport, EstM1, strDataInicial, vMeses, vFeriados)
#fEscreveExpansao(strPathExport=strPathExport, strNomeArqv='dadger.rv0', vExpansao=vExpansao, vMeses=vMeses, vAnos=vAnos,
                 #vAC=vAC, vUH=vUH)
print ('Fim')