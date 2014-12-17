from hashlib import sha512
from uuid import uuid4
from database import User

class Authenticator:
    def __init__(self, logger):
        self.logger = logger

    def hashPassword(self, password):
        # returns (salt, hashed password)
        salt = uuid4().hex
        hash = sha512(password + salt).hexdigest()
        return salt, hash

    def verifyUser(self, userName, password, session): 
        # Returns the userID if authentication was successful. Else return None.
        thisUser = session.query(User).filter(User.userName == userName).first()
        if thisUser is None:
            return None
        if sha512(password + thisUser.passwordSalt).hexdigest() == thisUser.passwordHash:
            return thisUser.id
        else:
            return None

    def authenticate(self, id, password, session):
        thisUser = session.query(User).filter(User.id == id).first()
        if thisUser is None:
            return False
        if sha512(password + thisUser.passwordSalt).hexdigest() == thisUser.passwordHash:
            return True
        else:
            return False

