from typing import Any, Iterable, Type

# Function to parse JSON articles and insert into database if valid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from ..db_exceptions import AddError, DatabaseError, DeleteError, UpdateError
from ..news_tables import Base, NewsArticleORM, NewsArticleSummaryORM
from pydantic import BaseModel
from icecream import ic

ic.disable()
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
        
        
    def get_all(self, db: Session, response_model: BaseModel=None) -> Iterable[A]:
        articles=db.query(self.model).all()
        
        if response_model and articles:
            articles = self._parse_to_response_model(articles, response_model=response_model)
            
        return articles

    def get_n(self, db: Session, n: int = 3, response_model: BaseModel=None) -> Iterable[A]:
        if n > 0:
            articles=db.query(self.model).limit(n).all()
        elif n == -1:
            articles=db.query(self.model).all()
        else:
            raise ValueError("n must be a positive integer or -1")
        
        from icecream import ic
        # ic(articles[0].__dict__)
        print(fr"{dir(articles[0])}")
        if response_model:
            articles = self._parse_to_response_model(articles, response_model=response_model)
            
        return articles

    def _parse_to_response_model(self, articles:list[A], response_model: BaseModel) -> Iterable[BaseModel]:

        attributes_to_parse = self._get_parsable_attributes(article=articles[0])
        
        parsed_article = []
        for article in articles:
            article_info = {
                attr:getattr(article, attr) for attr in attributes_to_parse
            }
            ic(article_info)
            article_model = response_model(**article_info)
            parsed_article.append(article_model)
            
        return parsed_article or None

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
    
    def get_by_id(self, obj_id: int, db: Session, response_model: BaseModel=None) -> A:
        article= db.query(self.model).filter_by(id=obj_id).first()
        
        if response_model and article:
            article = response_model(**article.__dict__)
            
        return article
        
        
    
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
        
# Repositories for each table
class NewsArticleRepository(BaseRepository):
    def __init__(self):
        super().__init__(NewsArticleORM)


class NewsArticleSummaryRepository(BaseRepository):
    def __init__(self):
        super().__init__(NewsArticleSummaryORM)