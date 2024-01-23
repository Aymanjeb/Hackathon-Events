import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from flask_pymongo import PyMongo
import requests
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('API_KEY')
app.config["MONGO_URI"] = os.getenv('SCALINGO_MONGO_URL')

mongo = PyMongo(app)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if login_user['password']==request.form['password']:
                session['username'] = request.form['username']
                return render_template('session.html')

        flash('Invalid username/password combination')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username': request.form['username'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return render_template('index.html')

        flash('Username already exists')
        return redirect(url_for('register'))

    return render_template('register.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
