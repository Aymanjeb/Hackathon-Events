import os
from flask import Flask, render_template, request
from pymongo import MongoClient
import requests

app = Flask(__name__)
client = MongoClient('mongodb+srv://newData:test123@cluster0.43miro1.mongodb.net/hackathon')
db = client['users'] 

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

@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    users = db['users']
    user_data = users.find_one({'username': user, 'password': password})
    if user_data:
        return render_template('results.html')
    else:
        return render_template('login.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
