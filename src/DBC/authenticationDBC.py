import os
import mysql.connector
import uuid
import base64


class AuthenticationDBC:
    __instance = None

    @staticmethod
    def get_instance():
        if AuthenticationDBC.__instance is None:
            AuthenticationDBC()
        return AuthenticationDBC.__instance

    def __init__(self):
        if AuthenticationDBC.__instance is None:
            AuthenticationDBC.__instance = self
        else:
            raise Exception("Trying to call init on a singleton. Use get_instance() instead")

        host = os.environ.get("JAWSDB_MARIA_HOST", "localhost")
        database = os.environ.get("JAWSDB_MARIA_DATABASE", "recipemanager")
        user = os.environ.get("JAWSDB_MARIA_USER", "rm")
        password = os.environ.get("JAWSDB_MARIA_PASSWORD", "rmpassword")

        self.connection = mysql.connector.connect(host=host,
                                                  database=database,
                                                  user=user,
                                                  password=password)

    @staticmethod
    def parse_basic_auth(base64str):
        """Returns username, password"""
        auth_type = base64str.split(" ")[0]
        decoded_userpass = base64.b64decode(base64str.split(" ")[1]).decode("utf-8")

        username = decoded_userpass.split(":")[0]
        password = decoded_userpass.split(":")[1]
        return username, password

    def register(self, username, password_hash, role):
        """Returns true if successful registration."""
        c = self.connection.cursor()
        c.execute("SELECT UserID FROM users WHERE users.UserName=%s",
                  (username,))
        c.fetchall()
        if c.rowcount == 1:
            return False, "Username exists"

        c.execute("INSERT INTO Users (UserName, PasswordHash, Role) VALUES (%s, %s, %s)",
                  (username, password_hash, role,))
        self.connection.commit()
        c.close()
        return True, "Registration success"

    def login(self, username, password_hash):
        """Returns session id if successful login, None otherwise."""
        c = self.connection.cursor()
        print(username, password_hash)
        c.execute("SELECT UserID FROM users WHERE users.UserName=%s AND users.PasswordHash=%s",
                  (username, password_hash,))
        user_id = (c.fetchone() or [None])[0]
        if c.rowcount == 0:
            c.close()
            return None
        session_id = uuid.UUID(bytes=os.urandom(16)).hex
        c.execute("""
                  DELETE FROM Sessions 
                  WHERE UserID = %s AND 
                  LastAccessedDT + INTERVAL ExpirationMinutes MINUTE < NOW()""",
                  (user_id,))

        c.execute("INSERT INTO Sessions (SessionID, UserID) VALUES (%s, %s)", (session_id, user_id,))
        self.connection.commit()
        c.close()
        return session_id

    def validate(self, session_id):
        """Returns user_id, role if session id is valid (expiration) and refreshes session id. None otherwise"""
        c = self.connection.cursor()
        c.execute("""
                    SELECT Users.UserID, Users.Role FROM Users 
                    INNER JOIN Sessions ON Sessions.UserID = Users.UserID 
                    WHERE Sessions.SessionID = %s""",
                  (session_id,))
        row = c.fetchone()
        self.connection.commit()
        c.close()

        if row is None:
            return None, None
        else:
            return row[0], row[1]

