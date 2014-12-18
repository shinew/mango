from sqlalchemy import Column, Integer, String
from setup import Base

class User(Base):
    """ Table of basic user information """

    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    passwordHash = Column("PasswordHash", String(150), nullable=False)
    passwordSalt = Column("PasswordSalt", String(50), nullable=False)

