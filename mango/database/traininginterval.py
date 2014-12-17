from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime, Boolean
from setup import Base

class TrainingInterval(Base):
    """ Table of training data for machine learning"""

    __tablename__ = "TrainingInterval"

    logTime = Column("LogTime", DateTime, nullable=False)
    id = Column(Integer, primary_key=True)
    userID = Column("UserID", Integer, nullable=False)
    startTime = Column("StartTime", DateTime, nullable=False)
    endTime = Column("EndTime", DateTime, nullable=False)
    category = Column("Category", Integer, nullable=False)
    isDefaultSet = Column("IsDefaultSet", Boolean, nullable=False)
    featureCache = Column("FeatureCache", String(5000), nullable=True)
    featureCacheVersion = Column("FeatureCacheVersion", Integer, nullable=True)

    def __repr__(self):
        return "<TrainingInterval(UserID='%s', StartTime='%s', EndTime='%s', Category='%s', IsDefaultSet='%s', FeatureCache='%s', FeatureCacheVersion='%s')>" % \
            (self.userID, self.startTime, self.endTime, self.category, self.isDefaultSet, self.featureCache, self.featureCacheVersion)
