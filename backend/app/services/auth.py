from app.extensions import bcrypt
from app.models.user import User
from app.exceptions.auth_exceptions import *

def verify_user(email: str, password: str) -> User:
    
    #Query user in database and test it
    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise AuthenticationError()
    
    return user


def create_user(username: str, email: str, password: str):

    user = User.query.filter_by(email=email).first()

    if user:
        raise UserAlreadyExistsError()

    if len(password) < 8:
        raise WeakPasswordError()
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_user = User(username=username, email=email, password=hashed_password)
    new_user.save()

    return new_user
    
    

