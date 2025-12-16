from app.extensions import bcrypt
from app.models.user import User
from app.exceptions.auth_exceptions import *

def verify_user(email: str, password: str) -> User:
    
    #Query user in database and test it
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        raise AuthenticationError()
    
    return user


def create_user(username: str, email: str, password: str):

    user = User.query.filter_by(email=email).first()

    if user:
        raise UserAlreadyExistsError()

    if len(password) < 8: #Adjust to consider number, letters, capsLock, etc.
        raise WeakPasswordError()
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    new_user = User(username=username, email=email, password=hashed_password)
    new_user.save()

    return new_user
    
    

