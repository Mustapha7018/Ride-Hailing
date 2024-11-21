from flask import Blueprint, request, jsonify
from app.models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate incoming data
    full_name = data.get('full_name')
    role = data.get('role')
    phone_number = data.get('phone_number')
    emergency_contact = data.get('emergency_contact')

    if not all([full_name, role, phone_number, emergency_contact]):
        return jsonify({'error': 'All fields are required'}), 400

    if role not in ['driver', 'passenger']:
        return jsonify({'error': 'Role must be either "driver" or "passenger"'}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(phone_number=phone_number).first()
    if existing_user:
        return jsonify({'error': 'User with this phone number already exists'}), 409

    # Create a new user
    new_user = User(
        full_name=full_name,
        phone_number=phone_number,
        role=role,
        emergency_contact=emergency_contact
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    # Check if user exists
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'Login successful', 'user': {
        'full_name': user.full_name,
        'role': user.role,
        'emergency_contact': user.emergency_contact
    }}), 200
