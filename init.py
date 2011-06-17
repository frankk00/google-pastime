import page
import tweet
from meta import Base
from sqlalchemy import create_engine

from meta import engine
metadata = Base.metadata
metadata.create_all(engine)
