"""
Contains class BaseModel from which all other instances will inherit from.
The BaseModel class from which all model classes will be derived
"""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlalchemy.inspection import inspect
from typing import Any

from api.v1 import db
import models

import uuid

time = "%Y-%m-%dT%H:%M:%S"


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(String(60), primary_key=True, index=True,
                default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.now(timezone.utc)
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now(timezone.utc)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now(timezone.utc)
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.now(timezone.utc)
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_fs=None, include_relationships=False, seen=None,
                exclude_none=True):
        """Serialises SQLAlchemy objects to dict().

            Args:
                save_fs (bool, optional): A flag indicating whether sensitive
                                          data should be included in the
                                          dictionary representation. If False,
                                          sensitive data such as passwords will
                                          be excluded.
                                          Defaults to None.
                include_relationships (bool, optional): Whether to include
                                                        model relationships in
                                                        the dictionary
                                                        representation.
                                                        Defaults to False.
                seen (set, optional): A set of seen objects to avoid
                                       recursion, when
                                       include_relationships=True.
                                       Defaults to None
                                       -----------------------------------
                                       NEVER CHANGE THE VALUE TO TRUE!!!!!
                                       -----------------------------------
                exclude_none (bool, optional): Determines whether to exclude
                                               keys with None values from the
                                               dictionary representation.
                                               Defaults to True.
            Returns:
                dict: a dictionary containing all keys/values of the instance.
        """
        if seen is None:
            seen = set()

        if self in seen:
            """Return a minimal representation to break recursion"""
            return {'id': self.id}

        seen.add(self)

        columns = {c.key: getattr(self, c.key) for c in
                   inspect(self).mapper.column_attrs}
        if "created_at" in columns and isinstance(columns["created_at"],
                                                  datetime):
            columns["created_at"] = columns["created_at"].strftime(time)
        if "updated_at" in columns and isinstance(columns["updated_at"],
                                                  datetime):
            columns["updated_at"] = columns["updated_at"].strftime(time)
        columns["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in columns:
            del columns["_sa_instance_state"]
        if save_fs is None:
            if "password_hash" in columns:
                del columns["password_hash"]

        if include_relationships:
            ir = include_relationships
            for relationship in inspect(self).mapper.relationships:
                related_value = getattr(self, relationship.key)
                if related_value is not None:
                    if relationship.uselist:
                        columns[relationship.key] = [
                                item.to_dict(
                                             save_fs=save_fs,
                                             include_relationships=ir,
                                             seen=seen
                                         ) for item in related_value]
                    else:
                        columns[relationship.key] = \
                                related_value.to_dict(save_fs=save_fs,
                                                      include_relationships=ir,
                                                      seen=seen)

        if exclude_none:
            columns = {key: value for key, value in columns.items() if value is
                       not None and not (isinstance(value, list) and
                                         len(value) == 0)}
        return columns

    def delete(self):
        """Deletes the current instance from the storage"""
        models.storage.delete(self)

    def update(self, attr: dict[str, Any]) -> bool:
        """
        Updates an existing attribute of an object in the database.

        Args:
            attr: A dictionary containing the attribute name as the key
                and the new value as the value.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            ValueError: If obj is not a valid model instance.
            KeyError: If the attribute specified does not exist in the object.
        """
        from models.engine.db_storage import classes

        if (
            self is None
            or not hasattr(self, 'id')
            or self.__class__.__name__ not in classes
        ):
            raise ValueError("The provided object is not valid.")

        if not isinstance(attr, dict):
            raise ValueError("The 'attr' parameter must be a dictionary.")

        for key, value in attr.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise KeyError(f"{self.__class__.__name} has no attribute '{key}'")

        try:
            self.save()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating object: {e}")
            return False
