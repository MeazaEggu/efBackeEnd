from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from common.databases import Connections
import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///pss-ej-traker.db', echo=True)
Base = declarative_base()

"""class Privilages(Base):
    __tablename__ = 'privilages'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), nullable=False)
    rolename=Column(String(30),nullable=False)
    usertype=Column(String(30), nullable=False)
    #privilage = relationship("Privilages")
    user = relationship("Users", back_populates="privilages")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def toString(self):
        return {self.id,self.name,self.rolename,self.usertype}

    def __repr__(self):
        return '<Privilages %r>' % self.name"""
"""def start():
    Base.metadata.create_all(Connections().getEngin())"""


class Privilages(Base):
    __tablename__ = 'privilages'
    id = Column(Integer(), primary_key=True)
    name = Column(String(30), nullable=False)
    rolename = Column(String(30), nullable=False)
    usertype = Column(String(30), nullable=False)
    user = relationship("Users")#, back_populates="privilages")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def toString(self):
        return {self.id,self.name,self.rolename,self.usertype}

    def __repr__(self):
        return '<Privilages %r>' % self.name

Base.metadata.create_all(engine)