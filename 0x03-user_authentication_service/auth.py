#!/usr/bin/env python3
"""
Password hashing module
"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Creates a user in the db"""
        user_mapping = {"email": email}
        existing_user = self._db.find_user_by(**user_mapping)
        if existing_user:
            raise ValueError("User {} already exists".format(email))
        self._db.add_user(
            email=email, hashed_password=_hash_password(password)
        )


def _hash_password(password: str) -> bytes:
    """Returns the salted hash of the input password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
