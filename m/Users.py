#from flask_sqlalchemy import SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
engine = create_engine('sqlite:///pss-ej-traker.db', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

import datetime
from passlib.hash import sha256_crypt

from model.Banks import *
from model.All import *
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    firstname = Column(String(30), nullable=False)
    middlename = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    bank_id = Column(Integer(), ForeignKey('banks.id'), nullable=True)
    bank = relationship("Banks", back_populates="users")
    privilage_id = Column(Integer(), ForeignKey('privilages.id'), nullable=False)
    privilage = relationship("Privilages", back_populates="users")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def toString(self):
        return {self.id,self.firstname,self.middlename,self.lastname,self.username,self.role,
                self.bank_id,self.email}

    def __repr__(self):
        return '<User %r>' % self.username
Base.metadata.create_all(engine)











#Base.metadata.create_all(engine)
"""

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#engine = create_engine('sqlite:///db/database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
user = Users(username="eyasu",
             password=sha256_crypt.encrypt("1234"),
             email="e@gm.com",
             bank="awash",
            )
session.add(user)
session.commit()

"""