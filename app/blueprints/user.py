from flask import Blueprint, request, jsonify
from app.models import db, User

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile", methods=["GET"])
def get_profile():
    """Get user profile details."""
    phone_number = request.args.get("phone_number")
    user = User.query.filter_by(phone_number=phone_number).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    profile = {
        "full_name": user.full_name,
        "role": user.role,
        "emergency_contact": user.emergency_contact,
        "phone_number": user.phone_number,
    }
    return jsonify({"profile": profile}), 200

@user_bp.route("/profile", methods=["PUT"])
def update_profile():
    """Update user profile details."""
    data = request.json
    phone_number = data.get("phone_number")
    user = User.query.filter_by(phone_number=phone_number).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if "full_name" in data:
        user.full_name = data["full_name"]
    if "role" in data:
        user.role = data["role"]
    if "emergency_contact" in data:
        user.emergency_contact = data["emergency_contact"]

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200
