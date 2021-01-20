import time
import requests
import json
import pandas as pd


#takes a string address and returns longitude and latitude tuple
def adresse_to_lon_lat(adresse):
    url = "https://api-adresse.data.gouv.fr/search"
    response = requests.get(url, params = {'q': adresse, 'limit': '1'})
    result = response.json()
    longitude = result['features'][0]['geometry']['coordinates'][0]
    latitude = result['features'][0]['geometry']['coordinates'][1]
    return (longitude, latitude)


df = pd.read_csv('processed_to_geo.csv', low_memory=False)
columns = ['No_voie', 'Type_de_voie', 'Voie', 'Code_postal', 'Commune']

if 'adresse' not in df:
    df['adresse'] = df[columns].apply(lambda col: ' '.join(col.values.astype(str)), axis = 1)

df.set_index('adresse', inplace=True)
for col in ['longitude', 'latitude']:
    if col not in df:
        df[col] = ''

print(df.head())

t = time.time()
df_empty = df
df_empty = df_empty[df_empty['longitude'] == '']
df_empty = df_empty[df_empty['latitude'] == '']
print("df_empty time: ", time.time()-t, "secondes")

while not df_empty.empty:
    adresses = pd.Series(df_empty.index)
    adresses.drop_duplicates(inplace=True)

    t = time.time()
    for adresse in adresses[0:100]:
        lon, lat = adresse_to_lon_lat(adresse)
        print(f'lon={lon} lat={lat} address={adresse}')
        df['longitude'][adresse] = lon
        df['latitude'][adresse] = lat
        df_empty.drop(index=adresse, inplace=True)

    print(time.time()-t, "secondes")

    df.to_csv('processed_to_geo.csv')

    print("shape of df_empty remaining ", df_empty.shape)