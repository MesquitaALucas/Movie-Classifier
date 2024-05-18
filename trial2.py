import pandas as pd
import requests

# Function to fetch movie details from TMDB API
def fetch_movie_details(title, year):
    api_key = '49222d07d88c367bd8dd466ce7eccbf1'
    base_url = 'https://api.themoviedb.org/3/search/movie'
    
    params = {
        'api_key': api_key,
        'query': title,
        'year': year
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if 'results' in data and data['results']:
        movie_id = data['results'][0]['id']
        return fetch_movie_details_by_id(movie_id)
    else:
        return None

# Function to fetch movie details by ID
def fetch_movie_details_by_id(movie_id):
    api_key = '49222d07d88c367bd8dd466ce7eccbf1'
    base_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    
    params = {
        'api_key': api_key,
        'append_to_response': 'keywords'
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if 'title' in data:
        return {
            'title': data['title'],
            'release_year': data['release_date'][:4],
            'overview': data['overview'],
            'keywords': [keyword['name'] for keyword in data['keywords']['keywords']]
        }
    else:
        return None

# Read CSV file into pandas DataFrame
df = pd.read_csv('your_csv_file.csv')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    title = row['title']
    year = row['year']
    
    # Fetch movie details
    movie_details = fetch_movie_details(title, year)
    
    if movie_details:
        print(movie_details)
    else:
        print(f"No details found for {title} ({year})")
