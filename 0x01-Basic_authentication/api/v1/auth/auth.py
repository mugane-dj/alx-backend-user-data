#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import TypeVar, List


class Auth:
    """Auth class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith("/"):
            path += "/"

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user"""
        return None
