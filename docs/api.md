# API Documentation

This file will include details about the backend endpoints, 
such as the Booking API (create & cancel booking).
It will define the request/response formats and example usage.
(Member B - responsible for backend API documentation.)
 # Booking API
## POST /bookings
Creates a new booking.
### Body
{
  "user_id": 1,
  "vehicle_id": 1,
  "start_at": "2025-10-20T09:00:00Z",
  "end_at": "2025-10-22T09:00:00Z",
  "total_amount": 80.00
}
### Response
201 Created

## DELETE /bookings/<id>
Cancels a booking.
### Response
200 OK
