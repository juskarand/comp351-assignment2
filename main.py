from fastapi import FastAPI, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import Base, engine, get_db
from models import InventoryItem
from schemas import ItemCreate, ItemUpdate, ItemResponse
    
from typing import Optional, List

app = FastAPI(title="Assignment 2 - Lego Inventory Items API")

Base.metadata.create_all(bind=engine)


def err(code: str, message: str):
    return {"error": {"code": code, "message": message}}


@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    existing = db.query(InventoryItem).filter(InventoryItem.sku == payload.sku).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err("SKU_EXISTS", "An item with this sku already exists"),
        )

    item = InventoryItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items", response_model=List[ItemResponse])
def list_items(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None, description="Search sku/name/location"),
    min_qty: Optional[int] = Query(default=None, ge=0),
    low_stock: Optional[bool] = Query(default=None, description="If true, quantity <= reorder_level"),
    skip: int = 0,
    limit: int = 50,
):
    query = db.query(InventoryItem)

    if q:
        like = f"%{q.strip()}%"
        query = query.filter(
            or_(
                InventoryItem.sku.ilike(like),
                InventoryItem.name.ilike(like),
                InventoryItem.location.ilike(like),
            )
        )

    if min_qty is not None:
        query = query.filter(InventoryItem.quantity >= min_qty)

    if low_stock is not None:
        if low_stock:
            query = query.filter(InventoryItem.quantity <= InventoryItem.reorder_level)
        else:
            query = query.filter(InventoryItem.quantity > InventoryItem.reorder_level)

    return query.offset(skip).limit(limit).all()


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err("NOT_FOUND", "Item not found"),
        )
    return item


@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err("NOT_FOUND", "Item not found"),
        )

    data = payload.model_dump(exclude_unset=True)

    if "sku" in data and data["sku"] is not None:
        existing = (
            db.query(InventoryItem)
            .filter(InventoryItem.sku == data["sku"], InventoryItem.id != item_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=err("SKU_EXISTS", "sku already used by another item"),
            )

    for k, v in data.items():
        setattr(item, k, v)

    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err("NOT_FOUND", "Item not found"),
        )

    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.get("/health")
def health():
    return {"status": "ok"}