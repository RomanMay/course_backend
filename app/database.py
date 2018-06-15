from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'postgres://tjlifzjdwsmoqh:068c8662fe033be9c78b98aae83c38c8a9aa17182458e09243a04d59c2745693@ec2-54-235-109-37.compute-1.amazonaws.com:5432/d8a6vl1bqbg0qk',
    convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
