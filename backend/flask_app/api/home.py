from flask import Blueprint, request
import json
import logging

from flask import Response, jsonify, current_app
from flask_jsontools import jsonapi
from flask_jwt_simple import (JWTManager, jwt_required, get_jwt_identity, get_jwt, create_jwt)

from backend.flask_app.lib import AlchemyEncoder
from backend.flask_app.models import Session, Coin, User
from ..factory import create_app
from ..http_codes import Status

logger = logging.getLogger(__name__)
home = Blueprint('home', __name__)

app = create_app()
app.json_encoder = AlchemyEncoder


@home.route('/protected', methods=['GET'])
# @jwt_required
def get_data():
    """Get dummy data returned from the server."""
    jwt_data = get_jwt()
    print(request.headers)
    # print(jwt_data['roles'] )
    # if jwt_data['roles'] != 'admin':
    #     return jsonify(msg="Permission denied"), Status.HTTP_BAD_FORBIDDEN

    user = Session.query(User).filter_by(username='pica').first()
    create_jwt(identity=user.email)
    identity = get_jwt_identity()
    print("identita %s" %identity)
    print("jwt %s" % get_jwt())
    if not identity:
        return jsonify({"msg": "Token invalid"}), Status.HTTP_BAD_UNAUTHORIZED

    data = {'Heroes': ['Hero1', 'Hero2', 'Hero3']}
    json_response = json.dumps(data)
    return Response(json_response,
                    status=Status.HTTP_OK_BASIC,
                    mimetype='application/json')


@home.route('/coins', methods=['GET'])
# @jwt_required
def coins():

    print("kokot")
    coins =  Session.query(Coin).all()
    json_object = json.dumps(coins, cls=AlchemyEncoder)

    json_response = json.dumps({'coins':json.loads(json_object)})
    print(json_response)
    # print(json_response)
    return Response(json_response, status=Status.HTTP_OK_BASIC, mimetype='application/json')