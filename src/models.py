from sqlalchemy import Column, Integer, String, Float,Text,DateTime
from database import Base
from datetime import datetime
metadata = Base.metadata

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)

class HighlightModel(Base):
    __tablename__ = "highlights"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    text = Column(Text, nullable=False)
    note = Column(Text, nullable=True)  # 註
    author = Column(String, nullable=True)
    chapter = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
