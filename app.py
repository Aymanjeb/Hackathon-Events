import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
import requests
#import bcrypt

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
                session['email'] = login_user['email']

                return redirect(url_for("hello"))
            
        flash('Invalid Credentials')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username': request.form['username'], 'password': request.form['password'], 'email': request.form['email']})
            session['username'] = request.form['username']
            session['email'] = request.form['email']
            return render_template('index.html')

        return redirect(url_for('choose_event'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


@app.route("/book")
def choose_event():
    if 'username' in session:
        events = fetch_events()
        return render_template('choose_event.html', events=events)



def fetch_events():
    url = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_agenda-evenements-nantes-nantes-metropole/records?select=*&where=%20date%20%3E%20now()&limit=100"
    params = {
    }
    parsed_events = []
    response = requests.get(url, params=params)
    if response.status_code == 200:
        events = response.json().get('results')
        for event in events:
            # Assuming the location data is in 'fields' -> 'geolocation'
            parsed_events.append({
                'lat': event['latitude'],
                'lon': event['longitude'],
                'nom': event['nom'],
                'description': event['description'],
                'id': event['id_manif'],
                'date' : event['date'],
                # Add other event details you need
            })
    
        return parsed_events
    else:
        return []

@app.route('/book_event', methods=['POST'])
def book_event():

    username = session['username']  
    email = session['email']
    event_id = request.form.get('event_id')
    event_name = request.form.get('event_name')
    existing_booking = mongo.db.booked_events.find_one({"username": username, "event_id": event_id, "event_name": event_name})
    if existing_booking:
        return "Event already booked", 409
    
    if not username or not event_id:
        return "Missing information", 400

    booked_event = {
        "username": username,
        "email": email,
        "event_id": event_id,
        "event_name": event_name
    }

    mongo.db.booked_events.insert_one(booked_event)
    return redirect(url_for('user_bookings'))

@app.route('/user_bookings')
def user_bookings():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if user not logged in

    username = session['username']
    user_bookings = mongo.db.booked_events.find({'username': username})
    event_ids = [booking['event_id'] for booking in user_bookings]

    # Finding other users who booked the same events
    other_users_bookings = {}
    for event_id in event_ids:
        other_users = mongo.db.booked_events.find({'event_id': event_id, 'username': {'$ne': username}})
        other_users_bookings[event_id] = [[user['username'], user['email']] for user in other_users]
    bookings = mongo.db.booked_events.find({'username': username})

    return render_template('myevents.html', bookings=list(bookings), other_users_bookings=other_users_bookings)


@app.route('/delete/<int:event_id>')
def delete_event(event_id):
    username = session['username']

    if not username:
        return "User not logged in", 401

    if not event_id:
        return "Event ID is required", 400

    # Check if the booking exists
    existing_booking = mongo.db.booked_events.find_one({"username": username, "event_id": str(event_id)})
    if not existing_booking:
        return "Booking not found", 404

    mongo.db.booked_events.delete_one({"username": username, "event_id": str(event_id)})
    return redirect(url_for('user_bookings'))

@app.route('/event_details/<int:event_id>')
def event_details(event_id):
    event = get_event_details(event_id)
    if event:
        return render_template('event_details.html', event=event)
    else:
        return "Event not found", 404
def get_event_details(event_id):

    url = "https://data.nantesmetropole.fr/api/explore/v2.1/catalog/datasets/244400404_agenda-evenements-nantes-nantes-metropole/records"
    params = {
        'limit' : 100
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        events = response.json().get('results')
        for event in events:
            if event['id_manif']==str(event_id):
                details = {
                    'lat': event['latitude'],
                    'lon': event['longitude'],
                    'nom': event['nom'],
                    'description': event['description'],
                    'id': event['id_manif'],
                    'date' : event['date'],
                    'heure_debut' : event['heure_debut'],
                    'heure_fin' : event['heure_fin'],
                    'website' : event['lieu_siteweb']
                }
                return details



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)