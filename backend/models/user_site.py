from sqlalchemy import Column, Integer, String, Enum, JSON, ForeignKey, create_engine
from sqlalchemy.orm import relationship, deferred, sessionmaker
from .base_model import Base, BaseModel



class UserSite(BaseModel, Base):
    __tablename__ = 'user_site'
    __forbidden_fields__ = BaseModel.__forbidden_fields__
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    site_id = Column(Integer, ForeignKey("site.id"))
    site = relationship("Site")

    
