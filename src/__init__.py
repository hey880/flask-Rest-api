from flask import Flask, config, jsonify
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            # sql alchemy의 이벤트를 처리하는 옵션, 추가적인 메모리를 필요로 하여 꺼두는 것을 추천
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),

            SWAGGER={
                'title': "Bookmarks API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    # JWT
    JWTManager(app)

    Swagger(app, config=swagger_config, template=template)

    # blueprint 등록
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    @app.get("/")
    def index():
        return "Hello world"

    @app.get("/hello")
    def say_hello():
        return {"message": "Hello world"}

    @app.errorhandler(HTTP_404_NOT_FOUND)  # 404 페이지로 이동할 경우 에러처리
    def handle_404(e):
        return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
