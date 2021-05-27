from sqlalchemy import Column, Integer, String, Float, Enum, JSON
from sqlalchemy.orm import relationship, deferred
from .base_model import Base, BaseModel
from alembic import op


class Site(BaseModel, Base):
    __tablename__ = 'site'
    __forbidden_fields__ = BaseModel.__forbidden_fields__
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    url = Column(String(100))
    interval = Column(Integer)
    status_code = Column(Integer)
    response_time = Column(Float)
    user_sites = relationship("UserSite")
