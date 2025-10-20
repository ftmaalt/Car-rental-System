from flask import Flask, jsonify
from flask_cors import CORS
from db.init_supabase import get_supabase_client

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})

supabase = get_supabase_client()

@app.route("/")
def home():
    return "✅ Supabase connection successful!"

@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        res = supabase.table("users").select("*").execute()
        return jsonify(res.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# NEW: contributors endpoint
@app.route("/api/contributors", methods=["GET"])
def get_contributors():
    try:
        # Try the view (if you created v_contributors in SQL)
        try:
            res = supabase.table("v_contributors").select("*").execute()
        except Exception:
            # Fallback: filter directly by role column
            res = supabase.table("users").select("*").in_("role", ["developer", "code_user"]).execute()
        return jsonify(res.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
