import csv
import requests

# Function to search movie info using TMDB API
def search_movie_info(api_key, movie_title, movie_year):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['total_results'] > 0:
            # Assuming the first result is the movie you want
            movie = next((m for m in data['results'] if m['release_date'][:4] == movie_year), None)
            if movie:
                movie_id = movie['id']
                overview = movie['overview']
                keywords_url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={api_key}"
                keywords_response = requests.get(keywords_url)
                if keywords_response.status_code == 200:
                    keywords_data = keywords_response.json()
                    keywords = [keyword['name'] for keyword in keywords_data['keywords']]
                else:
                    keywords = []
                return overview, keywords
    return None, None

# Read titles and years from CSV
movies = []
with open('output.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        movies.append({'title': row[0], 'year': row[1]})

# API key
api_key = '49222d07d88c367bd8dd466ce7eccbf1'

# Search info for each movie
for movie in movies:
    overview, keywords = search_movie_info(api_key, movie['title'], movie['year'])
    movie['overview'] = overview
    movie['keywords'] = keywords

# Write data to a new CSV file
with open('output_with_info.csv', 'w', newline='') as csvfile:
    fieldnames = ['Title', 'Year', 'Overview', 'Keywords']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for movie in movies:
        writer.writerow({'Title': movie['title'], 'Year': movie['year'],
                         'Overview': movie['overview'],
                         'Keywords': ', '.join(movie['keywords']) if movie['keywords'] else ''})
