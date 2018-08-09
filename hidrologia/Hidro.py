import pandas as pd
class Posto(object):
    def __init__(self):
        pass

class P3(Posto):
    def calcula(self, hidro):
        '''Vaz(3) = 0.0'''
        return None

class P4(Posto):
    def calcula(self, hidro):
        print('Posto 4 = 0.0')
        return None

class P5(Posto):
    def calcula(self, hidro):
        print('Posto 4 = 0.0')
        return None

class P119(Posto):
    def calcula(self, dados):
        '''
        Posto 119 = v(301=118) * a + b
        '''
        f = {
            1: [1.217, +0.608],
            2: [1.232, +0.123],
            3: [1.311, -2.359],
            4: [1.241, -0.496],
            5: [1.167, +0.467],
            6: [1.333, -0.533],
            7: [1.247, -0.374],
            8: [1.200, +0.360],
            9: [1.292, -1.292],
           10: [1.250, -0.250],
           11: [1.294, -1.682],
           12: [1.215, +0.729],
        }

        p_119 = list()
        for index, row in pd.DataFrame(dados.loc[dados['num_posto'] == 118]).iterrows():
            p_119.append(
                dict(
                    num_posto=119,
                    dat_medicao=row['dat_medicao'],
                    val_vaz_natr=(
                            row['val_vaz_natr'] *
                            f[row['dat_medicao'].month][0] +
                            f[row['dat_medicao'].month][1]
                    )

                )
            )

        p_119 = pd.DataFrame.from_dict(p_119)
        self.vaz_calculada = p_119
        return self.vaz_calculada

class P116(Posto):
    def calcula(self, dados):
        '''
        v(116) = v(119) - v(301) = v(301=118) * (a-1) + b')
        '''

        posto_calculado = list()
        f = {
            1: [1.217, +0.608],
            2: [1.232, +0.123],
            3: [1.311, -2.359],
            4: [1.241, -0.496],
            5: [1.167, +0.467],
            6: [1.333, -0.533],
            7: [1.247, -0.374],
            8: [1.200, +0.360],
            9: [1.292, -1.292],
           10: [1.250, -0.250],
           11: [1.294, -1.682],
           12: [1.215, +0.729],
        }

        for index, row in pd.DataFrame(dados.loc[dados['num_posto'] == 118]).iterrows():
            posto_calculado.append(
                dict(
                    num_posto=116,
                    dat_medicao=row['dat_medicao'],
                    val_vaz_natr=row['val_vaz_natr'] *
                                 (f[row['dat_medicao'].month][0] - 1) +
                                 f[row['dat_medicao'].month][1]
                )
            )

        df_calculado = pd.DataFrame.from_dict(posto_calculado)
        self.vaz_calculada = df_calculado
        return self.vaz_calculada

class P318(Posto):
    def calcula(self, dados):
        p_116 = P116()
        p_116.calcula(dados=dados)
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_318 = dict(
            num_posto=[318] * p_116.vaz_calculada['dat_medicao'].count(),
            dat_medicao=p_301['dat_medicao'],
            val_vaz_natr=(
                    p_116.vaz_calculada['val_vaz_natr'].values +
                    0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) +
                    p_117['val_vaz_natr'].values + p_301['val_vaz_natr'].values
            )
        )

        p_318 = pd.DataFrame.from_dict(p_318)
        self.vaz_calculada = p_318
        return self.vaz_calculada

