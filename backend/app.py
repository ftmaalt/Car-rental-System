from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables (.env file should include SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY)
load_dotenv()

# Import Blueprints
from api.auth import auth_bp
from api.bookings import bookings_bp  # if you have bookings endpoint file
# You can add more blueprints (payments, contributors, help, etc.)

app = Flask(__name__)

# -------------------------------------------
# CORS SETTINGS
# -------------------------------------------
# Adjust the origins to match your frontend URL (localhost or Vercel)
CORS(app,
     resources={r"/api/*": {"origins": [
         "http://127.0.0.1:5500",
         "http://localhost:5500",
         "https://<your-vercel-app>.vercel.app"  # change to your real Vercel domain
     ]}},
     supports_credentials=True)

# -------------------------------------------
# REGISTER BLUEPRINTS
# -------------------------------------------
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(bookings_bp, url_prefix="/api")

# -------------------------------------------
# SIMPLE ROOT / HEALTH ENDPOINT
# -------------------------------------------
@app.route("/")
def index():
    return jsonify({
        "message": "Car Rental API is running 🚗",
        "endpoints": {
            "auth": "/api/auth/*",
            "vehicles": "/api/vehicles/*",
            "bookings": "/api/bookings/*"
        }
    })

# -------------------------------------------
# ERROR HANDLERS (OPTIONAL)
# -------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# -------------------------------------------
# RUN SERVER LOCALLY
# -------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
