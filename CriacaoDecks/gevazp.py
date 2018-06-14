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
    print('Executando -> {caminho}'.format(caminho=vetor[0]))
    os.system('{caminho}\{executavel} > NUL'.format(caminho=vetor[6], executavel=vetor[7]))

    # Copia arquivo vazoes
    copyfile(r'{caminho}\{arquivo}'.format(caminho=vetor[1], arquivo=vetor[4][0]),
             r'{caminho}\{arquivo}'.format(caminho=vetor[0], arquivo=vetor[4][0])
             )

    rmtree(vetor[1], ignore_errors=True)

    #print 'Caso: {} executado'.format(vetor[0])
    return

if __name__ == '__main__':
    from multiprocessing import cpu_count, Pool
    from shutil import copyfile, rmtree
    import os
    from datetime import datetime
    path_exec = r'C:\Gevazp'  # Caminho para executavel gevazp
    path_gevazp = r'C:\Gevazp'  # Caminho para arruivos gevavazp e licenca
    nome_executavel = 'gevazp.exe'  # Nome do executavel do gevazp

    t1 = datetime.now()
    lista_arquivos = [
        r'dadger.rv0', r'prevs.rv0', r'vazoes.dat', r'hidr.dat', r'perdas.dat', r'mlt.dat',
    ]    # Lista com arquivos do decomop

    lista_gevazp = [
        r'arquivos.dat', r'caso.dat', r'gevazp.dat', r'modif.dat',
        r'regras.dat', r'rv0.txt', r'gevazp.lic', r'postos.dat'
    ]   # Lista com arquivos do gevazp

    arquivos_saida = [
        'vazoes.rv0'
    ] # Arquivos de saida a serem copiados para pasta do caso

    lista = [
        r'C:\Onedrive\Middle Office\Middle\Decks\Prospectivos\2018\05\p2-mediano\01',
        r'C:\Onedrive\Middle Office\Middle\Decks\Prospectivos\2018\05\p2-mediano\02',
        r'C:\Onedrive\Middle Office\Middle\Decks\Prospectivos\2018\05\p2-mediano\03',
        r'C:\Onedrive\Middle Office\Middle\Decks\Prospectivos\2018\05\p2-mediano\04',
        r'C:\Onedrive\Middle Office\Middle\Decks\Prospectivos\2018\05\p2-mediano\05',
    ]  # Lista com caminhos dos casos

    range_datas = [
        '201806', '201807', '201808'
    ]    # Lista com nomes dos estagios

    caminhos = []
    # Cria vetor com parametros para paralelizacao
    for i in lista: # Itera sobre casos
        for j in range_datas: # Itera sobre estagios
            caminhos.append(
                [r'{caso}\{estagio}\decomp'.format(caso=i, estagio=j),
                r'{caso}\{estagio}\decomp\gevazp'.format(caso=i, estagio=j),
                path_exec,
                lista_arquivos,
                arquivos_saida,
                lista_gevazp,
                path_gevazp,
                nome_executavel]
            )

    # Paralelismo
    print('Execucao dos casos em {} processos iniciada'.format(cpu_count()))
    p = Pool(processes=cpu_count())
    result = p.map(func=worker, iterable=caminhos)
    p.close()
    print ('Processo Finalizado')
    print ('Tempo Total: {}s'.format((datetime.now() - t1).total_seconds()))