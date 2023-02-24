from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from src.database import User, db

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password)< 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None: #first() : 첫번째에 매칭되는 인스턴스만 달라
        return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "Username is taken"}), HTTP_409_CONFLICT

    pwd_hash=generate_password_hash(password)

    user=User(username=username, password=pwd_hash, email=email) #받은 value들을 db column에 저장
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message':"User created",
        'user': {
            'username': username, 'email': email
            }
        }), HTTP_201_CREATED

@auth.get("/me")
def me():
    return {"user":"me"}