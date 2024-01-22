import os
from flask import Flask, render_template, request
import requests 

# text ext

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['movieQuery']
    movies = fetch_movies(query)
    return render_template('results.html', movies=movies)

def fetch_movies(query):
    api_key = os.getenv('API_KEY')
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}'
    response = requests.get(url)
    data = response.json()
    return data.get('results', [])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
