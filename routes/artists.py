from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import parse_obj_as

from models import Artist as ArtistORM, ArtistCreate, ArtistSchema
from utils import read_data, write_data
from config import ARTISTS_FILE
from database.config import get_db

router = APIRouter(
    prefix="/artists",
    tags=["artists"],
)

def get_next_id(items):
    """
    Get the next available numeric ID by finding the highest current ID and adding 1.
    """
    if not items:
        return "1"
    
    # Get all existing IDs as integers where possible
    ids = []
    for item in items:
        try:
            id_value = int(item.get("id", 0))
            ids.append(id_value)
        except (ValueError, TypeError):
            # Skip non-numeric IDs
            pass
    
    # If no valid numeric IDs found, start from 1
    if not ids:
        return "1"
    
    # Return the next ID as a string
    return str(max(ids) + 1)

@router.get("/", response_model=List[ArtistSchema])
def get_artists(
    db: Session = Depends(get_db),
    genre: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="Sort by field (name, popularity, etc.)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)")
):
    query = db.query(ArtistORM)
    
    # Apply filters
    if genre:
        query = query.join(ArtistORM.genres).filter(ArtistORM.genres.any(genre=genre))
    
    # Apply sorting
    if sort_by:
        if sort_order == "desc":
            query = query.order_by(getattr(ArtistORM, sort_by).desc())
        else:
            query = query.order_by(getattr(ArtistORM, sort_by))
    
    return query.all()

@router.get("/{artist_id}", response_model=ArtistSchema)
def get_artist(artist_id: str, db: Session = Depends(get_db)):
    artist = db.query(ArtistORM).filter(ArtistORM.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist

@router.post("/", response_model=ArtistSchema)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = ArtistORM(**artist.dict())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist

@router.put("/{artist_id}", response_model=ArtistSchema)
def update_artist(artist_id: str, artist: ArtistCreate, db: Session = Depends(get_db)):
    db_artist = db.query(ArtistORM).filter(ArtistORM.id == artist_id).first()
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    for key, value in artist.dict().items():
        setattr(db_artist, key, value)
    
    db.commit()
    db.refresh(db_artist)
    return db_artist

@router.delete("/{artist_id}")
def delete_artist(artist_id: str, db: Session = Depends(get_db)):
    db_artist = db.query(ArtistORM).filter(ArtistORM.id == artist_id).first()
    if not db_artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    db.delete(db_artist)
    db.commit()
    return {"message": "Artist deleted successfully"} 