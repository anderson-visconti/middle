from multiprocessing import cpu_count
from multiprocessing import Pool
from functools import partial


def worker(path):
    import os
    """worker function"""
    os.chdir(path[0])
    os.system(path[1])
    print 'Caso: {} executado'.format(path[0])
    return

if __name__ == '__main__':

    lista = [r'C:\Users\anderson.visconti\Desktop\c1\201702\decomp\gevazp',
             r'C:\Users\anderson.visconti\Desktop\c1\201703\decomp\gevazp',
             r'C:\Users\anderson.visconti\Desktop\c1\201704\decomp\gevazp',
             r'C:\Users\anderson.visconti\Desktop\c1\201705\decomp\gevazp'
             ]
    path_exec = r'C:\Gevazp\Gevazp.exe'
    caminhos = []
    for i in lista:
        print i
        caminhos.append([i, path_exec])

    p = Pool(processes=cpu_count())
    result = p.map(func=worker, iterable=caminhos)
    p.close()
    print 'Execucao gevazp concluida'
