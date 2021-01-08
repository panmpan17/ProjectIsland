import os

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer, DateTime, JSON, Text, Boolean,\
    BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta


Base = declarative_base()


def FormatDatetime(t):
    return t.timestamp()


class WebsiteNewsSubscription(Base):
    __tablename__ = "website_news_subscription"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    type = Column(Integer)
    ip = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<W.N.S {self.email} - {self.type}>"

    def jsonlize(self, level=0):
        if level == 0:
            return {
                "id": self.id,
                "email": self.email,
                "type": self.type,
                "ip": self.ip,
                "create_at": FormatDatetime(self.create_at),
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
    create_at = Column(DateTime, default=datetime.utcnow)

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

    def __repr__(self):
        return f"<Account {self.id}, {self.login_id}, {self.email}, {self.nickname}>"
    
    def jsonlize(self, level=0):
        if level == 0:
            return {
                "id": self.id,
                "nickname": self.nickname,
            }

        elif level == 1:
            return {
                "id": self.id,
                "login_id": self.login_id,
                "google_auth": self.google_auth,
                "facebook_auth": self.facebook_auth,
                "email": self.email,
                "nickname": self.nickname,
                "realname": self.realname,
                "create_at": FormatDatetime(self.create_at),
            }

        else:
            return {}


class AdminRole(Base):
    __tablename__ = "admin_role"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey(Account.id))
    permission = Column(JSON, default={})
    note = Column(Text, default="")
    disabled = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.utcnow)


class ForumPost(Base):
    __tablename__ = "forum_post"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    cover_img = Column(String, nullable=True)
    topic = Column(Integer, nullable=True)
    author_account_id = Column(Integer, ForeignKey(Account.id),
                               nullable=False)
    views_count = Column(BigInteger, default=0)
    status = Column(Integer, default=0)
    create_at = Column(DateTime, default=datetime.utcnow)

    author = relationship(Account)

    def __repr__(self):
        return f"<ForumPost {self.id}, {self.title}, {self.topic}, {self.author_account_id}>"

    def jsonlize(self, level=0):
        if level == 0:
            return {
                "id": self.id,
                "title": self.title,
                "content": self.content,
                "cover_img": self.cover_img,
                "topic": self.topic,
                "author": self.author.jsonlize(),
                "views_count": self.views_count,
                "create_at": FormatDatetime(self.create_at),
            }

        else:
            return {}


class ForumReply(Base):
    __tablename__ = "forum_reply"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    author_account_id = Column(Integer, ForeignKey(Account.id),
                               nullable=False)
    post_id = Column(Integer, ForeignKey(ForumPost.id),
                     nullable=False)
    status = Column(Integer, default=0)
    create_at = Column(DateTime, default=datetime.utcnow)

    author = relationship(Account)
    post = relationship(ForumPost)

    def __repr__(self):
        return f"<ForumPost {self.id}, {self.content}>"

    def jsonlize(self, level=0):
        if level == 0:
            return {
                "id": self.id,
                "content": self.content,
                "author": self.author.jsonlize(),
                "create_at": FormatDatetime(self.create_at),
            }

        else:
            return {}
