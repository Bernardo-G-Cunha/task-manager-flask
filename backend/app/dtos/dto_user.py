from dataclasses import dataclass

@dataclass
class UserSignupDTO:
    username: str
    email: str
    password: str

@dataclass
class UserLoginDTO:
    email: str
    password: str
    