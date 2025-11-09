from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# Blueprints (auth is required; bookings is optional)
from api.auth import auth_bp
try:
    from api.bookings import bookings_bp
except Exception:
    bookings_bp = None

# Supabase client (for simple routes here)
from db.init_supabase import get_supabase_client
sb = get_supabase_client()

app = Flask(__name__)

# ---------- CORS ----------
CORS(app,
     resources={r"/api/*": {"origins": [
         "http://127.0.0.1:5500",
         "http://localhost:5500"
     ]}},
     supports_credentials=True)

# ---------- Register blueprints ----------
app.register_blueprint(auth_bp, url_prefix="/api")
if bookings_bp:
    app.register_blueprint(bookings_bp, url_prefix="/api")

# ---------- Simple health ----------
@app.get("/api/health")
def health():
    return jsonify({"ok": True})

# ---------- Contributors (view: v_contributors) ----------
@app.get("/api/contributors")
def contributors():
    """
    Returns developers & code users from view v_contributors.
    This uses the service-role key server-side (safe) so RLS won't block.
    """
    try:
        res = sb.table("v_contributors").select("id,name,email,role").execute()
        return jsonify(res.data or [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Root info ----------
@app.route("/")
def index():
    return jsonify({
        "message": "Car Rental API is running 🚗",
        "endpoints": {
            "health": "/api/health",
            "contributors": "/api/contributors",
            "auth": "/api/auth/*"
        }
    })

# ---------- Errors ----------
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
