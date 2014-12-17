from sqlalchemy import Column, Integer
from sqlalchemy.types import DateTime, BigInteger
from setup import Base

class IntervalScore(Base):
    """ Table of interval data """

    __tablename__ = "IntervalScore"

    logTime = Column("LogTime", DateTime, nullable=False)
    id = Column(BigInteger, primary_key=True)
    userID = Column("UserID", Integer, nullable=False) # "should" have a ForeignKey reference to User.ID, but no cascades
    startTime = Column("StartTime", DateTime, nullable=False)
    endTime = Column("EndTime", DateTime, nullable=False)
    score = Column("Score", Integer, nullable=False)

    def __repr__(self):
        return "<IntervalScore(UserID='%s', StartTime='%s', EndTime='%s', Score='%s')>" % \
            (self.userID, self.startTime, self.endTime, self.score)
