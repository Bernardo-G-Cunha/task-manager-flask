from flask import Blueprint, request, jsonify
from app.schemas.user_schema import user_signup_schema, user_login_schema
from app.services.auth import verify_user, create_user
from app.extensions import limiter

#------------------------------------------------------------------------------------------------------------------

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    login_data = user_login_schema.load(request.get_json())
    access_token = verify_user(login_data)
    return jsonify({"success": True, "data": {"access_token": access_token}}), 200


@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("2 per minute")
def signup():
    signup_data = user_signup_schema.load(request.get_json())
    create_user(signup_data)
    return jsonify({"success": True, "message": "Successfully signed up"}), 201