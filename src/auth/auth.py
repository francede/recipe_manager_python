import jwt
import hashlib
import base64


class Auth:
    @staticmethod
    def register(username, password):
        """Returns true if successful registration."""
        pass

    @staticmethod
    def login(username, password):
        """Returns jwt token if successful login, None otherwise"""
        pass

    @staticmethod
    def validate(token):
        """Returns true if token is valid (expiration and signature)."""

    @staticmethod
    def renew(token):
        """Returns renewed token if valid token as parameter."""
