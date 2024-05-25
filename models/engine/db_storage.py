#!/usr/bin/python3
"""
Module for DBStorage class
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os


class DBStorage:
    """
    Interacts with the MySQL database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the DBStorage class
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the current database session for all objects of the given class
        """
        if cls:
            return {obj.to_dict()['__class__'] + '.' + obj.id: obj for obj in self.__session.query(cls).all()}
        else:
            objects = {}
            for cls in [State, City, User, Place, Review, Amenity]:
                objects.update({obj.to_dict()['__class__'] + '.' + obj.id: obj for obj in self.__session.query(cls).all()})
            return objects

    def new(self, obj):
        """
        Add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database (feature of SQLAlchemy)
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Call remove() method on the private session attribute (self.__session)
        """
        self.__session.remove()

