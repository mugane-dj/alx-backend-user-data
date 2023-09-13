#!/usr/bin/env python3
"""
Password hashing module
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Returns the salted hash of the input password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate UUID string"""
    return str(uuid.uuid4)


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Creates a user in the db"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Check email and password to corresponding user records"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode("utf-8"), user.hashed_password
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session id for an existing user"""
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None
