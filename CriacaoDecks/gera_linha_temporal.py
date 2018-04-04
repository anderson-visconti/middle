import openpyxl

import os

configs = {
    'paths_excel': [
        r'C:\Users\anderson.visconti\Desktop\teste\1\LP_1.xlsm',
        r'C:\Users\anderson.visconti\Desktop\teste\2\LP_2.xlsm',
        r'C:\Users\anderson.visconti\Desktop\teste\3\LP_3.xlsm',

    ],
    'sheet_name': r'Resultado Final',
    'vazpast': r'VazPast'
}

# Escrita dos prevs
for i, arquivo in enumerate(configs['paths_excel']):

    work_book = openpyxl.load_workbook(filename=arquivo, data_only=True)
    sheet = work_book[configs['sheet_name']]
    sheet_vazpast = work_book[configs['vazpast']]

    for rows in sheet.iter_cols(min_row=4, min_col=3, max_row=163, max_col=14): # Itera sobre o range completo
        prevs = open(
            os.path.join(
                os.path.dirname(arquivo),
                'prevs_{}_{}.rv0'.format(
                    os.path.basename(os.path.splitext(arquivo)[0]),
                    sheet.cell(row=2, column=rows[0].col_idx).internal_value,
                )
            ),
            'w'
        )

        for row, posto in enumerate(rows):
            prevs.write(
                '{:6d}''{:5d}''{:10d}''{:10d}''{:10d}''{:10d}''{:10d}''{:10d}\n'.format(
                    row + 1,
                    sheet.cell(row=posto.row, column=2).value,
                    posto.internal_value,
                    posto.internal_value,
                    posto.internal_value,
                    posto.internal_value,
                    posto.internal_value,
                    posto.internal_value
                )
            )
        prevs.close()
        print('Criado prevs {} de {}'.format(prevs.name, arquivo))

    # Escrita do Vazpast
    vazpast = open(
        os.path.join(
            os.path.dirname(arquivo),
            'vazpast_{}.dat'.format(
                os.path.basename(os.path.splitext(arquivo)[0]),
            )
        ),
        'w'
    )

    # Escrita do Export
    export = open(
        os.path.join(
            os.path.dirname(arquivo),
            'export_{}.txt'.format(
                os.path.basename(os.path.splitext(arquivo)[0]),
            )
        ),
        'w'
    )


    for cols in sheet_vazpast.iter_rows(min_row=6, min_col=5, max_row=221, max_col=18):  # Itera sobre o range completo
        valores = [i.value for i in cols]
        for i in range(2, 13):
            valores[i] = float(valores[i])

        vazpast.write(
            '{:>5d} ''{:11} ''{:>10.2f}''{:>10.2f}''{:>10.2f}''{:>10.2f}''{:>10.2f}''{:>10.2f}''{:>10.2f}'
            '{:>10.2f}''{:>10.2f}''{:>10.2f}''{:>10.2f}''{:>10.2f}\n'.format(*valores)
        )

        export.write(
            '{:>5d};''{:<15};''{:>10.2f};''{:>10.2f};''{:>10.2f};''{:>10.2f};''{:>10.2f};''{:>10.2f};''{:>10.2f};'
            '{:>10.2f};''{:>10.2f};''{:>10.2f};''{:>10.2f};''{:>10.2f};\n'.format(*valores)
        )

    print('Arquivos vazpast e export do cenario {} criado'.format(os.path.basename(arquivo)))
    work_book.close()
pass