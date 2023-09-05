#!/usr/bin/env python3
"""
An implementation of basic authentication
"""
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Class BasicAuth"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extract the Base64 part of the Authorization header for a Basic
        Authentication
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None

        return authorization_header.split(" ")[-1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes the Base64 string `base64_authorization_header`
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode("utf-8")
        except ValueError:
            return None

        return decoded_str

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extract user email and password from the Base64 decoded value.
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or decoded_base64_authorization_header.find(":") == -1
        ):
            return None, None
        email = decoded_base64_authorization_header.split(":")[0]
        password = decoded_base64_authorization_header.split(":")[-1]
        return email, password
