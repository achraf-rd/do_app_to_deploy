from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

router = APIRouter()


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)
    category: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None


class ItemResponse(ItemBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# In-memory storage (replace with database in production)
items_db = {}


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """
    Create a new item
    """
    item_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    item_data = {
        "id": item_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "quantity": item.quantity,
        "category": item.category,
        "created_at": now,
        "updated_at": now
    }
    
    items_db[item_id] = item_data
    return item_data


@router.get("/items", response_model=List[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """
    List all items with pagination and filters
    """
    items = list(items_db.values())
    
    # Apply filters
    if category:
        items = [i for i in items if i.get("category") == category]
    
    if min_price is not None:
        items = [i for i in items if i["price"] >= min_price]
    
    if max_price is not None:
        items = [i for i in items if i["price"] <= max_price]
    
    return items[skip: skip + limit]


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """
    Get item by ID
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    return items_db[item_id]


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item_update: ItemUpdate):
    """
    Update item by ID
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    item = items_db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        item[field] = value
    
    item["updated_at"] = datetime.utcnow()
    items_db[item_id] = item
    
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    """
    Delete item by ID
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    del items_db[item_id]
    return None


@router.patch("/items/{item_id}/stock", response_model=ItemResponse)
async def update_stock(item_id: str, quantity_change: int):
    """
    Update item stock quantity (increment/decrement)
    """
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    item = items_db[item_id]
    new_quantity = item["quantity"] + quantity_change
    
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    item["quantity"] = new_quantity
    item["updated_at"] = datetime.utcnow()
    items_db[item_id] = item
    
    return item
