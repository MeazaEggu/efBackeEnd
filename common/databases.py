from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
class Connections:
    def __init__(self):
        self.DATABASE_CONNECTION_STRING='sqlite:///pss-ej-traker.db'
    def get_connection(self):
        engine = create_engine(self.DATABASE_CONNECTION_STRING, echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
