import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import models
import schemas
from database import engine, get_db
from services.external_service import ExternalService

app = FastAPI(
    title="FastAPI Microservice",
    description="A scalable FastAPI microservice with PostgreSQL",
    version="1.0.0"
)

external_service = ExternalService()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"status": "healthy"}

@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db=db, item=item)

@app.get("/items/", response_model=list[schemas.Item])
async def list_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_name}", response_model=schemas.Item)
async def get_item(item_name: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_item(db=db, item_name=item_name)

@app.get("/external/items/{item_id}")
async def get_external_item(item_id: str):
    return await external_service.fetch_external_data(item_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)