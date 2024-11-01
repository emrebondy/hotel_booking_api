from flask import Blueprint, request, jsonify, redirect, url_for
from flask_expects_json import expects_json
from services.booking_service import (
    creer_reservation, obtenir_toutes_reservations, obtenir_reservation,
    modifier_reservation, supprimer_reservation, obtenir_statistiques_par_type_chambre
)
from dto.booking_schema import booking_schema

reservation_bp = Blueprint("reservation_bp", __name__)

# Route par défaut pour rediriger directement vers la liste des réservations
@reservation_bp.route("/", methods=["GET"])
def index():
    return redirect(url_for('reservation_bp.obtenir_reservations'))

# Route pour afficher toutes les réservations
@reservation_bp.route("/reservations", methods=["GET"])
def obtenir_reservations():
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 10))
    reservations = obtenir_toutes_reservations(offset, limit)
    return jsonify(reservations), 200

# Route pour afficher une seule réservation en fonction de l'id sur l'URL
@reservation_bp.route("/reservations/<reservation_id>", methods=["GET"])
def obtenir_une_reservation(reservation_id):
    reservation = obtenir_reservation(reservation_id)
    if reservation is None:
        return jsonify({"erreur": "Cette réservation n'existe pas ou n'a pas été trouvée."}), 404
    return jsonify(reservation), 200

# Route pour créer une nouvelle réservation
@reservation_bp.route("/reservations", methods=["POST"])
@expects_json(booking_schema)
def creer_nouvelle_reservation():
    data = request.json
    nouvelle_reservation = creer_reservation(data)
    return jsonify(nouvelle_reservation), 201

# Route pour modifier une réservation
@reservation_bp.route("/reservations/<reservation_id>", methods=["PUT"])
@expects_json(booking_schema)
def remplacer_reservation(reservation_id):
    data = request.json
    reservation_modifiee = modifier_reservation(reservation_id, data)
    if reservation_modifiee is None:
        return jsonify({"erreur": "Réservation introuvable"}), 404
    return jsonify(reservation_modifiee), 200

# Route pour supprimer une réservation en fonction de son id
@reservation_bp.route("/reservations/<reservation_id>", methods=["DELETE"])
def supprimer_reservation_route(reservation_id):
    reservation_supprimee = supprimer_reservation(reservation_id)
    if reservation_supprimee is None:
        return "", 204
    return "", 204

# Route pour voir seulement les types de chambres de toutes les réservations existantes
@reservation_bp.route("/statistiques/type_chambre", methods=["GET"])
def obtenir_statistiques_type_chambre():
    stats = obtenir_statistiques_par_type_chambre()
    return jsonify(stats), 200
