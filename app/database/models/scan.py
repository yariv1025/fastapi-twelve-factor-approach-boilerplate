from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ScanType(enum.Enum):
    IMAGE = "image"
    FILESYSTEM = "filesystem"
    REPOSITORY = "repository"

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, nullable=False)
    scan_type = Column(Enum(ScanType), nullable=False)
    status = Column(String, default="pending")
    result = Column(String, nullable=True)
