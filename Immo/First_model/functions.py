import numpy as np
# import math

def double_to_int(a):
    return int(a)

def test(df):
    return len(df)

def row_to_adress_fields(df, i):
    no_voie = str(int(df['No_voie'][i]))
    type_de_voie = df['Type_de_voie'][i].replace(' ', '+')
    voie = df['Voie'][i].replace(' ', '+')
    code_postal = str(int(df['Code_postal'][i])).replace(' ', '+')
    commune = df['Commune'][i].replace(' ', '+')
    adress = no_voie + '+' + type_de_voie + '+' + voie + '+' + code_postal + '+' + commune
    return adress