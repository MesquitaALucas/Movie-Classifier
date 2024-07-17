#USAR ESSE AQRUIVO
import requests
import pandas as pd

api_key = '49222d07d88c367bd8dd466ce7eccbf1'
movie_data = pd.read_csv("output.csv")

# Listas para armazenar os dados coletados
release_dates = []
overviews = []
keywords_list = []

for i in range(len(movie_data)):
    movie_title = movie_data.loc[i, 'Title']
    release_year = movie_data.loc[i, 'Year']

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
            
            # Fetch keywords
            keywords_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/keywords?api_key={api_key}"
            keywords_response = requests.get(keywords_url)
            if keywords_response.status_code == 200:
                keywords_data = keywords_response.json()
                keywords = [keyword['name'] for keyword in keywords_data['keywords']]
            else:
                keywords = []
            
            # Append data to lists
            release_dates.append(release_date)
            overviews.append(overview)
            keywords_list.append(", ".join(keywords))
        else:
            release_dates.append(None)
            overviews.append(None)
            keywords_list.append(None)
    else:
        release_dates.append(None)
        overviews.append(None)
        keywords_list.append(None)

# Add new columns to the DataFrame
movie_data['Release Date'] = release_dates
movie_data['Overview'] = overviews
movie_data['Keywords'] = keywords_list

# Save the updated DataFrame to a new CSV file
movie_data.to_csv("movie_info.csv", index=False)
