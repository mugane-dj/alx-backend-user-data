#!/usr/bin/env python3
"""
Password hashing module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns the salted hash of the input password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
