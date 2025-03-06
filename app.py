from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Home route to display the search form
@app.route('/')
def home():
    return render_template('index.html')

# Search route to handle form submission
@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['search_type']
    query = request.form['query']
    
    if search_type == 'title':
        # Search by title using the 's' parameter
        url = f"http://www.omdbapi.com/?s={query}&apikey=f44f11b"
        response = requests.get(url)
        movies = response.json().get('Search', [])
    
    elif search_type == 'year':
        # Search with a broad term and filter by year
        url = f"http://www.omdbapi.com/?s=the&apikey=f44f11b"
        response = requests.get(url)
        all_movies = response.json().get('Search', [])
        movies = [movie for movie in all_movies if movie['Year'] == query]
    
    elif search_type == 'genre':
        # Search with genre name, then filter by genre in details
        url = f"http://www.omdbapi.com/?s={query}&apikey=f44f11b"
        response = requests.get(url)
        all_movies = response.json().get('Search', [])
        movies = []
        for movie in all_movies:
            detail_url = f"http://www.omdbapi.com/?i={movie['imdbID']}&apikey=f44f11b"
            detail_response = requests.get(detail_url)
            detail = detail_response.json()
            if 'Genre' in detail and query.lower() in detail['Genre'].lower():
                movies.append(detail)
    
    elif search_type == 'cast':
        # Search with cast name, then filter by actors in details
        url = f"http://www.omdbapi.com/?s={query}&apikey=f44f11b"
        response = requests.get(url)
        all_movies = response.json().get('Search', [])
        movies = []
        for movie in all_movies:
            detail_url = f"http://www.omdbapi.com/?i={movie['imdbID']}&apikey=f44f11b"
            detail_response = requests.get(detail_url)
            detail = detail_response.json()
            if 'Actors' in detail and query.lower() in detail['Actors'].lower():
                movies.append(detail)
    
    else:
        movies = []
    
    return render_template('results.html', movies=movies)

# Run the app in debug mode
if __name__ == '__main__':
    app.run()