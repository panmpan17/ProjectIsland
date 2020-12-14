import os

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta


Base = declarative_base()


class WebsiteNewsSubscription(Base):
    __tablename__ = "website_news_subscription"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    type = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<W.N.S {self.email} - {self.type}>"
