def worker(vetor):
    import os
    from shutil import copyfile, rmtree
    """worker function"""

    # Cria pasta gevazp
    if os.path.exists(vetor[1]) == False:
        os.makedirs(vetor[1])

    else:
        rmtree(vetor[1], ignore_errors=True)
        os.makedirs(vetor[1])

    # Copia arquivos decomp para pasta gevazp
    for i in vetor[3]:

        copyfile(r'{caminho}\{arquivo}'.format(caminho=vetor[0], arquivo=i),
                 r'{caminho}\{arquivo}'.format(caminho=vetor[1], arquivo=i)
                 )

    # Copia arquivos gevazp para pasta gevazp
    for i in vetor[5]:
        copyfile(r'{caminho}\{arquivo}'.format(caminho=vetor[2], arquivo=i),
                 r'{caminho}\{arquivo}'.format(caminho=vetor[1], arquivo=i)
                 )

    # Executa gevazp
    os.chdir(vetor[1])
    os.system('{caminho}\{executavel}'.format(caminho=vetor[6], executavel=vetor[7]))

    # Copia arquivo vazoes
    copyfile(r'{caminho}\{arquivo}'.format(caminho=vetor[1], arquivo=vetor[4][0]),
             r'{caminho}\{arquivo}'.format(caminho=vetor[0], arquivo=vetor[4][0])
             )

    rmtree(vetor[1], ignore_errors=True)

    print 'Caso: {} executado'.format(vetor[0])
    return

if __name__ == '__main__':
    from multiprocessing import cpu_count, Pool
    from shutil import copyfile, rmtree
    import os
    path_exec = r'C:\Gevazp'  # Caminho para executavel gevazp
    path_gevazp = r'C:\Gevazp'  # Caminho para arruivos gevavazp e licenca
    nome_executavel = 'gevazp.exe'  # Nome do executavel do gevazp

    lista_arquivos = [r'dadger.rv0', r'prevs.rv0', r'vazoes.dat', r'hidr.dat', r'loss.dat', r'mlt.dat',
                      r'postos.dat']    # Lista com arquivos do decomop

    lista_gevazp = [r'arquivos.dat', r'caso.dat', r'gevazp.dat', r'modif.dat',
                    r'regras.dat', r'rv0.txt', r'gevazp.lic']   # Lista com arquivos do gevazp

    arquivos_saida = ['vazoes.rv0'] # Arquivos de saida a serem copiados para pasta do caso

    lista = [r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2017\01\c4-otimista-SE-pessimista-NE-N-medio',
             r'C:\OneDrive\Middle Office\Middle\Decks\Prospectivos\2017\01\c5-otimista-SE-pessimista-NE-N-medio-S-otimista'
             ]  # Lista com caminhos dos casos

    range_datas = ['201702', '201703', '201704', '201705', '201706']    # Lista com nomes dos estagios

    caminhos = []
    # Cria vetor com parametros para paralelizacao
    for i in lista: # Itera sobre casos
        for j in range_datas: # Itera sobre estagios
            caminhos.append([r'{caso}\{estagio}\decomp'.format(caso=i, estagio=j),
                             r'{caso}\{estagio}\decomp\gevazp'.format(caso=i, estagio=j),
                             path_exec,
                             lista_arquivos,
                             arquivos_saida,
                             lista_gevazp,
                             path_gevazp,
                             nome_executavel]
                            )

    # Paralelismo
    p = Pool(processes=cpu_count())
    result = p.map(func=worker, iterable=caminhos)
    p.close()
