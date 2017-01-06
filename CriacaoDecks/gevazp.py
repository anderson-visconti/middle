from multiprocessing import cpu_count
from multiprocessing import Pool
from functools import partial
import os
def worker(vetor):
    import os
    from shutil import copyfile, rmtree
    """worker function"""
    # Cria pasta gevazp
    try:
        os.makedirs(vetor[1])
    except:
        rmtree(vetor[1], ignore_errors=True)
        os.rmdir(vetor[1])

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
    os.system(vetor[2] + r'\gevazp.exe')

    # Copia arquivo vazoes
    copyfile(r'{caminho}\{arquivo}'.format(caminho=vetor[1], arquivo=vetor[4][0]),
             r'{caminho}\{arquivo}'.format(caminho=vetor[0], arquivo=vetor[4][0])
             )

    rmtree(vetor[1], ignore_errors=True)
    os.rmdir(vetor[1])
    print 'Caso: {} executado'.format(vetor[0])
    return

if __name__ == '__main__':
    path_exec = r'C:\Gevazp'  # Caminho para executavel, arquivos base e licenca

    lista_arquivos = [r'dadger.rv0', r'prevs.rv0', r'vazoes.dat', r'hidr.dat', r'loss.dat', r'mlt.dat',
                      r'postos.dat']

    lista_gevazp = [r'arquivos.dat', r'caso.dat', r'gevazp.dat', r'modif.dat', r'regras.dat', r'rv0.txt', r'gevazp.lic']

    arquivos_saida = ['vazoes.rv0']

    lista = [r'C:\Users\anderson.visconti\Desktop\casos\c1'
             ]

    range_datas = ['201702']
    caminhos = []
    # Cria vetor com parametros para paralelizacao
    for i in lista: # Itera sobre casos
        for j in range_datas: # Itera sobre estagios
            caminhos.append([r'{caso}\{estagio}\decomp'.format(caso=i, estagio=j),
                             r'{caso}\{estagio}\decomp\gevazp'.format(caso=i, estagio=j),
                             path_exec,
                             lista_arquivos,
                             arquivos_saida,
                             lista_gevazp]
                            )

    for i in caminhos[0]:
        print i

    p = Pool(processes=cpu_count())
    result = p.map(func=worker, iterable=caminhos)
    p.close()
    print 'Execucao gevazp concluida'
