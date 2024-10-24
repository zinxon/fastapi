from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from models import ItemModel, HighlightModel
from schemas import ItemCreate, HighlightCreate, HighlightUpdate
from fastapi import HTTPException
from typing import List, Optional
from datetime import datetime

async def create_item(db: AsyncSession, item: ItemCreate):
    db_item = ItemModel(**item.model_dump())
    db.add(db_item)
    try:
        await db.commit()
        await db.refresh(db_item)
        return db_item
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def get_item(db: AsyncSession, item_name: str):
    query = select(ItemModel).where(ItemModel.name == item_name)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(ItemModel).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_highlight(db: AsyncSession, highlight: HighlightCreate) -> HighlightModel:
    # db_highlight = HighlightModel(
    #     text=highlight.text,
    #     note=highlight.note,
    #     title=highlight.title,
    #     author=highlight.author
    # )
    db_highlight = HighlightModel(**highlight.model_dump())
    db.add(db_highlight)
    try:
        await db.commit()
        await db.refresh(db_highlight)
        return db_highlight
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def get_highlight(db: AsyncSession, highlight_id: int) -> Optional[HighlightModel]:
    query = select(HighlightModel).where(HighlightModel.id == highlight_id)
    result = await db.execute(query)
    highlight = result.scalar_one_or_none()
    if highlight is None:
        raise HTTPException(status_code=404, detail="Highlight not found")
    return highlight

async def get_highlights_by_title(
    db: AsyncSession, 
    title: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[HighlightModel]:
    query = select(HighlightModel)\
        .where(HighlightModel.title == title)\
        .offset(skip)\
        .limit(limit)\
        .order_by(HighlightModel.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def get_all_highlights(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 100
) -> List[HighlightModel]:
    query = select(HighlightModel)\
        .offset(skip)\
        .limit(limit)\
        .order_by(HighlightModel.created_at.desc())
    print(query)
    result = await db.execute(query)
    return result.scalars().all()

async def update_highlight(
    db: AsyncSession,
    highlight_id: int,
    highlight_update: HighlightUpdate
) -> HighlightModel:
    query = select(HighlightModel).where(HighlightModel.id == highlight_id)
    result = await db.execute(query)
    db_highlight = result.scalar_one_or_none()
    
    if db_highlight is None:
        raise HTTPException(status_code=404, detail="Highlight not found")
    
    update_data = highlight_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_highlight, field, value)
    
    try:
        await db.commit()
        await db.refresh(db_highlight)
        return db_highlight
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

async def delete_highlight(db: AsyncSession, highlight_id: int) -> bool:
    query = delete(HighlightModel).where(HighlightModel.id == highlight_id)
    result = await db.execute(query)
    try:
        await db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Highlight not found")
        return True
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))