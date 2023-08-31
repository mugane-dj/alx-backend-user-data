#!/usr/bin/env python3
"""Password hashing using bcrypt package"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if password matches the hashed_password provided"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
