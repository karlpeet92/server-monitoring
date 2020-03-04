
from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.orm import relationship, deferred
from .base_model import Base, BaseModel
from .user_site import UserSite
from .site import Site


class User(BaseModel, Base):
    __tablename__ = 'user'
    __forbidden_fields__ = BaseModel.__forbidden_fields__
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(100))
    password = Column(String(255))
    phone_number = Column(Integer)
    user_sites = relationship("UserSite")




