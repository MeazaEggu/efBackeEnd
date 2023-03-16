from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
#from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from model.Parent import Parent
class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    #parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent")

Base.metadata.create_all(engine)




"""from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#engine = create_engine('sqlite:///db/test.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
chiled = Parent(
    id=None,
            )
chiled = Child(
    id=None,
    parent=None
            )
session.add(chiled)
session.commit()"""