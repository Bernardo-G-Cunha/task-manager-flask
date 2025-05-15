from app.extensions import bcrypt
from app.models.user import User

def verify_user(email: str, password: str) -> User:
    
    #Query user in database and test it
    user = User.query.filter_by(email=email).first()

    if not(email == user.email) or not(bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
        raise ValueError("Invalid credentials")
    
    return user