from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db', echo=False)

Session = scoped_session(sessionmaker())
Session.configure(bind=engine)

Base = declarative_base()
