from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    #children = relationship("Child", back_populates="parent")
