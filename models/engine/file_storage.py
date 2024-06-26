#!/usr/bin/python3
"""
Module for FileStorage class
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage
        """
        if cls is None:
            return FileStorage.__objects
        else:
            filtered_objects = {}
            for key, value in FileStorage.__objects.items():
                if type(value) == cls:
                    filtered_objects[key] = value
            return filtered_objects

    def new(self, obj):
        """
        Adds new object to storage dictionary
        """
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """
        Saves storage dictionary to file
        """
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            temp = {}
            for key, val in FileStorage.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """
        Loads storage dictionary from file
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity, 'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """
        Call reload() method for deserializing the JSON file to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieve one object based on the class and its ID
        """
        if cls and id:
            key = "{}.{}".format(cls.__name__, id)
            return self.__objects.get(key, None)
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage matching the given class
        """
        if cls:
            return len(self.all(cls))
        return len(self.__objects)

