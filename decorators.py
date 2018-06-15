from functools import wraps
from flask import jsonify, request
import jwt
from app import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:

            return jsonify({'Message' : 'Token is missing'}), 401

        try:
            validate_token = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Message' : 'Token is invalid'}), 401

        return f(*args, **kwargs)
    return decorated