from flask import Flask
from flask_cors import CORS
from flask_expects_json import expects_json
from dotenv import load_dotenv
from controllers.booking_controller import reservation_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(reservation_bp)

if __name__ == "__main__":
    app.run(debug=True)
