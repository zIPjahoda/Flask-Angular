from flask import Blueprint

import json
import logging
import traceback
from datetime import datetime
from flask import Response, request, jsonify, current_app
from gevent.wsgi import WSGIServer
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity, get_jwt
)

from backend.flask_app.models import Session, User
from backend.flask_app.http_codes import Status
from backend.flask_app.factory import create_app, create_user
from flask_security.utils import hash_password, verify_password

user = Blueprint('user', __name__)

logger = logging.getLogger(__name__)


@user.route('/registers', methods=['POST'])
def register():
    logger.info('Regsiter new user')
    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)
    email = params.get('email', None)


    if not username:
        return jsonify({"msg": "Missing username parameter"}), Status.HTTP_BAD_REQUEST
    if Session.query(User).filter_by(username=username).first():
        return jsonify({"msg": "Username is already exist"}), Status.HTTP_BAD_REQUEST
    if not password or len(password) < 8:
        return jsonify({'msg': "Missing password parameter, minimum 8 characters"}), Status.HTTP_BAD_REQUEST
    if not email:
        return jsonify({'msg': "Missing email parameter"}), Status.HTTP_BAD_REQUEST
    if Session.query(User).filter_by(email=email).first():
        return jsonify({"msg": "Email is already using"}), Status.HTTP_BAD_REQUEST

    new_user = {
        'username': username,
        'password': hash_password(password),
        'email': email,
        'token': create_jwt(identity=email)}

    user = User.add(new_user)

    ret = {'jwt': user.token, 'exp': datetime.utcnow() + current_app.config['JWT_EXPIRES']}
    return jsonify(ret), 200


@user.route("/logout", methods=['POST'])
@jwt_required
def logout():
    """Logout the currently logged in user."""
    # TODO: handle this logout properly, very weird implementation.
    identity = get_jwt_identity()
    if not identity:
        return jsonify({"msg": "Token invalid"}), Status.HTTP_BAD_UNAUTHORIZED
    logger.info('Logged out user !!')
    return 'logged out successfully', Status.HTTP_OK_BASIC


@user.route('/login', methods=['POST'])
def login():
    """View function for login view."""
    logger.info('Logged in user')

    params = request.get_json()
    username = params.get('username', None)
    password = params.get('password', None)
    user = Session.query(User).filter_by(username=username).first()

    print(user)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), Status.HTTP_BAD_REQUEST
    if not password:
        return jsonify({"msg": "Missing password parameter"}), Status.HTTP_BAD_REQUEST
    if not user:
        return jsonify({"msg": "Bad password or username"}), Status.HTTP_BAD_REQUEST

    # TODO Check from DB
    if username != user.username or not verify_password(password, user.password):
        return jsonify({"msg": "Bad username or password"}), Status.HTTP_BAD_UNAUTHORIZED


    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=user.email), 'exp': datetime.utcnow() + current_app.config['JWT_EXPIRES']}
    return jsonify(ret), 200
