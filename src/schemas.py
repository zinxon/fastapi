from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

class MoonReaderHighlight(BaseModel):
    text: str
    note: Optional[str] = None
    title: str
    author: Optional[str] = None
    chapter: Optional[str] = None

class MoonReaderRequest(BaseModel):
    highlights: List[MoonReaderHighlight]

class HighlightBase(BaseModel):
    text: str
    note: Optional[str] = None
    title: str
    author: Optional[str] = None
    chapter: Optional[str] = None

class HighlightCreate(HighlightBase):
    pass

class HighlightUpdate(HighlightBase):
    pass

class Highlight(HighlightBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True