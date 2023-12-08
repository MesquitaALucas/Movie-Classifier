import requests
import json
import pandas as pd

api_key = ''
language = 'en-US'
api_params={'api_key':api_key,'language':language}

df_filmes = pd.read_csv('detalhes_tecnicos_oscar.csv')
ref = df_filmes[['id' , 'name']]

cast_data = []
for i in ref.index:
    movie_id = ref.loc[i]['id']
    movie_name = ref.loc[i]['name']
    focal_url = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + '/credits'
    responseJSON = requests.get(focal_url, params=api_params).json()
    cast = responseJSON['cast']
    appearance_order = 1
    for person in cast:
        row = [person['original_name'] , person['known_for_department'] , person['popularity'] , person['gender'] ,appearance_order, movie_id]
        cast_data.append(row)
        appearance_order += 1

fields = ['name' , 'type' , 'popularity' , 'gender' , 'position' , 'movieId']
df = pd.DataFrame(cast_data,columns=fields)

df.to_csv('cast_oscar.csv')

