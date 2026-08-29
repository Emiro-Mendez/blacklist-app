import os
from functools import wraps
from flask import request, jsonify

def require_bearer_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        expected_token = os.environ.get('BEARER_TOKEN', 'dev-token-12345')
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Unauthorized", "message": "Missing Authorization header"}), 401
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({"error": "Unauthorized", "message": "Invalid Authorization header format. Expected 'Bearer <token>'"}), 401
        token = parts[1]
        if token != expected_token:
            return jsonify({"error": "Unauthorized", "message": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated