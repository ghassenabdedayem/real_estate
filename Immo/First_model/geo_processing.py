import time
import requests
import pandas as pd


#takes a string address and returns longitude, latitude and score tuple
def adresse_to_lon_lat(adresse):
    url = "https://api-adresse.data.gouv.fr/search"
    response = requests.get(url, params = {'q': adresse, 'limit': '1'})
    result = response.json()
    longitude = result['features'][0]['geometry']['coordinates'][0]
    latitude = result['features'][0]['geometry']['coordinates'][1]
    score = result['features'][0]['properties']['score']
    return (longitude, latitude, score)


df = pd.read_csv('processed_to_geo.csv', low_memory=False,dtype={'longitude':str, 'latitude':str})

#columns= a list containing the address items
columns = ['No_voie', 'Type_de_voie', 'Voie', 'Code_postal', 'Commune']

if 'adresse' not in df:
    df['adresse'] = df[columns].apply(lambda col: ' '.join(col.values.astype(str)), axis = 1)

df.set_index('adresse', inplace=True)
for col in ['longitude', 'latitude']:
    if col not in df:
        df[col] = ''

if 'erreur' not in df:
    df['erreur'] = False

if 'score' not in df:
    df['score'] = 0.0

print(df.head())

t = time.time()
df_empty = df
df_empty = df_empty[df_empty['score'] == 0.0]
# df_empty = df_empty[df_empty['erreur'] == False]
print(f'df_empty time: {time.time()-t} sec')
print(f'df_empty shape {df_empty.shape}')

#creating a series that contains only the non duplicated addresses
adresses = pd.Series(df_empty.index)
adresses.drop_duplicates(inplace=True)

#transforming addresses into set type (that will reduce the computation time)
addresses = {a for a in adresses} 

while len(adresses) > 0:
    # to list to be able to use the sublist
    addresses_list = list(adresses)

    for adresse in addresses_list[0:min(len(addresses_list),100)]:
        try:
            t = time.time()
            lon, lat, score = adresse_to_lon_lat(adresse)
            print(f'to_lon_lat in {time.time()-t} sec')
            # print(f'lon={lon} lat={lat} score={score} address={adresse}')
            t = time.time()
            df['longitude'][adresse] = lon
            df['latitude'][adresse] = lat
            df['score'][adresse] = score
            print(f'writing in {time.time()-t} sec')
        except:
            df['erreur'] = True
            print(f'Error address={adresse}')
        t = time.time()
        #this is the f source of the f pblm
        addresses.remove(adresse)
        print(f'dropping in {time.time()-t} sec')

    df.to_csv('processed_to_geo.csv')

    print(f'shape of df_empty remaining {df_empty.shape}')