import hashlib
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Unicode, DateTime

from meta import Base

class Tweet(Base):
    
    __tablename__ = 'tweets'
    
    id = Column(Integer, primary_key=True)
    text = Column(Unicode, nullable=False)
    when = Column(DateTime, nullable=False, index=True)
    md5 = Column(Unicode, nullable=False, index=True, unique=True)
    
    def __init__(self, text, when):
        self.text = text
        self.when = when
        h = hashlib.new('md5')
        h.update(text.encode('ascii', 'ignore'))
        self.md5 = h.hexdigest()
