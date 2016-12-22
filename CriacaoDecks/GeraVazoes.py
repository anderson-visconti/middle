def execucao(path_gevazp, path_decomp, path_licenca):
    import os
    os.system('cd {0}'.format(path_gevazp))
    os.system('@ECHO | echo rv0 | call {}/datvaz'.format(path_licenca))
    os.system('call {}/gevazp'.format(path_licenca))
    os.system('call {}/prevcen'.format(path_licenca))
    shutil.copy(src=os.path.join(path_gevazp, 'vazoes.rv0'), dst=full_path_decomp)
    return

__author__= 'Anderson Visconti'
'''
Script para gerar arquivos vazoes da rotina gevazp
Necessário que os executeveis do datavaz, gevazp e prevcen estejam na variavel PATH do windows
Script fara um loop em todas as pastas indicadas no vetor cenarios, supondo que dentro de cada cenario havera umas pasta
com o estagio e dentro dela uma pasta decomp contendo todos os arquivos necessarios para geracao do arquivo vazoes.rvx
'''
import os
import shutil
#from joblib import Parallel, delayed
import multiprocessing

arquivos = ['dadger.rv0', 'hidr.dat', 'MLT.dat', 'MODIF.dat', 'POSTOS.dat', 'prevs.rv0',
            'Vazoesc.dat', 'LOSS.dat','rv0']
num_cores = multiprocessing.cpu_count()
#Variaveso -------------------------------------------------------------------------------------------------------------
path_licenca = r'C:\Gevazp'                                     # Caminho para os executáveis e licenca do gevazp
path = r'D:\Middle Office\Middle\Decks\Prospectivos\2016\9'     # Caminho base para os casos
cenarios = ['c2-medio'
            ]   # Nomes das pastas dos cenarios
#-----------------------------------------------------------------------------------------------------------------------
for i in range(0, len(cenarios)):
    full_path_cenarios = os.path.join(path, cenarios[i])
    estagios = os.listdir(full_path_cenarios)

    for j in range(0, len(estagios)):
        full_path_estagio = os.path.join(full_path_cenarios, estagios[j])

        # Verifica se ha pasta decomp no estagio
        if os.path.exists(os.path.join(full_path_estagio, 'decomp')) == True:
            full_path_decomp = os.path.join(os.path.join(full_path_estagio, 'decomp'))

            try:    # Cria pasta gevazp
                os.makedirs(os.path.join(full_path_decomp, 'gevazp'))
            except:

                pass
            # Copia arqvuivos necessarios para pasta gevazp
            shutil.copy(os.path.join(path_licenca, 'Gevazp.prm'), os.path.join(full_path_decomp, 'gevazp'))
            for k in range(0, len(arquivos)):
                shutil.copy(src=os.path.join(full_path_decomp, arquivos[k]), dst=os.path.join(full_path_decomp, 'gevazp'))

            path_gevazp = os.path.join(full_path_decomp, 'gevazp')
            os.chdir(path_gevazp)
            execucao(path_gevazp, full_path_decomp, path_licenca)
            #Parallel(n_jobs=num_cores)(delayed(estagios)(i) for i in estagios)

print('FIM')
