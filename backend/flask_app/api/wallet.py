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

from backend.flask_app.models import Session, User, Wallet
from backend.flask_app.http_codes import Status
from backend.flask_app.factory import create_app, create_user
from flask_security.utils import hash_password, verify_password

wallet = Blueprint('wallet', __name__)

logger = logging.getLogger(__name__)
app = create_app()
jwt = JWTManager(app)


@wallet.route('/add', methods=['POST'])
@jwt_required
def wallet_add():
    logger.info('Add new wallet')

    identity = get_jwt_identity()
    if not identity:
        return jsonify({"msg": "Token invalid"}), Status.HTTP_BAD_UNAUTHORIZED
    if not Session.query(User).filter_by(email=identity).first():
        return jsonify({"msg": "No exist user"}), Status.HTTP_BAD_UNAUTHORIZED

    params = request.get_json()
    wallet_address = params.get('wallet_address', None)
    token_id = params.get('token_id', None)
    user = Session.query(User).filter_by(email=identity).first()

    if not wallet_address:
        return jsonify({"msg": "Missing wallet parameter"}), Status.HTTP_BAD_REQUEST
    if Session.query(User).filter_by(wallet=wallet_address).first():
        return jsonify({"msg": "wallet is already exist"}), Status.HTTP_BAD_REQUEST
    if not token_id or len(token_id) < 8:
        return jsonify({'msg': "Missing token_id parameter, minimum 8 characters"}), Status.HTTP_BAD_REQUEST


    new_wallet = {
        'id_user': user.id,
        'id_coin': token_id,
        'id_exchange': 1,
        'address': wallet_address,
        'deposit': 0
    }
    Wallet.add(new_wallet)

    # aktualizovat penezenku a ziskat aktualni zustatky

    ret = {'msg': 'Success add wallet address'}
    return jsonify(ret), 200
