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


#import model.Banks
from model.All import *
class ATMs(Base):
    __tablename__ = 'atms'
    id = Column(Integer(), primary_key=True)
    name=Column(String(30), unique=True, nullable=False)
    #bank_id = Column(Integer, ForeignKey('banks.id'))
    #bank=relationship("Banks",backref="player")#,back_populates="atms")
    bank_id = Column(Integer(), ForeignKey('banks.id'))
    def __repr__(self):
        return '<ATM %r>' % self.name

Base.metadata.create_all(engine)