from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Options: 'driver', 'passenger'
    emergency_contact = db.Column(db.String(15), nullable=False)
