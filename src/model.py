import os

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, DateTime, JSON, Text, Boolean
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
    ip = Column(String)
    create_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<W.N.S {self.email} - {self.type}>"

    def jsonlize(self, level=0):
        if level == 0:
            return {
                "id": self.id,
                "email": self.email,
                "type": self.type,
                "ip": self.ip,
                "create_at": GMT(self.create_at),
            }

        else:
            return {}


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    login_id = Column(String, unique=True)
    password = Column(String)
    google_auth = Column(String, nullable=True)
    facebook_auth = Column(String, nullable=True)
    email = Column(String)
    nickname = Column(String)
    realname = Column(String, nullable=True)
    create_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Account {self.id}, {self.login_id}, {self.email}, {self.nickname}>"

    @classmethod
    def new_from_data(cls, data):
        new_account = Account()

        for c in cls.__table__.columns:
            nullable = (c.default is not None) or c.nullable or c.primary_key

            if c.name not in data:
                if not nullable:
                    return None
            else:
                setattr(new_account, c.name, data[c.name])

        return new_account


class AdminRole(Base):
    __tablename__ = "admin_role"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey(Account.id))
    permission = Column(JSON, default={})
    note = Column(Text, default="")
    disabled = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.now)

# class ForumPost(Base):
#     __tablename__ = "forum_post"

#     id = Column(Integer, primary_key=True)
