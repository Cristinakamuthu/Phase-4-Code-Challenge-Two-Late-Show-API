from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from models import db, User, Guest, Episode, Appearance
from config import create_app

app = create_app()
CORS(app)
jwt = JWTManager(app)

# AUTH ROUTES

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username)
    user.password_hash = password
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.authenticate(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200


# GET ALL EPISODES

@app.route("/episodes", methods=["GET"])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([{
        "id": ep.id,
        "date": ep.date
    } for ep in episodes]), 200


# GET ONE EPISODE WITH GUESTS

@app.route("/episodes/<int:id>", methods=["GET"])
def get_episode(id):
    ep = Episode.query.get_or_404(id)

    return jsonify({
        "id": ep.id,
        "date": ep.date,
        "appearances": [{
            "id": a.id,
            "rating": a.rating,
            "guest": {
                "id": a.guest.id,
                "name": a.guest.name
            }
        } for a in ep.appearances]
    }), 200


# GET ALL GUESTS

@app.route("/guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    return jsonify([{
        "id": g.id,
        "name": g.name
    } for g in guests]), 200


# CREATE AN APPEARANCE (Protected)

@app.route("/appearance", methods=["POST"])
@jwt_required()
def create_appearance():
    data = request.get_json()
    guest_id = data.get("guest_id")
    episode_id = data.get("episode_id")
    rating = data.get("rating")

    if not all([guest_id, episode_id, rating]):
        return jsonify({"error": "Missing fields"}), 400

    appearance = Appearance(guest_id=guest_id, episode_id=episode_id, rating=rating)
    db.session.add(appearance)
    db.session.commit()

    return jsonify({
        "id": appearance.id,
        "guest_id": guest_id,
        "episode_id": episode_id,
        "rating": rating
    }), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
