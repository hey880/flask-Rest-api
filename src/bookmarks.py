from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
import validators
from flask_jwt_extended import get_jwt_identity
from src.database import Bookmark, db
from flasgger import Swagger, swag_from
bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
@swag_from("./docs/bookmarks/handle_bookmarks.yaml")
def handle_bookmarks():
    current_user = get_jwt_identity()

    if request.method == 'POST':

        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                'error': 'URL alread exists'
            }), HTTP_409_CONFLICT

        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)  # 수정사항에 대한 commit
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'usl': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), HTTP_201_CREATED

    else:

        bookmarks = Bookmark.query.filter_by(
            user_id=current_user)  # Get method로 호출한 경우를 의미

        data = []

        for bookmark in bookmarks:
            data.append({
                'id': bookmark.id,
                'usl': bookmark.url,
                'short_url': bookmark.short_url,
                'visit': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at
            })

        return jsonify({'data': data}), HTTP_200_OK


@bookmarks.get('/<int:id>')
@jwt_required()
@swag_from('./docs/bookmarks/get_bookmark.yaml')
def get_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(
        user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_400_BAD_REQUEST

    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visit': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,
    }), HTTP_200_OK


@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
@swag_from("./docs/bookmarks/editbookmark.yaml")
def edit_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
        }), HTTP_400_BAD_REQUEST

    bookmark.url = url  # url에 request로 받은 새 url 넣음
    bookmark.body = body  # body에 request로 받은 새 body 넣음

    db.session.commit()

    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visit': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,
    }), HTTP_200_OK


@bookmarks.delete('/<int:id>')
@jwt_required()
@swag_from("./docs/bookmarks/delete.yaml")
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
