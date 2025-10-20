from flask import Blueprint, request, jsonify
from db.init_supabase import get_supabase_client

bookings_bp = Blueprint("bookings", __name__)
supabase = get_supabase_client()

# Create booking
@bookings_bp.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()
    required = ["user_id", "vehicle_id", "start_at", "end_at"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing fields"}), 400

    result = supabase.table("bookings").insert({
        "user_id": data["user_id"],
        "vehicle_id": data["vehicle_id"],
        "start_at": data["start_at"],
        "end_at": data["end_at"],
        "total_amount": data.get("total_amount", 0.00),
        "status": "confirmed"
    }).execute()

    return jsonify({"message": "Booking created", "data": result.data}), 201


# Cancel booking
@bookings_bp.route("/bookings/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    result = supabase.table("bookings").update({"status": "cancelled"}).eq("id", booking_id).execute()
    if not result.data:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify({"message": "Booking cancelled successfully"}), 200
