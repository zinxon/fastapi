from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import ItemModel
from schemas import ItemCreate
from fastapi import HTTPException

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