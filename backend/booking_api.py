# booking_api.py
# Minimal backend for Cruzr Booking search

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import re


# -----------------------------
# Demo inventory (replace later)
# -----------------------------
@dataclass
class Car:
    id: str
    title: str
    type: str               # SUV | Sedan | Electric | Luxury
    location: str           # City/Area
    rating: float           # e.g., 4.6
    price_per_day: int      # USD/day
    image: str              # placeholder image URL
    features: List[str]     # e.g., ["GPS","Auto","AC"]
    booked_ranges: List[Tuple[date, date]] = field(default_factory=list)  # (start, end) inclusive


INVENTORY: List[Car] = [
    Car(
        id="car_001",
        title="Tesla Model 3",
        type="Electric",
        location="San Francisco",
        rating=4.8,
        price_per_day=180,
        image="https://picsum.photos/seed/tesla/640/360",
        features=["AutoPilot", "GPS", "Heated Seats"],
        booked_ranges=[(date(2025, 11, 14), date(2025, 11, 16))]
    ),
    Car(
        id="car_002",
        title="Toyota RAV4",
        type="SUV",
        location="San Francisco",
        rating=4.5,
        price_per_day=95,
        image="https://picsum.photos/seed/rav4/640/360",
        features=["AWD", "Apple CarPlay", "AC"],
        booked_ranges=[(date(2025, 11, 10), date(2025, 11, 11))]
    ),
    Car(
        id="car_003",
        title="Mercedes C-Class",
        type="Luxury",
        location="Los Angeles",
        rating=4.7,
        price_per_day=210,
        image="https://picsum.photos/seed/merc/640/360",
        features=["Leather", "GPS", "Cruise Control"],
        booked_ranges=[]
    ),
    Car(
        id="car_004",
        title="Honda Civic",
        type="Sedan",
        location="San Francisco",
        rating=4.3,
        price_per_day=60,
        image="https://picsum.photos/seed/civic/640/360",
        features=["Eco", "Bluetooth", "AC"],
        booked_ranges=[(date(2025, 11, 20), date(2025, 11, 22))]
    ),
]


# -----------------------------
# Search service (core logic)
# -----------------------------
class SearchService:
    def __init__(self, cars: List[Car]) -> None:
        self.cars = cars

    @staticmethod
    def _normalize(s: str) -> str:
        return re.sub(r"\s+", " ", s).strip().lower()

    @staticmethod
    def _parse_date(s: str) -> date | None:
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return None

    @staticmethod
    def _ranges_overlap(a_start: date, a_end: date, b_start: date, b_end: date) -> bool:
        # overlap if both ranges share at least one day
        return not (a_end < b_start or b_end < a_start)

    def _is_available(self, car: Car, start: date, end: date) -> bool:
        for (b_start, b_end) in car.booked_ranges:
            if self._ranges_overlap(start, end, b_start, b_end):
                return False
        return True

    def search(
        self,
        pickup_location: str,
        pickup_date: str,
        dropoff_date: str,
        types: List[str] | None = None,
        price_max: int | None = None,
        rating_min: float | None = None,
        availability: str = "all",
        page: int = 1,
        per_page: int = 12,
    ) -> Dict[str, Any]:

        # validate inputs
        start = self._parse_date(pickup_date)
        end = self._parse_date(dropoff_date)
        if not start or not end or end < start:
            return {"error": "Invalid dates. Ensure pickupDate <= dropoffDate and format is YYYY-MM-DD."}

        norm_loc = self._normalize(pickup_location)
        norm_types = set(types or [])

        # filter pipeline
        results: List[Dict[str, Any]] = []
        for car in self.cars:
            # location (simple contains match)
            if norm_loc and norm_loc not in self._normalize(car.location):
                continue

            # type filter (if any boxes checked)
            if norm_types and car.type not in norm_types:
                continue

            # price/rating
            if price_max is not None and car.price_per_day > price_max:
                continue
            if rating_min is not None and car.rating < rating_min:
                continue

            # availability
            is_free = self._is_available(car, start, end)
            if availability == "available" and not is_free:
                continue

            # pack result card
            status = "Available" if is_free else "Unavailable"
            results.append({
                "id": car.id,
                "title": car.title,
                "type": car.type,
                "location": car.location,
                "rating": round(car.rating, 1),
                "pricePerDay": car.price_per_day,
                "image": car.image,
                "features": car.features,
                "status": status
            })

        # pagination
        total = len(results)
        page = max(1, page)
        per_page = max(1, min(50, per_page))
        start_i = (page - 1) * per_page
        end_i = start_i + per_page
        paged = results[start_i:end_i]

        return {
            "meta": {
                "count": len(paged),
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": math.ceil(total / per_page) if per_page else 1
            },
            "results": paged
        }


# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)
CORS(app)
service = SearchService(INVENTORY)


@app.get("/api/health")
def health():
    return {"ok": True, "service": "cruzr-booking-search"}


@app.get("/api/search")
def search():
    # Required
    pickup_location = request.args.get("pickupLocation", "").strip()
    pickup_date = request.args.get("pickupDate", "").strip()
    dropoff_date = request.args.get("dropoffDate", "").strip()

    # Optional filters
    # types can come as comma-separated or multiple query params ?type=SUV&type=Sedan
    types_multi = request.args.getlist("type")
    types_csv = request.args.get("types", "")
    types = [t for t in (types_multi or types_csv.split(",")) if t]

    price_max = request.args.get("priceMax", type=int)
    rating_min = request.args.get("rating", type=float)  # from <select name="rating">
    availability = request.args.get("availability", "all").lower()  # 'all' | 'available'
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=12, type=int)

    data = service.search(
        pickup_location=pickup_location,
        pickup_date=pickup_date,
        dropoff_date=dropoff_date,
        types=types or None,
        price_max=price_max,
        rating_min=rating_min,
        availability=availability,
        page=page,
        per_page=per_page,
    )

    status = 200 if "error" not in data else 400
    return jsonify(data), status


if __name__ == "__main__":
    # Run with: python booking_api.py
    app.run(host="0.0.0.0", port=5000, debug=True)
