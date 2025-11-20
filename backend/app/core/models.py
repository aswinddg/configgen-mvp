from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    
    vendor = relationship("Vendor")

class Param(Base):
    __tablename__ = "params"
    
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=False)
    key = Column(String, nullable=False)
    label = Column(String, nullable=False)
    type = Column(String, nullable=False)  # string, ip, int
    required = Column(Boolean, default=True)
    default_value = Column(String, default="")
    options = Column(String)