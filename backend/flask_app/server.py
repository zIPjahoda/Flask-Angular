# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the server application."""

import json
import logging
import traceback
from datetime import datetime

from flask import Response, jsonify, current_app
from flask_jwt_simple import (JWTManager, jwt_required, get_jwt_identity, get_jwt)
from gevent.wsgi import WSGIServer

from backend.flask_app.api.user import user
from backend.flask_app.api.home import home

from .factory import create_app, create_user
from .http_codes import Status

logger = logging.getLogger(__name__)
app = create_app()
jwt = JWTManager(app)


@app.before_first_request
def init():
    """Initialize the application with defaults."""
    create_user(app)


@jwt.jwt_data_loader
def add_claims_to_access_token(identity):
    """Explicitly set identity and claims for jwt."""
    print("identita data loader %s" % identity)
    if identity == 'zidpadne@seznam.cz':
        roles = 'admin'
    else:
        roles = 'user'

    now = datetime.utcnow()
    return {
        'exp': now + current_app.config['JWT_EXPIRES'],
        'iat': now,
        'nbf': now,
        'sub': identity,
        'roles': roles
    }




def main():
    """Main entry point of the app."""
    try:
        port = 8080
        ip = '0.0.0.0'
        http_server = WSGIServer((ip, port), app,log=logging,error_log=logging)
        print("Server started at: {0}:{1}".format(ip, port))
        http_server.serve_forever()
    except Exception as exc:
        # logger.error(exc.message)
        logger.exception(traceback.format_exc())
    finally:
        # Do something here, vykresleni nejakeho mainu
        pass


@app.route('/', methods=['GET'])
def test_connection():
    ret = {'msg': 'Is okey'}
    return jsonify(ret), 200

app.register_blueprint(user, url_prefix='/api/user')
app.register_blueprint(home, url_prefix='/api/home')