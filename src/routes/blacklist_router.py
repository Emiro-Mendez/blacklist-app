from flask import Blueprint, request, jsonify
from src.services.blacklist_service import BlacklistService
from src.middleware.auth_middleware import require_bearer_token
from src.utils.validation import is_valid_email, is_valid_uuid
from src.models.errors import BadRequestError, ConflictError, NotFoundError

blacklist_bp = Blueprint('blacklist', __name__, url_prefix='/blacklists')
service = BlacklistService()

@blacklist_bp.route('/', methods=['POST'])
@require_bearer_token
def add_email():
    data = request.get_json()
    if not data:
        raise BadRequestError("Missing request body")
    email = data.get('email')
    app_uuid = data.get('app_uuid')
    reason = data.get('reason')
    if not email or not app_uuid:
        raise BadRequestError("email and app_uuid are required")
    if not is_valid_email(email):
        raise BadRequestError("Invalid email format")
    if not is_valid_uuid(app_uuid):
        raise BadRequestError("Invalid app_uuid format")
    if reason and len(reason) > 255:
        raise BadRequestError("reason must be at most 255 characters")
    entry = service.add_email(email, app_uuid, reason)
    return jsonify({"message": "Email added to blacklist", "data": entry.to_dict()}), 201

@blacklist_bp.route('/<email>', methods=['GET'])
@require_bearer_token
def check_email(email):
    if not is_valid_email(email):
        raise BadRequestError("Invalid email format")
    exists = service.check_email(email)
    return jsonify({"email": email, "is_blacklisted": exists})