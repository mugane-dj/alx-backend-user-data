#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import TypeVar, List


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth"""
        return False, path, excluded_paths

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user"""
        return None
