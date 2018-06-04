from database import Base
from sqlalchemy import String, Integer, Column, Float, JSON


class User(Base):
    __tablename__ = 'user'

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    role = Column(String, default="user")
    email = Column(String, unique=True)
    password = Column(String)


class Offer(Base):
    __tablename__ = 'offer'

    def __init__(self, name, cost, description):
        self.name = name
        self.cost = cost
        self.description = description

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    cost = Column(Float)
    description = Column(JSON)


class Order(Base):
    __tablename__ = 'order'

    def __init__(self, user_id, offer_id, status):
        self.status = status
        self.user_id = user_id
        self.offer_id = offer_id

    id = Column(Integer, primary_key=True)
    status = Column(String)
    user_id = Column(Integer)
    offer_id = Column(Integer)
