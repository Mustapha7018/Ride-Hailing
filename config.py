import os

class Config:
    DEBUG = os.getenv("DEBUG", True)
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    PORT = int(os.getenv("PORT", 5002))
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    # Correct the database URI setting
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql://adams:1234@localhost:5432/ridehailing"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()
