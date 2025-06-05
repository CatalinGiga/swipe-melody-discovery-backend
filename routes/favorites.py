from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any

from models import Favorite as FavoriteORM, FavoriteCreate, FavoriteSchema
from database.config import get_db

router = APIRouter(
    prefix="/favorites",
    tags=["favorites"],
)

@router.get("/", response_model=List[FavoriteSchema])
def get_favorites(
    db: Session = Depends(get_db),
    type: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="Sort by field (type, created_at, etc.)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)")
):
    query = db.query(FavoriteORM)
    
    # Apply filters
    if type:
        query = query.filter(FavoriteORM.type == type)
    
    # Apply sorting
    if sort_by:
        if sort_order == "desc":
            query = query.order_by(getattr(FavoriteORM, sort_by).desc())
        else:
            query = query.order_by(getattr(FavoriteORM, sort_by))
    
    return query.all()

@router.get("/{favorite_id}", response_model=FavoriteSchema)
def get_favorite(favorite_id: str, db: Session = Depends(get_db)):
    favorite = db.query(FavoriteORM).filter(FavoriteORM.id == favorite_id).first()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return favorite

@router.post("/", response_model=FavoriteSchema)
def create_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    # Check if favorite already exists
    existing = db.query(FavoriteORM).filter(
        FavoriteORM.type == favorite.type,
        FavoriteORM.data_id == favorite.data_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Favorite already exists")
    
    db_favorite = FavoriteORM(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: str, db: Session = Depends(get_db)):
    db_favorite = db.query(FavoriteORM).filter(FavoriteORM.id == favorite_id).first()
    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(db_favorite)
    db.commit()
    return {"message": "Favorite deleted successfully"}

@router.get("/check/{item_type}/{item_id}", response_model=bool)
async def check_favorite(
    item_type: str = Path(..., description="The type of the item"),
    item_id: str = Path(..., description="The ID of the item"),
    db: Session = Depends(get_db)
):
    """
    Check if an item is in favorites.
    """
    if item_type not in ["track", "album", "artist"]:
        raise HTTPException(status_code=400, detail=f"Invalid item type: {item_type}")
    
    # Query the database for the favorite
    favorite = db.query(FavoriteORM).filter(
        FavoriteORM.type == item_type,
        FavoriteORM.data_id == item_id
    ).first()
    
    return favorite is not None 