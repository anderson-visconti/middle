#!/usr/bin/env python
# *- coding: utf-8 -*-
global private_key
private_key = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQC7njVlhaVw3Es+ujIWFzmCuN4vcu+MycIZkGlIldqXpk/SXwK4
sSi2n6vYBWvfXLrnp3m2JGFI4LyE3c84tkhayEntdfFX0HcCjVZ9ROf9R8EtMDwP
B8AfbKTqmejP4qhinGGoC4UnnCZY5wGIzmAoHE4gIEXwSNZ2sKuhXp4gnQIDAQAB
AoGASkWfLclybPNIdlSPb19STQWSL4Z4fmuAg04/35QzLMWR493o3eSEEYe0J5g9
0/aJpxsNe6V7PbZ56r9EQVcn3NrUgcTxFQJiWBLsfn1fneNRwI8VlF7uCb+xLIum
5amuTq7tXbloi0y/JsuU2T1JOWaKrvKK5vjo6PCxEFhgjwECQQDYNXiNCipVPWVV
gu5IxwZoyqwbEPE3dj5MvmC7j66ccyPSh4WeE+zMzhHV46FSdlaGv0Z2sCZHUgoV
N1u0qHR1AkEA3iWy8RWnVFB7dYMGy9YtOyrhsjJseLif3T85dfTdORCdJe8qVWIG
5QdoqwMs2b9w9wH37G2sSYLTw9nvhubWiQJAZPvEjIuc7ic491GqHg/nbHaNIC8v
myn9OzcIU1Juyd/1cVWfERBZX+c36WDibnObQmCAdtsbZeBpmTM8AAtWKQJBAIxe
X+KMXy4cqNZJE8tLK0t+vhw+VmI1rvY7VBCfyAWd5N6qcCKBjX+8nbuphvaUTEoY
GVNwvXO50huoIv0n8ZkCQQDOmPKAasRavV9iuj3ekQhH6iwHbMa46sYF5aoAGQ/m
hCL6y79BelOBAnBHt/oUvp4dqjwr8J2wGGi1DBvUWlGu
-----END RSA PRIVATE KEY-----'''

class Criptografia:
    def __init__(self, paths, nomes):
        self.paths = paths
        self.nomes = nomes
        return

    def gerar_chave_publica(self):
        self.public_key = RSA.importKey(private_key).publickey().exportKey()
        pub_key_file = open(os.path.join(self.paths['export'], self.nomes['public_key']), 'w')
        try:
            pub_key_file.write(str(self.public_key))
            print('\nchave publica {} exportada para {}\n'.format(self.nomes['public_key'],
                                                                self.paths['export']
                                                              )
                  )
            pub_key_file.close()
        except:
            print('\nNao foi possivel exportar a chave publica {} para {}\n'.format(self.nomes['public_key'],
                                                                                  self.paths['export']
                                                                                )
                  )
        return self


    def gerar_senha(self):
        pub_key = open(os.path.join(self.paths['export'], self.nomes['public_key']), 'r').read()
        senha = getpass.getpass(prompt='\nDigite a senha do email a ser criptograda: ')
        senha2 = getpass.getpass(prompt='\nConfirme a senha: ')

        if senha == senha2:
            priv_key = RSA.importKey(private_key)
            encrypt_senha =  priv_key.encrypt(senha, 42)
            senha_file = open(os.path.join(self.paths['export'], self.nomes['senha_email']), 'w')
            senha_file.write(str(encrypt_senha))
            senha_file.close()


        else:
            print('Voce digitou senhas diferentes. Execute novamente.')
        return


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


    def envia_email(self, config_email):
        priv_key = RSA.importKey(private_key)
        senha = open(os.path.join(self.paths['export'], self.nomes['senha_email']), 'r').read()
        decrypt_msg = priv_key.decrypt(ast.literal_eval(str(senha)))

        server = smtplib.SMTP(config_email['servidor'], config_email['porta'])
        server.starttls()
        server.login(config_email['user'], decrypt_msg)

        msg = MIMEMultipart()
        msg['Subject'] = 'Resultados GEVAZP'
        msg['From'] = config_email['from']
        msg['To'] = ', '.join(config_email['to'])
        body = \
        '''Resultados GEVAZP
        Caminho: {}
        
