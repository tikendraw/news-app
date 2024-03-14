from pydantic import BaseModel


class BaseClass(BaseModel):
    class Config:
        orm_mode: bool = True
    
    

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
    
class Article(BaseClass):
    title: str
    content: str
    author: str
    
class ShowArticle(BaseClass):
    title: str
    content: str
    author: str
    created_at: str
    updated_at: str
