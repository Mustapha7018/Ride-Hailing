from flask import Flask
from app.models import db
from app.blueprints.user import user_bp
from app.blueprints.whatsapp import whatsapp_bp
from config import config
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(whatsapp_bp)


if __name__ == "__main__":
    app.run(port=5002, debug=True)
