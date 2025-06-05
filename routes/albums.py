from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import parse_obj_as

from models import Album as AlbumORM, AlbumCreate, AlbumSchema
from database.config import get_db
from utils import read_data, write_data
from config import ALBUMS_FILE, TRACKS_FILE

router = APIRouter(
    prefix="/albums",
    tags=["albums"],
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

@router.get("/", response_model=List[AlbumSchema])
def get_albums(
    db: Session = Depends(get_db),
    genre: Optional[str] = None,
    artist: Optional[str] = None,
    release_year: Optional[int] = None,
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)")
):
    query = db.query(AlbumORM)
    
    # Apply filters
    if artist:
        query = query.filter(AlbumORM.artist_id == artist)
    if release_year:
        query = query.filter(AlbumORM.release_year == release_year)
    
    # Apply sorting
    if sort_by:
        if sort_order == "desc":
            query = query.order_by(getattr(AlbumORM, sort_by).desc())
        else:
            query = query.order_by(getattr(AlbumORM, sort_by))
    
    return query.all()

@router.get("/{album_id}", response_model=AlbumSchema)
def get_album(album_id: str, db: Session = Depends(get_db)):
    album = db.query(AlbumORM).filter(AlbumORM.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return album

@router.post("/", response_model=AlbumSchema)
def create_album(album: AlbumCreate, db: Session = Depends(get_db)):
    db_album = AlbumORM(**album.dict())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

@router.put("/{album_id}", response_model=AlbumSchema)
def update_album(album_id: str, album: AlbumCreate, db: Session = Depends(get_db)):
    db_album = db.query(AlbumORM).filter(AlbumORM.id == album_id).first()
    if not db_album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    for key, value in album.dict().items():
        setattr(db_album, key, value)
    
    db.commit()
    db.refresh(db_album)
    return db_album

@router.delete("/{album_id}")
def delete_album(album_id: str, db: Session = Depends(get_db)):
    db_album = db.query(AlbumORM).filter(AlbumORM.id == album_id).first()
    if not db_album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    db.delete(db_album)
    db.commit()
    return {"message": "Album deleted successfully"} 