*obs: E-mail automatico. Em caso de bugs, entre em contato com administrador'''

        msg.attach(MIMEText(body.format(self.paths['decks_gevazp']), 'plain'))

        # anexo
        csv = MIMEText(file(os.path.join(self.paths['export'], 'resultados.csv')).read())
        csv.add_header('Content-Disposition', 'attachment', filename='resultados.csv')
        msg.attach(csv)
        server.sendmail(config_email['from'], config_email['to'], msg.as_string())
        server.quit()
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
        self.dados = pd.DataFrame(dados)
        self.referencia = config_plot['sub_referencia']
        self.par_sub = config_plot['par_subs']
        self.retangulo = config_plot['retangulo']
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
        self.dados = pd.DataFrame(self.dados)
        colors = cm.jet(np.linspace(0, 0.9, self.config_plot.shape[0]))
        self.dados['ena'] = self.dados['ena'].apply(lambda x: float(x))
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

            #ax.scatter(x=x,
            #           y=y,
            #           c=colors[i[0]]
            #           )
            ax.scatter(x=x,
                       y=y,
                       c=colors[i[0]],
                       alpha=1.0
                   )
        #  Legenda
        cenarios = self.dados.shape[0] / 4 + 1
        plt.legend(self.config_plot.texto, loc=2, title='Agrupamento de {} cenarios'.format(cenarios),
                   fancybox=True
                   )
        ax.get_legend().get_title().set_color("red")

        #  ajustando eixos
        plt.xlabel(s='{} [%MLT]'.format(subsistemas[self.par_sub[0] - 1]))
        plt.ylabel(s='{} [%MLT]'.format(subsistemas[self.par_sub[1] - 1]))
        plt.tick_params(axis='both', which='major', labelsize=7)

        #tick_x = ticker.ScalarFormatter(0.2)
        #ax.xaxis.set_major_locator(ticker.ScalarFormatter(0.2))
        #ax.yaxis.set_major_locator(ticker.ScalarFormatter(0.2))

        lim_x = [round(min(self.dados.loc[self.dados['submercado'] == self.referencia, 'ena']) / \
                 mlt.loc[mlt['mes'] == mes, str(self.par_sub[0])].values[0], 1),

                 math.ceil(max(self.dados.loc[self.dados['submercado'] == self.referencia, 'ena']) / \
                           mlt.loc[mlt['mes'] == mes, str(self.par_sub[0])].values[0])
                ]

        lim_y = [round(min(self.dados.loc[self.dados['submercado'] == self.par_sub[1], 'ena']) / \
                            mlt.loc[mlt['mes'] == mes, str(self.par_sub[1])].values[0], 1),

                 math.ceil(max(self.dados.loc[self.dados['submercado'] == self.par_sub[1], 'ena']) / \
                           mlt.loc[mlt['mes'] == mes, str(self.par_sub[1])].values[0])
                 ]

        #plt.xticks(np.arange(0, lim_x[1], round(lim_y[1] * 100) / 5000), rotation=30)
        #plt.yticks(np.arange(0, lim_y[1], round(lim_x[1] * 100) / 1000))
        ticks_x = ax.get_xticks()
        ticks_y = ax.get_yticks()
        ax.set_xticklabels(['{:3.0f}%'.format(x * 100) for x in ticks_x])
        ax.set_yticklabels(['{:3.0f}%'.format(x * 100) for x in ticks_y])

        # Insere grade
        ax.grid(True, linestyle='--', alpha=0.85)
        plt.title('Matriz de Precos {} - Gevazp - Mes {}'.format(subsistemas[self.referencia - 1], mes))

        #  Desenha retangulo
        ax.add_patch(patches.Rectangle(xy=self.retangulo['lower_left'],
                                       width=self.retangulo['width'],
                                       height=self.retangulo['height'],
                                       fill=False,
                                       edgecolor='r',
                                       linestyle='dashed',
                                       linewidth=3.0
                                       )
                     )
        ax.annotate('Intervalo confianca',
                    xy=(self.retangulo['lower_left'][0] + self.retangulo['width'],
                        self.retangulo['lower_left'][1] + self.retangulo['height']
                        ),
                    color='r',
                    weight='bold',
                    arrowprops=dict(facecolor='r', edgecolor='r'),
                    xytext=(self.retangulo['lower_left'][0] + self.retangulo['width'] + 0.1,
                            self.retangulo['lower_left'][1] + self.retangulo['height'] + 0.5
                            ),
                    fontsize=14,
                    alpha=0.80
                    )

        # Salva figura
        plt.savefig(os.path.join(self.paths['export'], 'resultados.png'), bbox_inches='tight')
        return


    def desenha_scatter_ena_bruta(self, mes):
        subsistemas = ['SE', 'S', 'NE', 'N']
        fig = plt.figure(figsize=(13, 7))
        ax = fig.add_subplot(111)
        self.dados = pd.DataFrame(self.dados)

        self.dados['ena'] = self.dados['ena'].apply(lambda x: float(x))
        colors = cm.jet(np.linspace(0, 0.90, self.config_plot.shape[0]))
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

            x = aux.loc[aux['submercado'] == self.par_sub[0], 'ena'].values
            y = aux.loc[aux['submercado'] == self.par_sub[1], 'ena'].values
            ax.scatter(x=x,
                       y=y,
                       c=colors[i[0]]
                       )

        # Legenda
        cenarios = self.dados.shape[0] / 4 + 1
        plt.legend(self.config_plot.texto, loc=2, title='Agrupamento de {} cenarios'.format(cenarios),
                   fancybox=True
                   )
        ax.get_legend().get_title().set_color("red")

        #  ajustando eixos
        plt.xlabel(s='{} [MWm]'.format(subsistemas[self.par_sub[0] - 1]))
        plt.ylabel(s='{} [MWm]'.format(subsistemas[self.par_sub[1] - 1]))
        plt.tick_params(axis='both', which='major', labelsize=9)


        lim_x = [round(min(self.dados.loc[self.dados['submercado'] == self.referencia, 'ena'])),

                 math.ceil(max(self.dados.loc[self.dados['submercado'] == self.referencia, 'ena']))
                 ]

        lim_y = [round(min(self.dados.loc[self.dados['submercado'] == self.par_sub[1], 'ena'])),

                 math.ceil(max(self.dados.loc[self.dados['submercado'] == self.par_sub[1], 'ena']))
                 ]

        ticks_x = ax.get_xticks()
        ticks_y = ax.get_yticks()
        ax.set_xticklabels(['{:6.0f}'.format(x) for x in ticks_x])
        ax.set_yticklabels(['{:6.0f}'.format(x) for x in ticks_y])

        # Insere grade
        ax.grid(True, linestyle='--', alpha=0.85)
        plt.title('Matriz de Precos {} - Gevazp - Mes {}'.format(subsistemas[self.referencia - 1], mes))

        ax.annotate('Intervalo confianca',
                    xy=(self.retangulo['lower_left'][0] + self.retangulo['width'],
                        self.retangulo['lower_left'][1] + self.retangulo['height']
                        ),
                    color='r',
                    weight='bold',
                    arrowprops=dict(facecolor='r', edgecolor='r'),
                    xytext=(self.retangulo['lower_left'][0] + self.retangulo['width'] + 0.2,
                            self.retangulo['lower_left'][1] + self.retangulo['height'] + 0.2
                            ),
                    fontsize=14
                    )
        # Salva figura
        plt.savefig(os.path.join(self.paths['export'], 'resultados_bruto.png'), bbox_inches='tight')
        pass
        return


    def desenha_scatter_seaborn(self, mes):
        subsistemas = ['SE', 'S', 'NE', 'N']
        self.dados = pd.DataFrame(self.dados)
        self.dados['ena'] = self.dados['ena'].apply(lambda x: float(x))
        self.config_plot['texto'] = self.config_plot.apply(lambda x: '{} >= pld < {}'.format(x['inferior'],
                                                                                             x['superior']
                                                                                             ), axis=1
                                                           )
        self.dados['group'] = -1
        # itera classificando nos ranges definidos
        for i in self.config_plot.iterrows():
            aux = self.dados.loc[(self.dados['preco'] >= i[1].inferior) &
                                              (self.dados['preco'] < i[1].superior) &
                                              (self.dados['submercado'] == self.referencia), :
                                ]['cenario']

            self.dados.loc[self.dados['cenario'].isin(aux), ['group']] = i[1].texto

        # remove cenarios nao classificados e subsistemas que nao se deseja plotar
        self.dados = self.dados.loc[self.dados['submercado'].isin(self.par_sub), :]
        self.dados = pd.DataFrame(self.dados.loc[self.dados['group'] != -1, :])

        # cria coluna com ena percentual
        self.dados['ena_p'] = 0

        # calcula ena percentual subsistema de referencia
        aux = self.dados.loc[self.dados.submercado == self.referencia].index
        self.dados.loc[aux, 'ena_p'] = self.dados.loc[aux, 'ena'] / self.mlt.loc[mes - 1, str(self.referencia)] * 100
        # calcula ena percentual subsistema de comparacao
        aux = self.dados.loc[self.dados.submercado == self.par_sub[1]].index
        self.dados.loc[aux, 'ena_p'] = self.dados.loc[aux, 'ena'] / self.mlt.loc[mes - 1, str(self.par_sub[1])] * 100

        # pega enas para formacao das enas
        aux = self.dados.loc[self.dados['submercado'] == self.referencia, ['cenario', 'ena', 'ena_p']]
        aux2 = self.dados.loc[self.dados['submercado'] == self.par_sub[1], ['cenario', 'ena', 'ena_p']]

        aux = aux.rename(columns={'ena': 'ena_bruta_{}'.format(subsistemas[self.referencia - 1]),
                            'ena_p':'ena_p_{}'.format(subsistemas[self.referencia - 1])
                            }
                   )
        aux2 = aux2.rename(columns={'ena': 'ena_bruta_{}'.format(subsistemas[self.par_sub[1] - 1]),
                             'ena_p': 'ena_p_{}'.format(subsistemas[self.par_sub[1] - 1])
                            }
                   )

        self.dados = pd.merge(self.dados, aux, on=['cenario'])
        self.dados = pd.merge(self.dados, aux2, on=['cenario'])
        self.dados.sort_values(by=['preco'], ascending=True, inplace=True)
        sns.set_style('ticks', {'axes.grid': True,
                                'legend.frameon': True,
                                'grid.linestyle': u'--',
                                'legend.scatterpoints': 1
                               }
                      )

        markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'] * 10
        sns.set_context('notebook')
        sns.axes_style()
        
        # Grafico ENA bruta
        sns.lmplot(x='ena_bruta_{}'.format(subsistemas[self.referencia - 1]),
                   y='ena_bruta_{}'.format(subsistemas[self.par_sub[1] - 1]),
                   data=self.dados,
                   hue='group',
                   fit_reg=False,
                   palette='hsv',
                   legend=False,
                   legend_out=False,
                   size=6.3,
                   aspect=2.0,
                   scatter=True,
                   markers=markers[0:len(self.dados['group'].unique())]
                   )

        plt.xlabel(s='ENA - {} [MWm]'.format(subsistemas[self.referencia - 1]))
        plt.ylabel(s='ENA - {} [MWm]'.format(subsistemas[self.par_sub[1] - 1]))
        plt.legend(loc='best', fancybox=True, frameon=True, title='Classes PLD', facecolor='white')
        plt.minorticks_on()
        plt.grid(b=True, which='both', linestyle= u'--')
        plt.title(s='Matriz de Precos GEVAZP - Mes {} - Mercado - {}'.format(mes, subsistemas[self.referencia - 1]),
                  loc='center')
        plt.savefig(os.path.join(self.paths['export'], '{}_resultado_b_{}_{}.png'.format(mes,
                                                                                      str(subsistemas[self.referencia - 1]),
                                                                                      str(subsistemas[self.par_sub[1] - 1])
                                                                                      )
                                 )
                    )
        plt.close()

        # Grafico ENA relativa
        sns.lmplot(x='ena_p_{}'.format(subsistemas[self.referencia - 1]),
                   y='ena_p_{}'.format(subsistemas[self.par_sub[1] - 1]),
                   data=self.dados,
                   hue='group',
                   fit_reg=False,
                   palette='hsv',
                   legend=False,
                   legend_out=False,
                   size=6.3,
                   aspect=2.0,
                   scatter=True,
                   markers=markers[0:len(self.dados['group'].unique())]
                   )

        plt.xlabel(s='ENA - {} [%MLT]'.format(subsistemas[self.referencia - 1]))
        plt.ylabel(s='ENA - {} [%MLT]'.format(subsistemas[self.par_sub[1] - 1]))
        plt.legend(loc='best', fancybox=True, frameon=True, title='Classes PLD', facecolor='white')
        plt.minorticks_on()
        plt.grid(b=True, which='both', linestyle=u'--')
        plt.title(s='Matriz de Precos GEVAZP - Mes {} - Mercado - {}'.format(mes, subsistemas[self.referencia - 1]),
                  loc='center')
        plt.savefig(os.path.join(self.paths['export'], '{}_resultado_p_{}_{}.png'.format(mes,
                                                                                       str(subsistemas[
                                                                                               self.referencia - 1]),
                                                                                       str(subsistemas[
                                                                                               self.par_sub[1] - 1])
                                                                                       )
                                 )
                    )
        plt.close()
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
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.cm as cm
    import math
    import smtplib
    from email.MIMEText import MIMEText
    from email.mime.multipart import MIMEMultipart
    from Crypto.PublicKey import RSA
    import ast
    import getpass
    import seaborn as sns

    # Configuracao -----------------------------------------------------------------------------------------------------
    mes = 12
    paths = {'decomp_base': r'C:\OneDrive\Middle Office\Middle\Decks\gevazp\2017\10\12\decomp_base',
             'decks_gevazp': r'C:\OneDrive\Middle Office\Middle\Decks\gevazp\2017\10\12\decks',
             'vazoes_gevazp': r'C:\OneDrive\Middle Office\Middle\Decks\gevazp\2017\10\12\gevazp_base',
             'executavel_gevazp': r'C:\Gevazp\gevazp',
             'arquivos_gevazp': r'C:\Gevazp',
             'export': r'C:\OneDrive\Middle Office\Middle\Decks\gevazp\2017\10\12\export_1',
             'mlt': r'C:\OneDrive\Middle Office\Middle\Decks\gevazp\2017\10\12'
             }

    nomes = {'gevazp_exec': ['arquivos.dat', 'caso.dat', 'gevazp.dat', 'MODIF.DAT',
                             'postos.dat', 'regras.dat', 'rv0.txt'
                             ],
             'gevazp_lic': 'gevazp.lic',
             'vazoes': 'VAZOESTA.CSV',
             'decomp_exec': ['dadger.rv0', 'hidr.dat', 'loss.dat', 'mlt.dat',
                             'vazoes.dat'
                             ],
             'mlt':r'mlt.csv',
             'public_key': 'public_key.txt',
             'senha_email': 'config.txt'
             }

    config_servidor = {'n_proc': 40,
                       'versao_decomp': 25,
                       'path_exec': r'/usr/bin',
                       'path_lic': r'C:\Users\anderson.visconti\Desktop\gevazp\decomp-base',
                       'lic_decomp': r'deco.prm'
                       }

    config_plot = {'valor_inicial': 150,
                   'n_classes': 15,
                   'step': 40,
                   'sub_referencia': 1,
                   'par_subs': [1, 3],
                   'retangulo': {'lower_left': (0.80, 0.70),
                                 'height': 0.50,
                                 'width': 0.25}
                   }
    config_email = {'from': 'multivac.gerenciador@gmail.com',
                    'to': ['multivac.gerenciador@gmail.com',
                           'anderson.visconti@enexenergia.com.br'
                             ],
                    'servidor': 'smtp.gmail.com',
                    'porta': 587,
                    'user': 'multivac.gerenciador@gmail.com'
                    }


    #  Determina se executap preparacao do ambiente gevazp ou apenas decomp - 1 para sim e 0 para nao
    execucao = {'ambiente': 0,
                'gevazp': 0,
                'decomp': 0,
                'resultados': 0,
                'desenho': 1,
                'envia_email': 0,
                'criptografia': 0
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
        desenho.desenha_scatter_seaborn(mes=mes)

    if execucao['envia_email'] == 1:
        gerenciador = Gerenciador(paths=paths, nomes=nomes, config_servidor=config_servidor)
        gerenciador.envia_email(config_email=config_email)

    if execucao['criptografia'] == 1:
        cripto = Criptografia(paths=paths, nomes=nomes)
        cripto.gerar_chave_publica()
        cripto.gerar_senha()
        pass

    print('Fim')
    pass
