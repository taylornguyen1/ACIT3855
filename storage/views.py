from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class VideoViews(Base):
    """ Blood Pressure """

    __tablename__ = "views"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    views = Column(Integer, nullable=False)

    def __init__(self, user_id, timestamp, views):
        """ Initializes a blood pressure reading """
        self.user_id = user_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.views = views

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['views'] = self.views
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
