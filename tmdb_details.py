import requests
import json
import pandas as pd

api_key = ''
language = 'en-US'
focal_url = 'http://api.themoviedb.org/3/list/509ec17b19c2950a0600050d?api_key=' +  api_key
api_params={'api_key':api_key,'language':language}

response = requests.get(focal_url, params=api_params)

# Arquivo com nomes padronizados dos vencedores do oscar

filename = 'films.txt'
file = open(filename, 'r')
oscar_films_names = file.readlines()
for i in range(len(oscar_films_names) - 1):
    oscar_films_names[i] = oscar_films_names[i][:-1]

# Lista com os ids de cada filme

movies_ids = []
movies_data = response.json()['items']
for film in movies_data:
    movies_ids.append([film['title'] , film['id']])
movies_ids.reverse()


# Adicionando filmes recentes fora da lista dos vencedores do oscar

last_films = [['parasite-2019' , 496243],
               ['nomadland',581734],
               ['coda-2021',776503],
               ['everything-everywhere-all-at-once',545611]]
first_film = ['sunrise-a-song-of-two-humans',631]

movies_ids.extend(last_films)
movies_ids.insert(0,first_film)
del movies_ids[-21]

# Renomeando os filmes de acordo com o padrão

for i in range(len(movies_ids)):
    movies_ids[i][0] = oscar_films_names[i]

# Montando dataframe com os detalhes técnicos de cada filme

movie_specifications = []

for film in movies_ids:
    movie_id = str(film[1])
    movie_name = film[0]

    url =  'http://api.themoviedb.org/3/movie/' + movie_id
    responseJSON = requests.get(url, params =api_params).json()

    genres = ''
    genresobj = responseJSON['genres']
    for genre in genresobj:
        genres = genres + genre['name'] + ','
    genres = genres[:-1]

    row = [movie_id, movie_name, genres, responseJSON['budget'] , responseJSON['popularity'] , responseJSON['release_date'] , responseJSON['vote_average'] , responseJSON['runtime'] ]
    movie_specifications.append(row)
    

fields = ['id' , 'name' , 'genres' , 'budget' , 'popularity' , 'release_date' , 'vote_average' , 'runtime']

df = pd.DataFrame(movie_specifications, columns=fields)

# Preenchimento de dados incompletos
df.at[0,'budget'] = 200000
df.at[9,'budget'] = 2183000
df.at[10,'budget'] = 699000
df.at[22,'budget'] = 2000000


df.to_csv('detalhes_tecnicos_oscar.csv')

