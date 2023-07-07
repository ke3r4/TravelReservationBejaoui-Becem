from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
db = SQLAlchemy(app)

# Modèle de données
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    hotel = db.Column(db.String(100), nullable=False)
    car_rental = db.Column(db.String(100), nullable=False)

    def __init__(self, destination, date, duration, hotel, car_rental):
        self.destination = destination
        self.date = date
        self.duration = duration
        self.hotel = hotel
        self.car_rental = car_rental

with app.app_context():
    # Création de la base de données
    db.create_all()

# Page d'accueil
@app.route('/')
def index():
    trips = Trip.query.all()
    return render_template('index.html', trips=trips)

# Ajouter une réservation
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        destination = request.form['destination']
        date = request.form['date']
        duration = int(request.form['duration'])
        hotel = request.form['hotel']
        car_rental = request.form['car_rental']

        trip = Trip(destination, date, duration, hotel, car_rental)
        db.session.add(trip)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

# Supprimer une réservation
@app.route('/delete/<int:trip_id>', methods=['POST'])
def delete(trip_id):
    trip = Trip.query.get(trip_id)
    db.session.delete(trip)
    db.session.commit()
    return redirect('/')
