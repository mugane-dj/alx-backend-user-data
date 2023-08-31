#!/usr/bin/env python3
"""Password hashing using bcrypt package"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password"""
    return bcrypt.hashpw(password)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if password matches the hashed_password provided"""
    if bcrypt.hashpw(password) == hashed_password:
        return True
    return False
