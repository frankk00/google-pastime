from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Unicode, DateTime

from meta import Base

class Page(Base):
    
    __tablename__ = 'pages'
    
    id = Column(Integer, primary_key=True)
    url = Column(Unicode, nullable=False)
    html = Column(Unicode, nullable=False)
    numresults = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    olderurl = Column(Unicode, nullable=False)
    newerurl = Column(Unicode, nullable=False)
    hit = Column(DateTime, nullable=False)
    
    def __init__(self, url, html, numresults, olderurl, newerurl):
        self.url = url
        self.html = html
        self.numresults = numresults
        self.olderurl = olderurl
        self.newerurl = newerurl
        self.hit = datetime.now()
