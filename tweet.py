import hashlib
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Unicode, DateTime

from meta import Base

class Tweet(Base):
    
    __tablename__ = 'tweets'
    
    id = Column(Integer, primary_key=True)
    text = Column(Unicode, nullable=False)
    md5 = Column(Unicode, nullable=False, unique=True)
    
    def __init__(self, text):
        self.text = text
        h = hashlib.new('md5')
        h.update(text.encode('ascii', 'ignore'))
        self.md5 = h.hexdigest()
