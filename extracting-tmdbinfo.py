import requests
import pandas as pd

api_key = '49222d07d88c367bd8dd466ce7eccbf1'
# movie_title = 'Frozen'
# release_year = '2013'  # Example release year
movie_data = pd.read_csv("output.csv", index_col=False)

for title,year in movie_data.iterrows():
    movie_title = movie_data['Title']
    release_year = movie_data['Year']

    # Construct the API request URL
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}&year={release_year}'

    # Send the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if data['total_results'] > 0:
            movie = data['results'][0]  # Assuming the first result is the movie you want
            release_date = movie['release_date']
            overview = movie['overview']
            keywords_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/keywords?api_key={api_key}"
            keywords_response = requests.get(keywords_url)
            if keywords_response.status_code == 200:
                keywords_data = keywords_response.json()
                keywords = [keyword['name'] for keyword in keywords_data['keywords']]
            else:
                keywords = []
            print("Release Date:", release_date)
            print("Overview:", overview)
            print("Keywords:", keywords)
        else:
            print("No movie found with the title",movie_title)
            print("released in", release_year)
    else:
        print("Error occurred:", response.status_code)
