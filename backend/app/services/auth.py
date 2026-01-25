from app.extensions import bcrypt, db
from app.models.user import User
from app.schemas.user_schema import UserLoginDTO, UserSignupDTO
from app.exceptions import AuthenticationError, UserAlreadyExistsError, WeakPasswordError
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
import re


def verify_user(login_data: UserLoginDTO) -> str:
    """
    Verify if the user  request exists
    
    args:
        login_data: UserLoginDTO with
    """

    
    email = login_data.email
    password = login_data.password

    #Query user in database and test it
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        raise AuthenticationError()
    
    access_token = create_access_token(identity=user.id)
    
    return access_token


def create_user(signup_data: UserSignupDTO) -> None:

    username = signup_data.username
    email = signup_data.email
    password = signup_data.password

    user = User.query.filter_by(email=email).first()

    if user:
        raise UserAlreadyExistsError()

    if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$", password):
        raise WeakPasswordError()
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    new_user = User(username=username, email=email, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        raise UserAlreadyExistsError() from e

    

