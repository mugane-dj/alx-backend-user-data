#!/usr/bin/env python3
"""
An implementation of session authentication
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Class SessionAuth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
