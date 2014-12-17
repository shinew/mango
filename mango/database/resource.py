from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.types import DateTime, BigInteger
from setup import Base

class Resource (Base):
    """ Table of heart rate data """

    __tablename__ = "Resource" 

    logTime = Column("LogTime", DateTime, nullable=False)
    id = Column(BigInteger, primary_key=True)
    userID = Column("UserID", Integer, nullable=False) # "should" have a ForeignKey reference to User.ID, but no cascades
    time = Column("Time", DateTime, nullable=False)
    type = Column("Type", String(10), nullable=False)
    value = Column("Value", Integer, nullable=False)

    def __repr__(self):
        return "<Resource(UserID='%s', time='%s', type='%s', value='%s'>" % \
            (self.userID, self.time, self.type, self.value)

