from flask import Blueprint, request, jsonify
from app.schemas import user_signup_schema, user_login_schema
from app.services import verify_user, create_user
from app.extensions import limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def login():

    """
    User login
    ---
    tags:
      - Authentication
    summary: Authenticate user and return JWT token
    description: Validates user credentials and returns a JWT access token.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: user@example.com
            password:
              type: string
              example: mySecurePassword123
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      400:
        description: Validation error
      401:
        description: Invalid credentials
    """

    login_data = user_login_schema.load(request.get_json())
    access_token = verify_user(login_data)
    return jsonify({"success": True, "data": {"access_token": access_token}}), 200


@auth_bp.route('/signup', methods=['POST'])
@limiter.limit("2 per minute")
def signup():

    """
    User registration
    ---
    tags:
      - Authentication
    summary: Create a new user account
    description: Registers a new user in the system.
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - username
          properties:
            email:
              type: string
              example: user@example.com
            password:
              type: string
              example: mySecurePassword123
            username:
              type: string
              example: johndoe
    responses:
      201:
        description: User successfully registered
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Successfully signed up
      400:
        description: Validation error
      409:
        description: User already exists
    """

    signup_data = user_signup_schema.load(request.get_json())
    create_user(signup_data)
    return jsonify({"success": True, "message": "Successfully signed up"}), 201