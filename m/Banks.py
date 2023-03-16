#from flask_sqlalchemy import SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import create_engine
engine = create_engine('sqlite:///pss-ej-traker.db', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

"""class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), unique=True, nullable=False)
    atms = relationship("ATMs",back_populates="banks")
    def __repr__(self):
        return '<Bank %r>' % self.name"""
#from model.ATMs import *
class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer(), primary_key=True)
    name=Column(String(30), unique=True, nullable=False)
    atm = relationship("ATMs")
    #atms = relationship("ATMs",backref="player")#,back_populates="banks")
    #users = relationship("Users",backref="player")#, back_populates="banks")
    def __repr__(self):
        return '<Banks %r >' % self.name+" "+str(self.id)

Base.metadata.create_all(engine)


