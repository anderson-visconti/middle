#!/usr/bin/env python
# *- coding: utf-8 -*-
class Gerenciador:
    def __init__(self, paths, nomes, config_servidor):
        self.paths = paths
        self.nomes = nomes
        self.config_servidor = config_servidor
        self.resultados = pd.DataFrame()
        return


    def listar_casos(self):
        self.aux = map(int, os.listdir(self.paths['decks_gevazp']))
        self.lista = []
        for i in self.aux:
            self.lista.append({'cenario': i,
                               'caminho': os.path.join(self.paths['decks_gevazp'], str(i))
                               })
        self.lista = pd.DataFrame.from_dict(self.lista)
        return self


    def executar_decomp(self):
        # itera sobre todos os cenarios
        for i in self.lista.iterrows():
            # Copiar arquivos decomp_base para pasta
            for j in  glob.glob(os.path.join(self.paths['decomp_base'], '*')):
                shutil.copy(src=j, dst=i[1].caminho)

            # Copia licenca
            shutil.copy(src=os.path.join(self.config_servidor['path_lic'], self.config_servidor['lic_decomp']),
                        dst=i[1].caminho)

            # Entra na pasta e executa decomp
            print('Preparacao para executar {}'.format(i[1].caminho))
            os.chdir(i[1].caminho)
            #FNULL = open(os.devnull, 'w')
            print('Execucao do decomp para {}'.format(i[1].caminho))
            stdout = open(os.path.join(i[1].caminho, 'stdout.txt'), 'w')    # arquivo para saida
            stderr = open(os.path.join(i[1].caminho, 'stderr.txt'), 'w')    # arquivo para saida de erros
            retcode = subprocess.call(['convertenomesdecomp_{}'.format(self.config_servidor['versao_decomp'])
                                       ],
                                      stdout=stdout,
                                      stderr=stderr,
                                      shell=True
                                      )
            retcode = subprocess.call(['mpiexec -n {} {}/decomp_{}'.format(self.config_servidor['n_proc'],
                                                                           self.config_servidor['path_exec'],
                                                                           self.config_servidor['versao_decomp']
                                                                           )
                                       ],
                                     stdout=stdout,
                                     stderr=stderr,
                                     shell=True
                                      )
            stdout.close()
            stderr.close()
            if retcode == 1:
                print('Erro ao executar cenario -> {}'.format(i[1].caminho))
            else:
                print('Execucao completa cenario -> {}'.format(i[1].caminho))
                #  pega dados
                self.pegar_resultado(cenario=i[1].cenario)
                self.exportar_resultados()

            #  remove todos os arquivos execeto relato.rv0 e prevs.rv0 e vazoes.rv0
            for j in os.listdir(i[1].caminho):
                if j not in  ['relato.rv0', 'prevs.rv0', 'vazoes.rv0']:
                    os.remove(os.path.join(i[1].caminho, j))

            s = """---------------------------------------------------------------------------------------\n"""
            print(s)
        return


    def pegar_resultado(self, cenario):
        print('Capturando resultados do cenario {}'.format(cenario))
        relato = open(os.path.join(self.paths['decks_gevazp'], str(cenario), 'relato.rv0'), 'r')
        submercado = 1
        cont = 0
        cont_ena = 1
        dados_ena = []
        dados_preco = []
        ena = {'submercado': 0.0,
               'cenario': 0.0,
                'ena': 0.0,
               }
        preco = {'submercado': 0.0,
               'cenario': 0.0,
               'preco': 0.0,
               }
        for linha in relato:
            if linha.strip() == 'RELATORIO  DO  BALANCO  ENERGETICO':
                cont += 1

            if cont > 1:
                break

            if linha[0:12].strip() == 'EAR_ini' and cont_ena <=4:    # pega ENA
                dados_ena.append([cenario, submercado, float(linha[37:43].strip())])
                submercado += 1
                cont_ena += 1

                if submercado > 4:
                    submercado = 1

            if linha[0:44].strip() == 'Custo marginal de operacao do subsistema':   # pega PLDs
                if linha[44:46].strip() != 'FC':
                    dados_preco.append([cenario, submercado, float(linha[56:69].strip())])
                    submercado += 1

                    if submercado > 4:
                        submercado = 1

        x = pd.DataFrame(data=dados_ena, columns=['cenario', 'submercado', 'ena'])
        y = pd.DataFrame(data=dados_preco, columns=['cenario', 'submercado', 'preco'])
        self.resultados =pd.concat([self.resultados, pd.merge(x, y, on=['cenario', 'submercado'])])
        return self


    def exportar_resultados(self):
        self.resultados.to_csv(os.path.join(self.paths['export'], 'resultados.csv'),
                               sep=';', decimal=',')

        print('Resultado exportado para {}'.format(self.paths['export']))
        return


