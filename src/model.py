import os

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta


Base = declarative_base()


def GMT(t, format_="%Y/%m/%d %H:%M:%S"):
    try:
        t += timedelta(hours=8)
        return t.strftime(format_)
    except Exception:
        return None


class WebsiteNewsSubscription(Base):
    __tablename__ = "website_news_subscription"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    type = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<W.N.S {self.email} - {self.type}>"

    def jsonlize(self, level=0):
        if level == 0:
            return {
                "id": self.id,
                "email": self.email,
                "type": self.type,
                "create_at": GMT(self.create_at),
            }

        else:
            return {}
