import uuid
from models.bookings_db import bookings_db

def creer_reservation(data):
    reservation_id = str(uuid.uuid4())
    data["booking_id"] = reservation_id
    bookings_db[reservation_id] = data
    return data

def obtenir_toutes_reservations(offset=0, limit=10):
    toutes_reservations = list(bookings_db.values())
    return toutes_reservations[offset:offset + limit]

def obtenir_reservation(reservation_id):
    return bookings_db.get(reservation_id)

def modifier_reservation(reservation_id, data):
    if reservation_id not in bookings_db:
        return None
    bookings_db[reservation_id] = data
    bookings_db[reservation_id]["booking_id"] = reservation_id
    return bookings_db[reservation_id]

def supprimer_reservation(reservation_id):
    return bookings_db.pop(reservation_id, None)

def obtenir_statistiques_par_type_chambre():
    stats = {"SINGLE": 0, "DELUXE": 0, "SUITE": 0}
    for reservation in bookings_db.values():
        if not reservation["is_cancelled"] and reservation["room_type"] in stats:
            stats[reservation["room_type"]] += 1
    return stats