class Casos:
    def __init__(self, paths, nomes):
        self.paths = paths
        self.nomes = nomes
        return

    def ler_vazoes(self, sep, decimal, mes):
        df = pd.read_csv(filepath_or_buffer=os.path.join(self.paths['vazoes_gevazp'], self.nomes['vazoes']),
                         sep=sep, decimal=decimal)
        df = df.rename(columns=lambda x: x.strip())
        df.set_index(keys=['CENA', 'POSTO'], inplace=True)
        df = pd.DataFrame(df.loc[:, [str(mes)]])
        self.dados = df
        return self


    def gerar_arquivos(self):
        print('qualquer coisa')

        return


    def gerar_ambiente(self):
        c = self.dados.index.levels[0].values
        for i in self.dados.index.levels[0].values:
            if os.path.isdir(r'{}/{}'.format(self.paths['decks_gevazp'], i)) == True:
                shutil.rmtree(r'{}/{}'.format(self.paths['decks_gevazp'], i))

            os.mkdir(r'{}/{}'.format(self.paths['decks_gevazp'], i))

        print('Ambiente de pastas criado em {}'.format(self.paths['decks_gevazp']))
        return self


    def gerar_prevs(self):
        s = '''{:>6d}{:>5d}{:>10d}{:>10d}{:>10d}{:>10d}{:>10d}{:>10d}\n'''

        ordem = [1, 2, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 22, 23, 24, 25, 28, 31, 32, 33, 34, 47, 48, 49, 50,
                 51, 52, 57, 61, 62, 63, 71, 72, 73,
                 74, 76, 77, 78, 89, 92, 93, 94, 97, 98, 99, 101, 102, 103, 110, 111, 112, 113, 114, 115, 117, 120, 121,
                 122, 123, 125, 129, 130, 134, 141, 144, 145, 148, 149, 155, 156, 158, 161, 168, 169, 172, 173, 175,
                 178, 183,
                 188, 190, 191, 196, 197, 198, 201, 202, 203, 204, 205, 206, 207, 209, 211, 215, 216, 217, 220, 222,
                 229, 237, 238, 239, 240,
                 241, 242, 244, 245, 246, 247, 248, 249, 251, 253, 254, 255, 257, 259, 261, 262, 263, 266, 269, 270,
                 271, 273, 275,
                 277, 278, 279, 280, 281, 283, 284, 285, 288, 286, 287, 290, 291, 294, 295, 296, 297, 301]

        for i in self.dados.index.levels[0].values:
            k = 1
            file = open(r'{}/{}/{}'.format(self.paths['decks_gevazp'], i, 'prevs.rv0'), 'w')
            aux = pd.DataFrame(self.dados.loc[i, :, :])
            for j in ordem:
                vazao = abs(int(math.ceil(self.dados.loc[i, j, :][str(mes)].values[0])))
                file.write(s.format(k, j, vazao, vazao, vazao, vazao, vazao, vazao))
                k += 1

            # for j in aux.iterrows():
            #    vazao =abs(int(j[1].values[0]))
            #    file.write(s.format(k, j[0], vazao, vazao, vazao, vazao, vazao, vazao))
            #    k += 1


            file.close()

        print('Arquivos prevs criados')
        return self


    def calcula_postos(self, mes):
        x = [237, 240, 242, 238, 239, 245, 244, 246, 129, 202, 130, 125, 201, 203, 117, 301, 266, 76, 288, 34]
        df_posto = pd.DataFrame(data=[], columns=['CENA', 'POSTO', str(mes)])

        for j in self.dados.index.levels[0].values:
            for i in x:
                if i == 237:  # igual ao posto 37
                    aux = pd.DataFrame(data=[(j, 237, self.dados.loc[j, 37][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])

                if i == 240:  # igual 40
                    aux = pd.DataFrame(data=[(j, 240, self.dados.loc[j, 40][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 242:  # igual 42
                    aux = pd.DataFrame(data=[(j, 242, self.dados.loc[j, 42][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 238:  # igual 38
                    aux = pd.DataFrame(data=[(j, 238, self.dados.loc[j, 38][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])

                if i == 239:  # igual 39
                    aux = pd.DataFrame(data=[(j, 239, self.dados.loc[j, 39][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])

                if i == 245:  # igual 45
                    aux = pd.DataFrame(data=[(j, 245, self.dados.loc[j, 45][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 244:  # igual 44
                    aux = pd.DataFrame(data=[(j, 244, self.dados.loc[j, 44][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 246:  # igual 46
                    aux = pd.DataFrame(data=[(j, 246, self.dados.loc[j, 46][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 129:  # igual 130 = # igual 126
                    aux = pd.DataFrame(data=[(j, 129, self.dados.loc[j, 126][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 202:  # igual 130 = # igual 132
                    aux = pd.DataFrame(data=[(j, 202, self.dados.loc[j, 132][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 130:  # igual 299
                    aux = pd.DataFrame(data=[(j, 130, self.dados.loc[j, 299][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 125:  # igual 21
                    aux = pd.DataFrame(data=[(j, 125, self.dados.loc[j, 21][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 201:  # tocos igual a qualquer valor
                    aux = pd.DataFrame(data=[(j, 201, 5.0)],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 203:  # tocos igual a qualquer valor
                    aux = pd.DataFrame(data=[(j, 203, 5.0)],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 117:  # igual pedras 116 ou qualquer valor
                    aux = pd.DataFrame(data=[(j, 117, 5.0)],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 301:
                    aux = pd.DataFrame(data=[(j, 301, 5.0)],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 266:  # igual 66
                    aux = pd.DataFrame(data=[(j, 266, self.dados.loc[j, 66][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 76:  # igual 75
                    aux = pd.DataFrame(data=[(j, 76, self.dados.loc[j, 75][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 288:  # igual 302
                    aux = pd.DataFrame(data=[(j, 288, self.dados.loc[j, 302][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])
                    pass

                if i == 34:  # 44 - 42
                    aux = pd.DataFrame(data=[(j, 34, self.dados.loc[j, 44][str(mes)].values[0] - \
                                              self.dados.loc[j, 42][str(mes)].values[0])],
                                       columns=['CENA', 'POSTO', str(mes)])
                    df_posto = pd.concat([df_posto, aux])

        df_posto.set_index(['CENA', 'POSTO'], inplace=True)
        self.dados = pd.concat([self.dados, df_posto])
        self.dados.sort_index(axis=0, level=[1], ascending=True, inplace=True)
        return self


class Desenho:
    def __init__(self, paths, nomes, dados, config_plot, mlt):
        self.paths = paths
        self.nomes = nomes
        self.dados = dados
        self.referencia = config_plot['sub_referencia']
        self.par_sub = config_plot['par_subs']
        aux = []
        for i in range(config_plot['n_classes']):
            aux.append([config_plot['valor_inicial'] + i * config_plot['step'],
                        config_plot['valor_inicial'] +  (i + 1) * config_plot['step']
                        ]
                       )
        self.config_plot = pd.DataFrame(data=aux, columns=['inferior', 'superior'])
        self.mlt = mlt
        return


    def desenha_scatter(self, mes):
        subsistemas = ['SE', 'S', 'NE', 'N']
        fig = plt.figure(figsize=(13, 7))
        ax = fig.add_subplot(111)

        colors = cm.hsv(np.linspace(0, 1, self.config_plot.shape[0]))
        self.config_plot['texto'] = self.config_plot.apply(lambda x: '{} >= pld < {}'.format(x['inferior'],
                                                                                             x['superior']
                                                                                             ), axis=1
                                                           )

        for i in self.config_plot.iterrows():
            aux = pd.DataFrame(self.dados.loc[(self.dados['preco'] >= i[1].inferior) &
                                (self.dados['preco'] < i[1].superior) &
                                (self.dados['submercado'] == self.referencia)
                               ]
                               )

            aux = self.dados.loc[self.dados['cenario'].isin(aux['cenario'].values)]

            x = aux.loc[aux['submercado'] == self.par_sub[0], 'ena'].values / \
                mlt.loc[mlt['mes'] == mes, str(self.par_sub[0])].values[0]

            y = aux.loc[aux['submercado'] == self.par_sub[1], 'ena'].values / \
                mlt.loc[mlt['mes'] == mes, str(self.par_sub[1])].values[0]

            ax.scatter(x=x,
                       y=y,
                       c=colors[i[0]]
                       )

        #  Legenda
        cenarios = self.dados.shape[0] / 4
        plt.legend(self.config_plot.texto, loc=2, title='Agrupamento de {} cenarios'.format(cenarios),
                   fancybox=True
                   )
        ax.get_legend().get_title().set_color("red")

        #  ajustando eixos
        plt.xlabel(s='{} [%MLT]'.format(subsistemas[self.par_sub[0] - 1]))
        plt.ylabel(s='{} [%MLT]'.format(subsistemas[self.par_sub[1] - 1]))
        plt.tick_params(axis='both', which='major', labelsize=7)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
        ticks_x = ax.get_xticks()
        ticks_y = ax.get_yticks()
        ax.set_xticklabels(['{:3.0f}%'.format(x * 100) for x in ticks_x])
        ax.set_yticklabels(['{:3.0f}%'.format(x * 100) for x in ticks_y])

        # Insere grade
        ax.grid(True, linestyle='--', alpha=0.85)
        plt.title('Matriz de Precos {} - Gevazp'.format(subsistemas[self.referencia - 1]))
        plt.savefig(os.path.join(self.paths['export'], 'resultados.png'))

        return


def executa_gevazp(parametros):
    import os
    import shutil
    import subprocess
    from datetime import datetime

    t = datetime.now()
    caso = parametros[0]
    path = parametros[1]

    # Cria pasta gevazp
    os.makedirs(os.path.join(path, 'gevazp'))

    # Copia arquivos para pasta
    for i in parametros[0].nomes['decomp_exec']:
        shutil.copy(src=os.path.join(caso.paths['decomp_base'], i),
                    dst=os.path.join(path, 'gevazp'))

    for i in parametros[0].nomes['gevazp_exec']:
        shutil.copy(src=os.path.join(caso.paths['arquivos_gevazp'], i),
                    dst=os.path.join(path, 'gevazp'))

    shutil.copy(src=os.path.join(path, 'prevs.rv0'), dst=os.path.join(path, 'gevazp'))
    shutil.copy(src=os.path.join(caso.paths['arquivos_gevazp'], caso.nomes['gevazp_lic']),
                dst=os.path.join(path, 'gevazp'))

    # Executa gevazp
    os.chdir(os.path.join(path, 'gevazp'))
    FNULL = open(os.devnull, 'w')
    stdout = open(os.path.join(path, 'stdout.txt'), 'w')
    stderr = open(os.path.join(path, 'stderr.txt'), 'w')
    retcode = subprocess.call([caso.paths['executavel_gevazp']], stdout=stdout, stderr=stderr)

    #  Copia arquivo para pasta anterior
    if os.path.isfile(os.path.join(path, 'gevazp', 'vazoes.rv0')) == False:
        raw_input("Executavel nao encontrado")

    shutil.copy(os.path.join(path, 'gevazp', 'vazoes.rv0'), path)

    # Limpa pasta
    os.chdir(path)
    shutil.rmtree(os.path.join(path, 'gevazp'))

    print('Concluido -> {} Tempo de execucao GEVAZP :{:06.2f}s'.format(path, (datetime.now() - t).total_seconds()))
    return


if __name__ == '__main__':
    import os
    import glob
    import pandas as pd
    import numpy as np
    import shutil
    from multiprocessing import cpu_count, Pool
    import subprocess
    import matplotlib.ticker as ticker
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    # Configuracao -----------------------------------------------------------------------------------------------------
    paths = {'decomp_base': r'C:\Users\anderson.visconti\Desktop\gevazp\decomp-base',
             'decks_gevazp': r'C:\Users\anderson.visconti\Desktop\gevazp\decks_2',
             'vazoes_gevazp': r'C:\Users\anderson.visconti\Desktop\gevazp',
             'executavel_gevazp': r'C:\Gevazp',
             'arquivos_gevazp': r'C:\Gevazp',
             'export': r'C:\Users\anderson.visconti\Desktop\gevazp',
             'mlt': r'C:\Users\anderson.visconti\Desktop\gevazp'
             }

    nomes = {'gevazp_exec': ['arquivos.dat', 'caso.dat', 'gevazp.dat', 'MODIF.DAT',
                             'postos.dat', 'regras.dat', 'rv0.txt'
                             ],
             'gevazp_lic': 'gevazp.lic',
             'vazoes': 'VAZOESTA.CSV',
             'decomp_exec': ['dadger.rv0', 'hidr.dat', 'loss.dat', 'mlt.dat',
                             'vazoes.dat'
                             ],
             'mlt':r'mlt.csv'
             }

    config_servidor = {'n_proc': 40,
                       'versao_decomp': 25,
                       'path_exec': r'/usr/bin',
                       'path_lic': r'C:\Users\anderson.visconti\Desktop\gevazp\decomp-base',
                       'lic_decomp': r'deco.prm'
                       }

    config_plot = {'valor_inicial': 100,
                   'n_classes': 10,
                   'step': 50,
                   'sub_referencia': 1,
                   'par_subs': [1, 2]
                   }
    mes = 8

    #  Determina se executap reparacao do ambiente gevazp ou apenas decomp - 1 para sim e 0 para nao

    execucao = {'ambiente': 0,
                'gevazp': 0,
                'decomp': 0,
                'resultados': 0,
                'desenho': 1
                }
    # Fim Configuracao -------------------------------------------------------------------------------------------------

    if execucao['ambiente'] == 1:
        caso = Casos(paths=paths, nomes=nomes)
        caso.ler_vazoes(sep=',', decimal='.', mes=mes)
        caso.gerar_ambiente()
        caso.calcula_postos(mes=mes)
        caso.gerar_prevs()
        lista = glob.glob(os.path.join(caso.paths['decks_gevazp'], '*'))
        parametros = []
        for i in lista:
            parametros.append([caso, i])

    if execucao['gevazp'] == 1:
        #p = Pool(1)
        p = Pool(cpu_count())
        result = p.map(func=executa_gevazp, iterable=parametros)
        print('Fim da execucao dso Gevazps')

    # Execucao dos casos gevazp
    if execucao['decomp'] == 1:
        gerenciador = Gerenciador(paths=paths, nomes=nomes, config_servidor=config_servidor)
        gerenciador.listar_casos()
        gerenciador.executar_decomp()

    #  Captura dos resultados
    if execucao['resultados'] == 1:
        gerenciador = Gerenciador(paths=paths, nomes=nomes, config_servidor=config_servidor)
        gerenciador.listar_casos()
        for i in gerenciador.lista.iterrows():
            gerenciador.pegar_resultado(cenario=i[1].cenario)
            gerenciador.exportar_resultados()

    #  Monta grafico
    if execucao['desenho'] == 1:
        resultados = pd.read_csv(os.path.join(paths['export'], 'resultados.csv'), sep=';', decimal=',')
        mlt = pd.read_csv(os.path.join(paths['mlt'], nomes['mlt']), sep=';', decimal=',')
        desenho = Desenho(paths=paths, nomes=nomes ,dados=resultados, config_plot=config_plot, mlt=mlt)
        desenho.desenha_scatter(mes=mes)

    print('Fim')
    pass
