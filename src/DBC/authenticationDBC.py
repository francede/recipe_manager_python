import os
import mysql.connector


class AuthenticationDBC:
    def __init__(self):
        host = os.environ.get("JAWSDB_MARIA_HOST", "localhost")
        database = os.environ.get("JAWSDB_MARIA_DATABASE", "recipemanager")
        user = os.environ.get("JAWSDB_MARIA_USER", "rm")
        password = os.environ.get("JAWSDB_MARIA_PASSWORD", "rmpassword")

        self.connection = mysql.connector.connect(host=host,
                                                  database=database,
                                                  user=user,
                                                  password=password)

    def register(self, username, password):
        """Returns true if successful registration."""
        pass

    def login(self, username, password):
        """Returns session id if successful login, None otherwise"""
        pass

    def validate(self, session_id):
        """Returns true if token is valid (expiration) and ."""

    def renew(self, session_id):
        """Returns renewed token if valid token as parameter."""
