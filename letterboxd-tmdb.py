import requests
from bs4 import BeautifulSoup
import csv

def scrape_letterboxd_list(list_url):
    try:
        response = requests.get(list_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        movie_titles = [movie.text.strip() for movie in soup.select('.poster-list-item-title')]
        return movie_titles
    except requests.exceptions.RequestException as e:
        print("Error fetching Letterboxd list:", e)
        return []

def search_movie_by_title(movie_title, api_key):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        search_results = response.json()
        if search_results['results']:
            return search_results['results'][0]['id']
        else:
            print("No movie found with title:", movie_title)
            return None
    except requests.exceptions.RequestException as e:
        print("Error searching for movie:", e)
        return None

def get_movie_details(movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=keywords"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        print(movie_data)  # Print the full movie data to inspect its structure
        return movie_data
    except requests.exceptions.RequestException as e:
        print("Error fetching movie details:", e)
        return None

def write_to_csv(movie_details_list, output_file):
    fields = ['Title', 'Release Year', 'Overview', 'Genres', 'Keywords']
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for movie in movie_details_list:
            writer.writerow({
                'Title': movie['title'],
                'Release Year': movie['release_date'][:4],
                'Overview': movie['overview'],
                'Genres': ', '.join(genre['name'] for genre in movie['genres']),
                'Keywords': ', '.join(keyword['name'] for keyword in movie['keywords']['keywords'])
            })

# Example usage:
list_url = "https://letterboxd.com/deltanz/list/the-definitive-horror-list-based-on-deltanzs/"  # Replace this with the URL of your Letterboxd list
api_key = "49222d07d88c367bd8dd466ce7eccbf1"  # Replace this with your TMDb API key
output_file = "movie_details.csv"  # Name of the CSV file to be created

# Scrape Letterboxd list to get movie titles
movie_titles = scrape_letterboxd_list(list_url)

movie_details_list = []

for title in movie_titles:
    # Search for movie ID using title
    movie_id = search_movie_by_title(title, api_key)
    if movie_id:
        # Retrieve movie details using movie ID
        movie_details = get_movie_details(movie_id, api_key)
        if movie_details:
            movie_details_list.append(movie_details)

# Write movie details to CSV
write_to_csv(movie_details_list, output_file)
print("CSV file created successfully.")
