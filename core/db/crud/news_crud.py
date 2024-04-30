from typing import Any, Iterable, Type

from icecream import ic
from pydantic import BaseModel
# Function to parse JSON articles and insert into database if valid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..db_exceptions import AddError, DatabaseError, DeleteError, UpdateError
from ..news_tables import Base, NewsArticleORM, NewsArticleSummaryORM

ic.enable()
A = Type[Base]

class BaseRepository:
    def __init__(self, model: Type):
        self.model = model

    def map_to_orm(self, obj: Any) -> A:
        """
        Map the attributes of the input object to the ORM model.
        
        Parameters:
        obj (Any): The input object to be mapped.
        
        Returns:
        any: The mapped ORM model instance.
        """
        if isinstance(obj, self.model):
            return obj
        
        mapped_obj = self.model()
        for key, value in obj.__dict__.items():
            if hasattr(mapped_obj, key):
                setattr(mapped_obj, key, value)
        return mapped_obj

    def add(self, obj: A, db: Session) -> A:
        """
        Add the object to the database and return the added ORM instance.
        
        Parameters:
        obj (A): The object to be added of the ArticleORM class.
        db (Session): The database session.
        
        Returns:
        obj (A): The added ORM instance.
        """
        orm_obj = self.map_to_orm(obj)
        db.add(orm_obj)
        try:
            db.commit()
            db.refresh(orm_obj)
            return orm_obj
        except IntegrityError:
            db.rollback()
            raise AddError(f"Error adding object: {obj}")
        except SQLAlchemyError as e:
            db.rollback()
            raise DatabaseError(f"Error adding object: {e}")
        
    def update(self, obj_id: int, updates: dict, db: Session) -> A:
        """
        Update the object with the given ID and return the updated ORM instance.
        
        Parameters:
        obj_id (int): The ID of the object to be updated.
        updates (dict): A dictionary of updates to be applied to the object.
        db (Session): The database session.
        
        Returns:
        A: The updated ORM instance.
        """
        obj = db.query(self.model).filter_by(id=obj_id).first()
        if obj is None:
            raise UpdateError(f"Object with ID {obj_id} does not exist.")
        for key, value in updates.items():
            setattr(obj, key, value)
        try:
            db.commit()
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise UpdateError(f"Error updating object with ID {obj_id}: {e}")
        
        
    def get_all(self, db: Session, response_model: BaseModel=None, return_dict:bool=True) -> Iterable[BaseModel|dict]:
        articles=db.query(self.model).all()

        return self._return_model_or_dict(articles, response_model, return_dict)

    def get_n(self, db: Session, n: int = 3, response_model: BaseModel=None, return_dict:bool=True) -> Iterable[BaseModel|dict]:
        if n > 0:
            articles=db.query(self.model).limit(n).all()
        elif n == -1:
            articles=db.query(self.model).all()
        else:
            raise ValueError("n must be a positive integer or -1")

        return self._return_model_or_dict(articles, response_model, return_dict)

    def get_by_id(self, obj_id: int, db: Session, response_model: BaseModel=None, return_dict:bool=True) -> list[BaseModel|dict]:
        article= [db.query(self.model).filter_by(id=obj_id).first()]

        return self._return_model_or_dict(article, response_model, return_dict)
    

    def get_latest_n(self, n: int, db: Session, response_model: BaseModel=None, return_dict: bool=True) -> Iterable[BaseModel|dict]:
        """
        Get the latest `n` articles from the database.

        Args:
            n (int): The number of latest articles to retrieve.
            db (Session): The database session.
            response_model (BaseModel, optional): The Pydantic model to use for serialization. Defaults to None.
            return_dict (bool, optional): Whether to return the articles as dictionaries or Pydantic models. Defaults to True.

        Returns:
            Iterable[BaseModel|dict]: The latest `n` articles.
        """
        articles = db.query(self.model).order_by(desc(self.model.id)).limit(n).all()
        return self._return_model_or_dict(articles, response_model, return_dict)
    
    def _return_model_or_dict(self, arg0, response_model=None, return_dict=None):
        if not arg0:
            return None
        if response_model:
            arg0 = self._parse_to_response_model(arg0, response_model=response_model)
        if return_dict:
            arg0 = self._parse_to_dict(arg0)
        return arg0
        
        
    
    def delete(self, obj_id: int, db: Session) -> None:
        obj = db.query(self.model).filter_by(id=obj_id).first()
        if obj is None:
            raise DeleteError(f"Object with ID {obj_id} does not exist.")
        try:
            db.delete(obj)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise DeleteError(f"Error deleting object with ID {obj_id}: {e}")


    def _parse_to_response_model(self, articles:list[A], response_model: BaseModel) -> Iterable[BaseModel]:

        dict_articles = self._parse_to_dict(articles=articles)
        
        parsed_article = [response_model(**article_info) for article_info in dict_articles]
            
        return parsed_article or None
    
    def _parse_to_dict(self, articles:list[A]) -> Iterable[dict]:
        
        if all(isinstance(item, BaseModel) for item in articles):
            return [a.model_dump() for a in articles]
        
        attributes_to_parse = self._get_parsable_attributes(article=articles[0])
        
        dict_article = []
        for article in articles:
            article_info = {
                attr:getattr(article, attr) for attr in attributes_to_parse
            }
            dict_article.append(article_info)
        
        return dict_article or None
    
    def _get_parsable_attributes(self, article: A, not_to_parse_attributes=None):
        if not not_to_parse_attributes:
            not_to_parse_attributes = set([
                '__annotations__', '__class__', '__class_getitem__', '__delattr__', '__dict__', '__dir__', '__doc__', 
                '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', 
                '__init_subclass__', '__le__', '__lt__', '__mapper__', '__module__', '__ne__', 
                '__new__', '__orig_bases__', '__parameters__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', 
                '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__table__', '__tablename__', '__weakref__', 
                '_sa_class_manager', '_sa_instance_state', '_sa_registry', 'metadata', 'registry'
            ])
        
        return set(dir(article)).difference(not_to_parse_attributes)
    
            
# Repositories for each table
class NewsArticleRepository(BaseRepository):
    def __init__(self):
        super().__init__(NewsArticleORM)


class NewsArticleSummaryRepository(BaseRepository):
    def __init__(self):
        super().__init__(NewsArticleSummaryORM)