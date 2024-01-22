import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)
client = MongoClient('mongodb+srv://Game_api:sI3vG3fOUjwDltxr@game.yik52gz.mongodb.net/Hackathon')
users = client['users'] 

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

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        user_data = users.find_one({'username': user, 'password': password})
        if user_data:
            return render_template('results.html')
        else:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = {
            "username": username,
            "email": email,
            "password": password
        }

        users.insert_one(new_user)

        return redirect(url_for('login')) 
    
    return render_template('register.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
