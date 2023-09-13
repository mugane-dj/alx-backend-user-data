#!/usr/bin/env python3
"""
Password hashing module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns the salted hash of the input password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Creates a user in the db"""
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError("User {} already exists".format(email))
        self._db.add_user(
            email=email, hashed_password=_hash_password(password)
        )

    def valid_login(self, email: str, password: str) -> bool:
        """Check email and password to corresponding user records"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password=password.encode("utf-8"),
                hashed_password=user.hashed_password,
            )
        except NoResultFound:
            return False
