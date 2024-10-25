import uvicorn
from fastapi import FastAPI, Depends,Header, HTTPException
from typing import Optional,List
from sqlalchemy.ext.asyncio import AsyncSession
import crud
import models
# import schemas 
from schemas import (
    Item,
    ItemCreate,
    MoonReaderRequest, 
    HighlightCreate, 
    HighlightUpdate, 
    Highlight
)
from database import engine, get_db
from services.external_service import ExternalService
from services.storage_service import StorageService
from services.moonreader_service import MoonReaderService
import os
from dotenv import load_dotenv  
from mangum import Mangum # this line is where we import Mangum

load_dotenv()
app = FastAPI(
    title="FastAPI Microservice",
    description="A scalable FastAPI microservice with PostgreSQL",
    version="1.0.0"
)
handler = Mangum(app) # this line is where we use Mangum

# Initialize services
external_service = ExternalService()
storage_service = StorageService()
moonreader_service = MoonReaderService(
    token=os.getenv("MOONREADER_TOKEN", "default_token"),
    storage_service=storage_service
)

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"status": "healthy"}

@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db=db, item=item)

@app.get("/items/", response_model=list[Item])
async def list_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_name}", response_model=Item)
async def get_item(item_name: str, db: AsyncSession = Depends(get_db)):
    return await crud.get_item(db=db, item_name=item_name)

@app.get("/external/items/{item_id}")
async def get_external_item(item_id: str):
    return await external_service.fetch_external_data(item_id)

@app.post("/highlights")
async def create_highlights(
    request: MoonReaderRequest,
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    # Validate token
    # moonreader_service.validate_token(authorization)

    # Process the first highlight (maintaining original behavior)
    if not request.highlights:
        raise HTTPException(status_code=400, detail="No highlights provided")

    highlight = request.highlights[0]
    # Create highlight in database
    highlight_create = HighlightCreate(
        text=highlight.text,
        note=highlight.note,
        title=highlight.title,
        author=highlight.author,
        chapter=highlight.chapter
    )
    db_highlight = await crud.create_highlight(db, highlight_create)
    
    # Process highlight for file storage
    await moonreader_service.process_highlight(highlight.model_dump())

    return {"status": "Success", "highlight_id": db_highlight.id}

@app.get("/highlights", response_model=List[Highlight])
async def read_highlights(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    highlights = await crud.get_all_highlights(db, skip=skip, limit=limit)
    return highlights

@app.get("/highlights/{highlight_id}", response_model=Highlight)
async def read_highlight(
    highlight_id: int,
    db: AsyncSession = Depends(get_db)
):
    highlight = await crud.get_highlight(db, highlight_id)
    return highlight

@app.get("/highlights/by-title/{title}", response_model=List[Highlight])
async def read_highlights_by_title(
    title: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    highlights = await crud.get_highlights_by_title(db, title, skip=skip, limit=limit)
    return highlights

@app.put("/highlights/{highlight_id}", response_model=Highlight)
async def update_highlight(
    highlight_id: int,
    highlight: HighlightUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated_highlight = await crud.update_highlight(db, highlight_id, highlight)
    return updated_highlight

@app.delete("/highlights/{highlight_id}")
async def delete_highlight(
    highlight_id: int,
    db: AsyncSession = Depends(get_db)
):
    await crud.delete_highlight(db, highlight_id)
    return {"status": "Success", "message": "Highlight deleted"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)

