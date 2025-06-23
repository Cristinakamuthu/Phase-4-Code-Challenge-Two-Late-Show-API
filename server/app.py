from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from config import app, db, api

if __name__ == '__main__':
    app.run(port=5555, debug=True)
