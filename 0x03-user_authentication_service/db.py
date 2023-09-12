#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar("User"):
        """Add user to DB"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    # def find_user_by(self, **kwargs) -> TypeVar("User"):
    #     """Find user in DB"""
    #     session = self._session
    #     user = session.query(User).filter_by(**kwargs).first()
    #     if not user:
    #         raise NoResultFound
    #     return user

    # def update_user(self, user_id: int, **kwargs) -> None:
    #     """Update a user instance"""
    #     user = self.find_user_by(id=user_id)
    #     session = self._session
    #     for k, v in kwargs.items():
    #         if k not in dir(User):
    #             raise ValueError
    #         setattr(user, k, v)
    #     session.commit()
