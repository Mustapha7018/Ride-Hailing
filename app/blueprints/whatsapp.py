from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from app.models import User
from app import db

whatsapp_bp = Blueprint("whatsapp", __name__)
user_sessions = {}  # Temporary in-memory session storage


@whatsapp_bp.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_message = request.form.get("Body", "").strip().lower()
    phone_number = request.form.get("From")[-10:]  # Extract last 10 digits
    response = MessagingResponse()

    greetings = ["hi", "hello", "hey"]

    # Handle greetings or start of conversation
    if incoming_message in greetings:
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            response.message(
                f"👋 Hi {user.full_name}! Welcome back.\n"
                "1️⃣ Book a Ride 🚖\n"
                "2️⃣ Manage Account ⚙️\n"
                "Type '1' or '2' to proceed."
            )
        else:
            user_sessions[phone_number] = {"step": "get_name"}
            response.message(
                "👋 Welcome! You don't have an account.\n"
                "Please enter your full name to get started."
            )
        return str(response)

    # Handle user registration steps
    if phone_number in user_sessions:
        session = user_sessions[phone_number]
        step = session.get("step")

        if step == "get_name":
            session["full_name"] = incoming_message.title()  # Capitalize name
            session["step"] = "get_role"
            response.message("Great! Are you a Driver or a Passenger? 🚗")
            return str(response)

        elif step == "get_role":
            role = incoming_message.lower()
            if role not in ["driver", "passenger"]:
                response.message("Please specify if you're a 'Driver' or 'Passenger'.")
                return str(response)

            session["role"] = role
            session["step"] = "get_emergency_contact"
            response.message("Almost done! Provide your emergency contact number. 📞")
            return str(response)

        elif step == "get_emergency_contact":
            emergency_contact = incoming_message
            if not emergency_contact.isdigit() or len(emergency_contact) < 10:
                response.message(
                    "Please provide a valid emergency contact number (10 digits). 📞"
                )
                return str(response)

            session["emergency_contact"] = emergency_contact
            new_user = User(
                full_name=session["full_name"],
                phone_number=phone_number,
                role=session["role"],
                emergency_contact=session["emergency_contact"],
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                response.message(
                    "🎉 Account created successfully! You can now book rides. 🚖\n\n"
                    "1️⃣ Book a Ride 🚖\n"
                    "2️⃣ Manage Account ⚙️\n"
                    "Type '1' or '2' to proceed."
                )
            except Exception:
                db.session.rollback()
                response.message("😟 An error occurred while creating your account. Please try again.")
            del user_sessions[phone_number]
            return str(response)

    # Handle existing user interactions
    user = User.query.filter_by(phone_number=phone_number).first()
    if user:
        if incoming_message == "1":
            response.message("🚘 Let's book a ride! Please share your location.")
        elif incoming_message == "2":
            response.message("⚙️ Manage Account (Feature coming soon).")
        else:
            response.message(
                "👋 Welcome back!\n"
                "1️⃣ Book a Ride 🚖\n"
                "2️⃣ Manage Account ⚙️\n"
                "Type '1' or '2' to proceed."
            )
    else:
        # If user somehow interacts without an account
        user_sessions[phone_number] = {"step": "get_name"}
        response.message(
            "😟 You don't have an account.\n"
            "Please enter your full name to register. 📝"
        )

    return str(response)
