from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

from config import create_app, db, api
from models import User, Guest, Episode, Appearance

app = create_app()



class Register(Resource):
    def post(self):
        data = request.get_json() or {}
        if not data.get("username") or not data.get("password"):
            return {"error": "username and password required"}, 400
        if User.query.filter_by(username=data["username"]).first():
            return {"error": "user exists"}, 400
        user = User(username=data["username"])
        user.password_hash = data["password"]
        db.session.add(user)
        db.session.commit()
        return {"id": user.id, "username": user.username}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            return {"error": "username and password required"}, 400
        user = User.query.filter_by(username=data["username"]).first()
        if not user or not user.authenticate(data["password"]):
            return {"error": "invalid credentials"}, 401
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
        return {"access_token": token}, 200

class Episodes(Resource):
    def get(self):
        episodes = Episode.query.all()
        return [episode.to_dict(rules=("-appearances.episode",)) for episode in episodes], 200

class EpisodeDetail(Resource):
    def get(self, id):
        episode = Episode.query.get_or_404(id)
        return episode.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        episode = Episode.query.get_or_404(id)
        Appearance.query.filter_by(episode_id=id).delete()
        db.session.delete(episode)
        db.session.commit()
        return {}, 204

class Guests(Resource):
    def get(self):
        guests = Guest.query.all()
        return [guest.to_dict(rules=("-appearances.guest",)) for guest in guests], 200

class Appearances(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        required = {"guest_id", "episode_id", "rating"}
        if not data or not required.issubset(data):
            return {"error": "guest_id, episode_id, rating required"}, 400
        try:
            appearance = Appearance(
                guest_id=data["guest_id"],
                episode_id=data["episode_id"],
                rating=int(data["rating"])
            )
            db.session.add(appearance)
            db.session.commit()
            return appearance.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "invalid guest or episode ID"}, 400


api.add_resource(Register, "/register",endpoint='register')
api.add_resource(Login, "/login" ,endpoint='login')
api.add_resource(Episodes, "/episodes" ,endpoint='episodes_list')
api.add_resource(EpisodeDetail, "/episodes/<int:id>", endpoint='episodes')
api.add_resource(Guests, "/guests",endpoint='guests')
api.add_resource(Appearances, "/appearances" ,endpoint='appearances')

if __name__ == '__main__':
    print(app.url_map)
    app.run(port=5555, debug=True)
