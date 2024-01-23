from curses import flash
import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from flask_pymongo import PyMongo
import requests


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://aykill:123456789@6b9d25ac-cc65-4e9c-8b56-1ba40bdd6c13.hackathon-events-3530.mongo.a.osc-fr1.scalingo-dbs.com:34233/hackathon-events-3530?replicaSet=hackathon-events-3530-rs0&ssl=true"

mongo = PyMongo(app)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
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
        users = mongo.db.users
        print(users)
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

#define a logout function 
@app.route('/logout')
def logout():
    requests.session.pop('logged_in', None)
    flash("You were logged out", 'info')
    return redirect(url_for('hello'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
