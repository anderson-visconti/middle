#!/usr/bin/env python
if __name__== '__main__':
    import urllib2
    import os
    import subprocess
    import pandas as pd
    from datetime import datetime
    import glob


    paths = {
        'ftp_cptec': r'http://ftp.cptec.inpe.br/modelos/io/produtos/MERGE/',
        'export': r'/home/middle/merge/bin'
    }

    datas = {
        'data_inicial':  '2007-01-02',
        'data_final': '2017-10-23',
    }

    df_dados = pd.DataFrame(
        data=pd.date_range(datas['data_inicial'], datas['data_final'], freq='D'),
        columns=['datas']
    )

    df_dados['bin'] = df_dados['datas'].apply(lambda x: r'{}/{}/prec_{:%Y%m%d}.bin'.format(
        paths['ftp_cptec'],
        x.year,
        x
    ))

    df_dados['ctl'] = df_dados['datas'].apply(lambda x: r'{}/{}/prec_{:%Y%m%d}.ctl'.format(
        paths['ftp_cptec'],
        x.year,
        x
    ))

    df_dados['nome'] = df_dados['datas'].apply(lambda x: 'prec_{:%Y%m%d}'.format(x))

    for i in df_dados.iterrows():
        # .bin
        data = urllib2.urlopen(i[1]['bin']).read()
        f_bin = open(r'{}/{}.bin'.format(paths['export'], i[1]['nome']), 'wb')
        f_bin.write(data)
        f_bin.close()

        # .ctl
        data = urllib2.urlopen(i[1]['ctl']).read()
        f_bin = open(r'{}/{}.ctl'.format(paths['export'], i[1]['nome']), 'wb')
        f_bin.write(data)
        f_bin.close()
        
    
    pass