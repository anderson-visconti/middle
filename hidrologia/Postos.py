import pandas as pd
class Posto(object):
    def __init__(self):
        pass

class P3(Posto):
    def calcula(self, hidro):
        print('Posto 3 = 0.0')
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
            dat_medicao=p_116.vaz_calculada['dat_medicao'],
            val_vaz_natr=(
                    p_116.vaz_calculada['val_vaz_natr'] +
                    0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) +
                    p_117['val_vaz_natr'] + p_301['val_vaz_natr']
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
                        p_237['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_238['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_239['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_240['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_242['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_243['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_245['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_246['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
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
                        p_266['val_vaz_natr'] -
                        0.1 * (p_161['val_vaz_natr'] - p_117['val_vaz_natr'] - p_301['val_vaz_natr']) -
                        p_117['val_vaz_natr'] -
                        p_301['val_vaz_natr']
                )
            )
        )

        self.vaz_calculada = p_66
        return self.vaz_calculada

class P123(Posto):
    def calcula(self, dados):
        print('Posto 123 = v(119)')
        return None
