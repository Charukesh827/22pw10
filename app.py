from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = 'https://api.tmdb.org/3'


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['search_type']
    query = request.form['query']
    
    print(search_type,query)
    if search_type == 'title':
        url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
        response = requests.get(url)
        movies = response.json().get('results', [])
    
    elif search_type == 'cast':
        person_url = f"{BASE_URL}/search/person?api_key={API_KEY}&query={query}"
        person_response = requests.get(person_url)
        persons = person_response.json().get('results', [])
        if persons:
            person_id = persons[0]['id'] 
            credits_url = f"{BASE_URL}/person/{person_id}/movie_credits?api_key={API_KEY}"
            credits_response = requests.get(credits_url)
            movies = credits_response.json().get('cast', [])
        else:
            movies = []
    
    elif search_type == 'genre':
        genres_url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}"
        genres_response = requests.get(genres_url)
        print(genres_response)
        genres = genres_response.json().get('genres', [])
        genre_id = next((genre['id'] for genre in genres if genre['name'].lower() == query.lower()), None)
        print(genre_id)
        if genre_id:
            discover_url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}"
            discover_response = requests.get(discover_url)
            movies = discover_response.json().get('results', [])
        else:
            movies = []
    
    elif search_type == 'year':
        discover_url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&primary_release_year={query}"
        discover_response = requests.get(discover_url)
        movies = discover_response.json().get('results', [])
    
    else:
        movies = []
    
    return render_template('results.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True,port = 8080)