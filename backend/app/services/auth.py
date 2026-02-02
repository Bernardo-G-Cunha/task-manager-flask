from app.extensions import bcrypt, db
from app.models import User
from app.services.events import create_event
from app.dtos import UserLoginDTO, UserSignupDTO
from app.auth import AuthenticationError, UserAlreadyExistsError, WeakPasswordError
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
import re


def verify_user(login_data: UserLoginDTO) -> str:
    
    email = login_data.email
    password = login_data.password

    #Query user in database and test it
    user = User.query.filter_by(email=email, deleted_at=None).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        raise AuthenticationError()
    
    access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
    
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

        db.session.flush()

        create_event(
            entity_type="user",
            entity_id=new_user.id,
            event_type="USER_CREATED",
            actor_user_id=None,
            new_value={
                "username": new_user.username,
                "email": new_user.email
            }
        )

        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        raise UserAlreadyExistsError() from e

    

