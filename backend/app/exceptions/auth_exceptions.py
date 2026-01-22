from app.exceptions import ProblemDetailException

class AuthenticationError(ProblemDetailException):
    """Error for invalid email or password during log in."""
    def __init__(self):
        super().__init__(
            type_="errors/authentication-error",
            title="Authentication Failed",
            status=401,
            detail="Invalid email or password."
        )

class UserAlreadyExistsError(ProblemDetailException):
    """Error for existent users during sign up."""
    def __init__(self):
        super().__init__(
            type_="errors/user-already-exists",
            title="User Already Exists",
            status=409,
            detail="An account with this email already exists."
        )

class WeakPasswordError(ProblemDetailException):
    """Weak or invalid password."""
    def __init__(self):
        super().__init__(
            type_="errors/weak-password",
            title="Weak Password",
            status=400,
            detail="Password does not meet the minimum strength requirements."
        )
