from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.types import DateTime, BigInteger
from setup import Base

class HeartRate(Base):
    """ Table of heart rate data """

    __tablename__ = "HeartRate" 

    logTime = Column("LogTime", DateTime, nullable=False)
    id = Column(BigInteger, primary_key=True)
    userID = Column("UserID", Integer, nullable=False) # "should" have a ForeignKey reference to User.ID, but no cascades
    device = Column("Device", String(255), nullable=False)
    time = Column("Time", DateTime, nullable=False)
    hasMovement = Column("HasMovement", Boolean, nullable=False)
    hr = Column("HR", Integer)
    hrv = Column("HRV", Integer)

    def __repr__(self):
        return "<HeartRate(UserID='%s', Device='%s', Time='%s', HasMovement='%s', HR='%s', HRV='%s'>" % \
            (self.userID, self.device, self.time, self.hasMovement, self.hr, self.hrv)
