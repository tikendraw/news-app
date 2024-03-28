from .base_schema import BaseClass


class UserLoginCredentials(BaseClass):
    username: str
    password: str
    
class UserRegisterCredentials(BaseClass):
    username: str
    password: str
    email: str
    
class ShowUser(BaseClass):
    username: str
    email: str
    