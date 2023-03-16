"""from model import Users as user,Privilages as privilage
from model.* import Banks as bank, ATMs as atm"""
"""import model.Banks, model.Banks.s
import model.ATMs
import model.Privilages
import model.Users
from common.databases import Connections
Base=Connections().getBase()"""
"""from model.Users import Users
from model.Privilages import Privilages

from passlib.hash import sha256_crypt"""

"""bank.start()
atm.start()
privilage.start()
user.start()"""
"""print(Base.metadata.create_all(Connections().getEngin()))

db_session = Connections().get_connection()"""


"""privilage=Privilages()
privilage.name="adminpss"
privilage.rolename = "admin"
privilage.usertype = "pss"
db_session = Connections().get_connection()
db_session.add(privilage)
db_session.commit()"""
"""from model.Users import Users
user=Users()
user.firstname="test"
user.middlename="test"
user.lastname="test"
user.username = "pss"
user.password=sha256_crypt.encrypt("1234")
user.email = "test@mail.com"
user.bank_id = None
user.privilage_id = 1
db_session.add(user)
db_session.commit()"""




from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///pss-ej-traker.db', echo=True)
Base = declarative_base()
import datetime
from passlib.hash import sha256_crypt

class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    """
    #atm = relationship("ATMs")
    bank = relationship("Banks")  # , back_populates="users")"""
    user = relationship("Users", back_populates="bank")
    atm = relationship("ATMs", back_populates="bank")

    def __repr__(self):
        return '<Banks %r >' % self.name+" "+str(self.id)

class ATMs(Base):
    __tablename__ = 'atms'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), unique=False, nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    bank = relationship("Banks", back_populates="atm")

    def __repr__(self):
        return '<ATM %r>' % self.name

class Privilages(Base):
    __tablename__ = 'privilages'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), nullable=False)
    rolename=Column(String(30),nullable=False)
    usertype=Column(String(30), nullable=False)
    user = relationship("Users",back_populates="privilage")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def toString(self):
        return {self.id,self.name,self.rolename,self.usertype}

    def __repr__(self):
        return '<Privilages %r>' % self.name


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname=Column(String(30), nullable=False)
    middlename=Column(String(30),nullable=False)
    lastname=Column(String(30), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password=Column(String(200), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'),nullable=True)
    bank = relationship("Banks", back_populates="user")
    privilage_id = Column(Integer, ForeignKey('privilages.id'), nullable=False)
    privilage=relationship("Privilages", back_populates="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def toString(self):
        return {self.id,self.firstname,self.middlename,self.lastname,self.username,self.role,
                self.bank_id,self.email}

    def __repr__(self):
        return '<User %r>' % self.username

Base.metadata.create_all(engine)
"""from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
db_session = session
#from model.Privilages import Privilages
privilage=Privilages()
privilage.name="adminpss"
privilage.rolename = "admin"
privilage.usertype = "pss"
db_session.add(privilage)
db_session.commit()

#rom model.Users import Users
user=Users()
user.firstname="test"
user.middlename="test"
user.lastname="test"
user.username = "pss"
user.password=sha256_crypt.encrypt("1234")
user.email = "test@mail.com"
user.bank_id = None
user.privilage_id = privilage.id
db_session.add(user)
db_session.commit()
print(db_session.query(Users).filter_by(username="pss").first())
del(db_session)
del(Base)"""