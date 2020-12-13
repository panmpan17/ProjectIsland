import os

# import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from contextlib import contextmanager


Base = declarative_base()


@contextmanager
def session_scope():
    session = DatabaseManager.Session()

    try:
        yield session
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        session.close()


class DatabaseManager:
    db_string = None
    engine = None
    Session = None

    @classmethod
    def to_sqlite(cls, location=None):
        if cls.engine is not None:
            raise "Database is already started"

        if location is None:
            cls.db_string = "sqlite:///:memory:"
        else:
            cls.db_string = "sqlite:///" + location

    @classmethod
    def connect_database(cls):
        if cls.db_string is None:
            raise "Database string is not define"

        cls.engine = create_engine(cls.db_string)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
    
    @classmethod
    def dispose_engine(cls):
        if cls.engine is None:
            cls.engine.dispose()
            self.engine = None


class WebsiteNewsSubscription(Base):
    __tablename__ = "website_news_subscription"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    type = Column(Integer)
    create_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<W.N.S {self.email} - {self.type}>"


if __name__ == "__main__":
    DatabaseManager.to_sqlite("test.db")
    DatabaseManager.connect_database()

    with session_scope() as session:
        user_a = WebsiteNewsSubscription(
            email="panmpan@gmail.com",
            type=0)
        session.add(user_a)

    DatabaseManager.dispose_engine()