class P37(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_237 = pd.DataFrame(dados.loc[dados['num_posto'] == 237])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_37 = pd.DataFrame.from_dict(
            dict(
                num_posto=[37] * p_237['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_237['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_37
        return self.vaz_calculada

        return None

class P38(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_238 = pd.DataFrame(dados.loc[dados['num_posto'] == 238])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_38 = pd.DataFrame.from_dict(
            dict(
                num_posto=[38] * p_238['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_238['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_38
        return self.vaz_calculada

class P39(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_239 = pd.DataFrame(dados.loc[dados['num_posto'] == 239])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_39 = pd.DataFrame.from_dict(
            dict(
                num_posto=[39] * p_239['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_239['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_39
        return self.vaz_calculada

class P40(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_240 = pd.DataFrame(dados.loc[dados['num_posto'] == 240])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_40 = pd.DataFrame.from_dict(
            dict(
                num_posto=[40] * p_240['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_240['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_40
        return self.vaz_calculada

class P42(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_242 = pd.DataFrame(dados.loc[dados['num_posto'] == 242])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_42 = pd.DataFrame.from_dict(
            dict(
                num_posto=[42] * p_242['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_242['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_42
        return self.vaz_calculada

class P43(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_243 = pd.DataFrame(dados.loc[dados['num_posto'] == 243])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_43 = pd.DataFrame.from_dict(
            dict(
                num_posto=[43] * p_243['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_243['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_43
        return self.vaz_calculada

class P45(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_245 = pd.DataFrame(dados.loc[dados['num_posto'] == 245])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_45 = pd.DataFrame.from_dict(
            dict(
                num_posto=[45] * p_245['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_245['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_45
        return self.vaz_calculada

class P46(Posto):
    def calcula(self, dados):
        '''
        VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301)
        '''
        p_246 = pd.DataFrame(dados.loc[dados['num_posto'] == 246])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_46 = pd.DataFrame.from_dict(
            dict(
                num_posto=[46] * p_246['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_246['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_46
        return self.vaz_calculada

class P66(Posto):
    def calcula(self, dados):
        '''VAZ(237)-0.1*(VAZ(161)-VAZ(117)-VAZ(301))-VAZ(117)-VAZ(301).'''

        p_266 = pd.DataFrame(dados.loc[dados['num_posto'] == 266])
        p_161 = pd.DataFrame(dados.loc[dados['num_posto'] == 161])
        p_117 = pd.DataFrame(dados.loc[dados['num_posto'] == 117])
        p_301 = pd.DataFrame(dados.loc[dados['num_posto'] == 118])

        p_66 = pd.DataFrame.from_dict(
            dict(
                num_posto=[66] * p_266['dat_medicao'].count(),
                dat_medicao=dados['dat_medicao'].unique(),
                val_vaz_natr=(
                        p_266['val_vaz_natr'].values -
                        0.1 * (p_161['val_vaz_natr'].values - p_117['val_vaz_natr'].values - p_301['val_vaz_natr'].values) -
                        p_117['val_vaz_natr'].values -
                        p_301['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_66
        return self.vaz_calculada

class P298(Posto):
    def calcula(self, dados):
        p_125 = pd.DataFrame(dados.loc[dados['num_posto'] == 125])

        p_298 = list()
        for i, row in p_125.iterrows():
            if row['val_vaz_natr'] <= 190.0:
                p_298.append(
                    dict(
                        num_posto=298,
                        dat_medicao=row['dat_medicao'],
                        val_vaz_natr=row['val_vaz_natr'] * 119.0 / 190.0
                    )
                )
            else:
                if row['val_vaz_natr'] <= 209.0:
                    p_298.append(
                        dict(
                            num_posto=298,
                            dat_medicao=row['dat_medicao'],
                            val_vaz_natr=209.0
                        )
                    )
                else:
                    if row['val_vaz_natr'] <= 250.0:
                        p_298.append(
                            dict(
                                num_posto=298,
                                dat_medicao=row['dat_medicao'],
                                val_vaz_natr=row['val_vaz_natr'] - 90.0
                            )
                        )
                    else:
                        p_298.append(
                            dict(
                                num_posto=298,
                                dat_medicao=row['dat_medicao'],
                                val_vaz_natr=160.0
                            )
                        )

        p_298 = pd.DataFrame.from_dict(p_298)
        self.vaz_calculada = p_298
        return self.vaz_calculada

class P304(Posto):
    def calcula(self, dados):
        p_315 = P315()
        p_315.calcula(dados=dados)
        p_316 = P316()
        p_316.calcula(dados=dados)

        p_304 = pd.DataFrame().from_dict(
            dict(
                num_posto=[304] * p_315.vaz_calculada['dat_medicao'].count(),
                dat_medicao=p_315.vaz_calculada['dat_medicao'],
                val_vaz_natr=p_315.vaz_calculada['val_vaz_natr'].values - p_316.vaz_calculada['val_vaz_natr'].values
            )
        )

        self.vaz_calculada = p_304

        return self.vaz_calculada

class P127(Posto):
    def calcula(self, dados):
        p_129 = pd.DataFrame(dados.loc[dados['num_posto'] == 129])
        p_298 = P298()
        p_298.calcula(dados=dados)
        p_304 = P304()
        p_304.calcula(dados=dados)
        p_203 = P203()
        p_203.calcula(dados=dados)

        p_127 = pd.DataFrame.from_dict(
            dict(
                num_posto=[127] * p_129['dat_medicao'].count(),
                dat_medicao=p_129['dat_medicao'],
                val_vaz_natr=p_129.loc[:, 'val_vaz_natr'].values -
                             p_298.vaz_calculada.loc[:, 'val_vaz_natr'].values -
                             p_304.vaz_calculada.loc[:, 'val_vaz_natr'].values +
                             p_203.vaz_calculada.loc[:, 'val_vaz_natr'].values
            )
        )

        self.vaz_calculada = p_127
        return self.vaz_calculada

class P317(Posto):
    def calcula(self, dados):
        p_201 = pd.DataFrame(dados.loc[dados['num_posto'] == 201])
        p_317 = list()
        for i, row in p_201.iterrows():
            p_317.append(
                dict(
                    num_posto=317,
                    dat_medicao=row['dat_medicao'],
                    val_vaz_natr=max(0.0, row['val_vaz_natr'] - 25)
                )
            )

        p_317 = pd.DataFrame.from_dict(p_317)
        self.vaz_calculada = p_317
        return self.vaz_calculada

class P315(Posto):
    def calcula(self, dados):
        p_203 = P203()
        p_203.calcula(dados=dados)
        p_201 = pd.DataFrame(dados.loc[dados['num_posto'] == 201])
        p_317 = P317()
        p_317.calcula(dados=dados)
        p_298 = P298()
        p_298.calcula(dados=dados)

        p_315 = pd.DataFrame.from_dict(
            dict(
                num_posto=[315] * p_201['dat_medicao'].count(),
                dat_medicao=p_201['dat_medicao'],
                val_vaz_natr=(
                        (p_203.vaz_calculada['val_vaz_natr'].values - p_201['val_vaz_natr'].values) +
                        p_317.vaz_calculada['val_vaz_natr'].values +
                        p_298.vaz_calculada['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_315
        return self.vaz_calculada

class P316(Posto):
    def calcula(self, dados):
        p_315 = P315()
        p_315.calcula(dados=dados)

        val_vaz_natr = list()
        for i, row in p_315.vaz_calculada.iterrows():
            val_vaz_natr.append(
                min(row['val_vaz_natr'], 190.0)
            )

        p_316 = pd.DataFrame.from_dict(
            dict(
                num_posto=[316] * p_315.vaz_calculada['dat_medicao'].count(),
                dat_medicao=p_315.vaz_calculada['dat_medicao'],
                val_vaz_natr=val_vaz_natr
            )
        )

        self.vaz_calculada = p_316
        return self.vaz_calculada

class P132(Posto):
    def calcula(self, dados):
        p_201 = pd.DataFrame(dados.loc[dados['num_posto'] == 201])
        p_202 = pd.DataFrame(dados.loc[dados['num_posto'] == 202])

        val_vaz_natr = list()

        for i, row in p_202.iterrows():
            val_vaz_natr.append(
                row['val_vaz_natr'] +
                min(p_201.loc[p_201['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values, 25.0)
            )

        p_132 = pd.DataFrame.from_dict(
            dict(
                num_posto=[132] * p_201['dat_medicao'].count(),
                dat_medicao=p_201['dat_medicao'],
                val_vaz_natr=val_vaz_natr
            )
        )

        self.vaz_calculada = p_132
        return self.vaz_calculada

class P75(Posto):
    def calcula(self, dados):
        p_76 = pd.DataFrame(dados.loc[dados['num_posto'] == 76])
        p_73 = pd.DataFrame(dados.loc[dados['num_posto'] == 73])

        val_vaz_natr = list()
        for i, row in p_73.iterrows():
            val_vaz_natr.append(min(row['val_vaz_natr'], 173.50))

        p_75 = pd.DataFrame.from_dict(
            dict(
                num_posto=[75] * p_76['dat_medicao'].count(),
                dat_medicao=p_76['dat_medicao'],
                val_vaz_natr=val_vaz_natr
            )
        )

        self.vaz_calculada = p_75
        return self.vaz_calculada

class P303(Posto):
    def calcula(self, dados):
        p_132 = P132()
        p_132.calcula(dados=dados)
        p_316 = P316()
        p_316 = p_316.calcula(dados=dados)
        p_131 = P131()
        p_131.calcula(dados=dados)
        p_123 = pd.DataFrame(dados.loc[dados['num_posto'] == 123])

        val_vaz_natr = list()
        for i, row in p_132.vaz_calculada.iterrows():

            if row['val_vaz_natr'] < 17.0:
                val_vaz_natr.append(
                    p_132.vaz_calculada.loc[i, 'val_vaz_natr'] +
                    min(
                        p_316.loc[p_316['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values -
                        p_131.vaz_calculada.loc[p_131.vaz_calculada['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values -
                        p_123.loc[p_123['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values,
                        34.0
                    )
                )
            else:
                val_vaz_natr.append(
                    17.0 +
                    min(
                        p_316.loc[p_316['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values -
                        (p_131.vaz_calculada.loc[p_131.vaz_calculada['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values +
                         p_123.loc[p_123['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values),
                        34.0
                    )
                )

        p_303 = pd.DataFrame.from_dict(
            dict(
                num_posto=[303] * p_316['dat_medicao'].count(),
                dat_medicao=p_316['dat_medicao'],
                val_vaz_natr=val_vaz_natr
            )
        )

        self.vaz_calculada = p_303
        return self.vaz_calculada

class P126(Posto):
    def calcula(self, dados):
        p_127 = P127()
        p_127.calcula(dados=dados)
        p_123 = pd.DataFrame(dados.loc[dados['num_posto'] == 123])
        val_vaz_natr = list()

        for i, row in p_123.iterrows():

            if p_127.vaz_calculada.loc[p_127.vaz_calculada['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values <= 430.0:

                val_vaz_natr.append(
                    max(
                        0.0,
                        p_127.vaz_calculada.loc[p_127.vaz_calculada['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values - 90.0
                    ) + p_123.loc[i, 'val_vaz_natr']
                )

            else:
                val_vaz_natr.append(
                    340.0 + p_123.loc[p_123.loc[p_123['dat_medicao'] == row['dat_medicao']], 'val_vaz_natr']

                )

        p_126 = pd.DataFrame.from_dict(
            dict(
                num_posto=[127] * p_123['dat_medicao'].count(),
                dat_medicao=p_123['dat_medicao'],
                val_vaz_natr=val_vaz_natr
            )
        )

        self.val_calculada = p_126
        return self.val_calculada

class P299(Posto):
    def calcula(self, dados):
        p_130 = pd.DataFrame(dados.loc[dados['num_posto'] == 130])
        p_123 = pd.DataFrame(dados.loc[dados['num_posto'] == 123])
        p_203 = P203()
        p_203.calcula(dados=dados)
        p_298 = P298()
        p_298.calcula(dados=dados)
        p_304 = P304()
        p_304.calcula(dados=dados)

        p_299 = pd.DataFrame.from_dict(
            dict(
                num_posto=[299] * p_130['dat_medicao'].count(),
                dat_medicao=p_130['dat_medicao'],
                val_vaz_natr=(
                    p_130['val_vaz_natr'].values -
                    p_298.vaz_calculada['val_vaz_natr'].values -
                    p_203.vaz_calculada['val_vaz_natr'].values +
                    p_304.vaz_calculada['val_vaz_natr'].values +
                    p_123['val_vaz_natr'].values
                )
            )
        )

        self.vaz_calculada = p_299
        return self.vaz_calculada

class P131(Posto):
    def calcula(self, dados):
        p_316 = P316()
        p_316.calcula(dados=dados)
        p_123 = pd.DataFrame(dados.loc[dados['num_posto'] == 123])

        val_vaz_natr = list()
        for i, row in p_123.iterrows():
            val_vaz_natr.append(
                min(
                    p_316.vaz_calculada.loc[p_316.vaz_calculada['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values,
                    144.0
                ) + p_123.loc[p_123['dat_medicao'] == row['dat_medicao'], 'val_vaz_natr'].values
            )

        p_131 = pd.DataFrame.from_dict(
            dict(
                num_posto=[131] * p_316.vaz_calculada['dat_medicao'].count(),
                dat_medicao=p_316.vaz_calculada['dat_medicao'],
                val_vaz_natr=val_vaz_natr
            )
        )

        self.vaz_calculada = p_131
        return self.vaz_calculada

class P306(Posto):
    def calcula(self, dados):
        p_303 = P303()
        p_303.calcula(dados=dados)
        p_131 = P131()
        p_131.calcula(dados=dados)

        p_303 = pd.DataFrame.from_dict(
            dict(
                num_posto=[303] * p_131.vaz_calculada['dat_medicao'].count(),
                dat_medicao=p_131.vaz_calculada['dat_medicao'],
                val_vaz_natr=p_303.vaz_calculada['val_vaz_natr'].values + p_131.vaz_calculada['val_vaz_natr'].values
            )
        )

class P292(Posto):
    def calcula(self, dados):
        f = {
            1:1100.0,
            2:1600.0,
            3:4000.0,
            4:8000.0,
            5:4000.0,
            6:2000.0,
            7:1200.0,
            8:900.0,
            9:750.0,
            10:700.0,
            11:800.0,
            12:900.0,
        }
        p_292 = list()
        p_288 = pd.DataFrame(dados.loc[dados['num_posto'] == 288])
        for i, row in p_288.iterrows():

            if row['val_vaz_natr'] <= f[row['dat_medicao'].month]:
                val_vaz_natr = 0

            else:

                if row['val_vaz_natr'] <= f[row['dat_medicao'].month] + 13900.0:
                    val_vaz_natr = row['val_vaz_natr'] - f[row['dat_medicao'].month]

                else:
                    val_vaz_natr = 13900.0

            p_292.append(
                dict(
                    num_posto = 292,
                    dat_medicao=row['dat_medicao'],
                    val_vaz_natr=val_vaz_natr
                )
            )

        self.vaz_calculada = pd.DataFrame.from_dict(p_292)
        return self.vaz_calculada

class P302(Posto):
    def calcula(self, dados):
        p_288 = pd.DataFrame(dados.loc[dados['num_posto'] == 288])
        p_292 = P292()
        p_292.calcula(dados=dados)

        p_302 = pd.DataFrame.from_dict(
            dict(
                num_posto=[302] * p_288['dat_medicao'].count(),
                dat_medicao=p_288['dat_medicao'],
                val_vaz_natr=p_288['val_vaz_natr'].values - p_292.vaz_calculada['val_vaz_natr'].values
            )
        )

        self.vaz_calculada = p_302
        return self.vaz_calculada

class P203(Posto):
    def calcula(self, dados):
        p_203 = pd.DataFrame(dados.loc[dados['num_posto'] == 201])
        p_203['num_posto'] = 203
        self.vaz_calculada = p_203
        return self.vaz_calculada
