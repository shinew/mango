from sqlalchemy import Column, Integer, String, func
from setup import Base

class User(Base):
    """ Table of basic user information """

    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    userName = Column("UserName", String(255), nullable=False)
    passwordHash = Column("PasswordHash", String(150), nullable=False)
    passwordSalt = Column("PasswordSalt", String(50), nullable=False)

    def __repr__(self):
        return "<User(ID='%s', UserName='%s')>" % (self.id, self.userName)

