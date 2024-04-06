from typing import Any, Iterable, Type

# Function to parse JSON articles and insert into database if valid
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from ..db_exceptions import AddError, DatabaseError, DeleteError, UpdateError
from ..news_tables import Base, NewsArticleORM, NewsArticleSummaryORM

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
        
        
    def get_all(self, db: Session) -> Iterable[A]:
        return db.query(self.model).all()

    def get_n(self, db: Session, n: int) -> Iterable[A]:
        if n > 0:
            return db.query(self.model).limit(n).all()
        elif n == -1:
            return db.query(self.model).all()
        else:
            return None

    def get_by_id(self, obj_id: int, db: Session) -> A:
        return db.query(self.model).filter_by(id=obj_id).first()
    
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