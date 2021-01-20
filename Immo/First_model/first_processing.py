import pandas as pd
import numpy as np
import matplotlib as plt
import sklearn as sk
import seaborn as sns
import json
import time
import requests


#defining a function to concatenate adress elements and prepare it for the API request
def row_to_adress_fields(df, i, sep='+'):
    no_voie = str(int(df['No_voie'][i]))
    type_de_voie = df['Type_de_voie'][i].replace(' ', sep)
    voie = df['Voie'][i].replace(' ', sep)
    code_postal = str(int(df['Code_postal'][i]))
    commune = df['Commune'][i].replace(' ', sep)
    if no_voie == 0.0:
        adress = type_de_voie + sep + voie + sep + code_postal + sep + commune
    else:
        adress = no_voie + sep + type_de_voie + sep + voie + sep + code_postal + sep + commune
    return adress

#a function that replaces spaces by plus into a given string (phrase)
def replace_space_by_plus(phrase):
    phrase.replace(' ', '+')

def concatenate_columns(df, columns, sep='+'):
    df_temporary = df[columns[0]].apply(replace_space_by_plus)
    for column in columns[1:]:
        df_temporary += sep + df[column]

#a function to transform string into integer, and handeling exceptions with 0
def handle_special_to_int(string):
    try:
        return int(string)
    except:
        return 0

df = pd.read_csv('../Destination_2015_2019.csv', low_memory=False)

#formatting the data with appropriate index
df.rename(columns={'Unnamed: 0' : 'Id'}, inplace=True)
df.set_index(keys=['Id'], inplace=True)
df.reset_index(inplace=True)
print('formatting completed')

#dropping non interesting lines
df = df[df['No_disposition'] == 1] #on ne s'intéresse qu'aux ventes(regarde ligne suivante)
df = df[df['Nature_mutation'] == 'Vente']
print('dropping rows complete')

#dropping useless columns
df.drop(columns=['No_disposition' ], inplace=True)
df.drop(columns=['Nature_mutation'], inplace=True)
df.drop(columns=['1er_lot', 'Surface_Carrez_du_1er_lot', '2eme_lot', 'Surface_Carrez_du_2eme_lot',
       '3eme_lot', 'Surface_Carrez_du_3eme_lot', '4eme_lot',
       'Surface_Carrez_du_4eme_lot', '5eme_lot', 'Surface_Carrez_du_5eme_lot',
       'Nombre_de_lots', 'Code_type_local'], inplace=True)
df.drop(columns=['Nature_culture', 'Nature_culture_speciale'], inplace=True)
print('dropping columlns completed')

#filling NaN by 0 for integer fields and by a space for string fields
values = {'No_voie': 0, 'Type_de_voie': ' ', 'Voie': ' ', 'Code_postal': 0,
        'Valeur_fonciere': 0, 'No_voie': 0, 'Nombre_pieces_principales': 0}
df.fillna(value=values, inplace=True)
print('replacing NaN completed')

#transforming floats and strings into integers
df['Valeur_fonciere'] = df.Valeur_fonciere.apply(int)
df['No_voie'] = df.No_voie.apply(int)
df['No_voie'] = df.No_voie.apply(int)
df['Code_postal'] = df.Code_postal.apply(handle_special_to_int)
print('changed floats and strings into integers')

#creating a computed value (prince per meter)
df['Prix_par_m_bati'] = df['Valeur_fonciere']/df['Surface_reelle_bati']
df['Prix_par_m_terrain'] = df['Valeur_fonciere']/df['Surface_terrain']
df.Prix_par_m_bati.fillna(0, inplace=True)
df.Prix_par_m_terrain.fillna(0, inplace=True)
df.replace(np.inf, 0, inplace=True)
print('computation completed')

df.to_csv('processed_to_geo.csv')

