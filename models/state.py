#!/usr/bin/python3
"""
State Module for HBNB project
"""
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """
    State class
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete, delete-orphan")

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
            Getter method for cities in State
            """
            from models import storage
            city_list = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

