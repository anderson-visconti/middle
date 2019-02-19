#!/usr/bin/env python


def worker(path):
    import os
    print('Executanto -> {}'.format(path))
    os.system('cdo -f nc import_binary {} {}.nc'.format(path, path[:-4]))
    return


if __name__ == '__main__':
    import os
    import glob
    from multiprocessing import cpu_count, Pool

    # Caminho onde estao os arquivos
    path = r'/home/centos/merge/merge_bin'

    lista = glob.glob(os.path.join(path, '*.ctl'))
    print('Execucao conversao em {} processos'.format(cpu_count()))
    p = Pool(processes=cpu_count())
    result = p.map(func=worker, iterable=lista)
    os.chdir(path)
    os.system('zip ./chuva.zip *.nc')
