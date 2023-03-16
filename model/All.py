from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from common.databases import Connections
connection=Connections()
engine = create_engine(connection.DATABASE_CONNECTION_STRING, echo=False)
Base = declarative_base()
import datetime
from passlib.hash import sha256_crypt

class Banks(Base):
    __tablename__ = 'banks'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), unique=True, nullable=False)
    active_status= Column(Integer, default=0)
    delete_status= Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user = relationship("Users", back_populates="bank")
    atm = relationship("ATMs", back_populates="bank")
    atmdispute = relationship("ATMDisputes",foreign_keys='ATMDisputes.bank_id', back_populates="bank")
    atmdisputedispute = relationship("ATMDisputes",foreign_keys='ATMDisputes.bank_id_dispute', back_populates="bankdispute")

    def isActive(self):
        if self.active_status==0 or self.active_status==None:
            return True
        else:
            return False
    def isDeleted(self):
        if self.delete_status==0 or self.delete_status==None:
            return True
        else:
            return False

    def __repr__(self):
        return '<Banks %r >' % self.name+" "+str(self.id)

class ATMs(Base):
    __tablename__ = 'atms'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), unique=False, nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'))
    active_status= Column(Integer, default=0)
    delete_status= Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    bank = relationship("Banks", back_populates="atm")
    atmdisputeamt = relationship("ATMDisputes", back_populates="atm")
    def isActive(self):
        if self.active_status==0 or self.active_status==None:
            return True
        else:
            return False
    def isDeleted(self):
        if self.delete_status==0 or self.delete_status==None:
            return True
        else:
            return False
    def __repr__(self):
        return '<ATM %r>' % self.name

class Privilages(Base):
    __tablename__ = 'privilages'
    id = Column(Integer, primary_key=True)
    name=Column(String(30), nullable=False)
    rolename=Column(String(30),nullable=False)
    usertype=Column(String(30), nullable=False)
    user = relationship("Users",back_populates="privilage")
    active_status= Column(Integer, default=0)
    delete_status= Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def toString(self):
        return {self.id,self.name,self.rolename,self.usertype}
    def isActive(self):
        if self.active_status==0 or self.active_status==None:
            return True
        else:
            return False
    def isDeleted(self):
        if self.delete_status==0 or self.delete_status==None:
            return True
        else:
            return False
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
    bank_id = Column(Integer, ForeignKey('banks.id'),nullable=False)
    bank = relationship("Banks", back_populates="user")
    privilage_id = Column(Integer, ForeignKey('privilages.id'), nullable=False)
    privilage=relationship("Privilages", back_populates="user")
    active_status= Column(Integer, default=0)
    delete_status= Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    atmdispute = relationship("ATMDisputes",foreign_keys='ATMDisputes.user_id', back_populates="user")
    atmdisputeconfirmuser = relationship("ATMDisputes", foreign_keys='ATMDisputes.user_id_confirm_dispute', back_populates="userconfirmatmdispute")

    def toString(self):
        return {self.id,self.firstname,self.middlename,self.lastname,self.username,self.privilage,
                self.bank_id,self.email}
    def isActive(self):
        if self.active_status==0 or self.active_status==None:
            return True
        else:
            return False
    def isDeleted(self):
        if self.delete_status==0 or self.delete_status==None:
            return True
        else:
            return False
    def __repr__(self):
        return '<User %r>' % self.username


class ATMDisputes(Base):
    __tablename__ = 'atmdisputes'
    id = Column(Integer, primary_key=True)
    amount=Column(Float)
    off_us=Column(Boolean)
    on_us=Column(Boolean)
    card_number=Column(String)
    customer_name=Column(String)
    #who save dispute
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("Users", uselist = False, back_populates="atmdispute",foreign_keys=[user_id])

    #Which customer bank , where atm dispute registered
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    bank = relationship("Banks", uselist = False, back_populates="atmdispute", foreign_keys=[bank_id])

    # whic bank make dispute
    bank_id_dispute = Column(Integer, ForeignKey('banks.id'), nullable=True)
    bankdispute = relationship("Banks", uselist = False, back_populates="atmdisputedispute", foreign_keys=[bank_id_dispute])

    #WHich atm make cdispute
    atm_id = Column(Integer, ForeignKey('atms.id'), nullable=True)
    atm = relationship("ATMs", back_populates="atmdisputeamt")
    bank_name=Column(String)
    atm_name = Column(String)
    bank_name_dispute = Column(String)

    #

    #At what time error happend
    dispute_at = Column(DateTime)

    active_status = Column(Integer, default=0)
    delete_status = Column(Integer, default=1)
    confirm_status = Column(Boolean, default=False)
    #A user who confirm this dispute
    user_id_confirm_dispute = Column(Integer, ForeignKey('users.id'), nullable=True,default=None)
    userconfirmatmdispute = relationship("Users", uselist = False, back_populates="atmdisputeconfirmuser", foreign_keys=[user_id_confirm_dispute])
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

def startSchemaBuilder(Base=Base):
    engine.echo = True
    Base.metadata.create_all(engine)
def startInsertingDefaultData(Base=Base):
    print('-----------------------------------------------------------------------')
    print("Create tables")
    engine.echo = True
    #Base.metadata.create_all(engine)
    print("All tables are created")
    print('-----------------------------------------------------------------------')

    print('-----------------------------------------------------------------------')
    print("Insert startup data")
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    db_session = session

    privilage=Privilages()
    privilage.name="adminpss"
    privilage.rolename = "admin"
    privilage.usertype = "pss"
    db_session.add(privilage)
    db_session.commit()

    bank=Banks()
    bank.name="pss"
    db_session.add(bank)
    db_session.commit()

    user=Users()
    user.firstname="test"
    user.middlename="test"
    user.lastname="test"
    user.username = "pss"
    user.password=sha256_crypt.encrypt("1234")
    user.email = "test@mail.com"
    user.bank_id = bank.id
    user.privilage_id = privilage.id
    db_session.add(user)
    db_session.commit()
    #print(db_session.query(Users).filter_by(username="pss").first())
    privilage = Privilages()
    privilage.name = "normalpss"
    privilage.rolename = "normal"
    privilage.usertype = "pss"
    db_session.add(privilage)
    db_session.commit()

    privilage = Privilages()
    privilage.name = "adminbank"
    privilage.rolename = "admin"
    privilage.usertype = "bank"
    db_session.add(privilage)
    db_session.commit()

    privilage = Privilages()
    privilage.name = "normalbank"
    privilage.rolename = "normal"
    privilage.usertype = "bank"
    db_session.add(privilage)
    db_session.commit()


    del(db_session)
    del(Base)
    print("Startup data inserted")
    print('-----------------------------------------------------------------------')