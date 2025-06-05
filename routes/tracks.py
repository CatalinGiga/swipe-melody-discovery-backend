from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from pydantic import parse_obj_as

from models import Track as TrackORM, TrackCreate, TrackSchema, FilterParams
from database.config import get_db
from utils import read_data, write_data
from config import TRACKS_FILE

router = APIRouter(
    prefix="/tracks",
    tags=["tracks"],
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

@router.get("/", response_model=List[TrackSchema])
def get_tracks(
    db: Session = Depends(get_db),
    genre: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    release_year: Optional[int] = None,
    mood: Optional[str] = None,
    favorite: Optional[bool] = None,
    listened: Optional[bool] = None,
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)")
):
    query = db.query(TrackORM)
    
    # Apply filters
    if genre:
        query = query.filter(TrackORM.genre == genre)
    if artist:
        query = query.filter(TrackORM.artist_id == artist)
    if album:
        query = query.filter(TrackORM.album_id == album)
    if release_year:
        query = query.filter(TrackORM.release_year == release_year)
    if mood:
        query = query.filter(TrackORM.mood == mood)
    if favorite is not None:
        query = query.filter(TrackORM.favorite == favorite)
    if listened is not None:
        query = query.filter(TrackORM.listened == listened)
    
    # Apply sorting
    if sort_by:
        if sort_order == "desc":
            query = query.order_by(getattr(TrackORM, sort_by).desc())
        else:
            query = query.order_by(getattr(TrackORM, sort_by))
    
    return query.all()

@router.get("/{track_id}", response_model=TrackSchema)
def get_track(track_id: str, db: Session = Depends(get_db)):
    track = db.query(TrackORM).filter(TrackORM.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

@router.post("/", response_model=TrackSchema)
def create_track(track: TrackCreate, db: Session = Depends(get_db)):
    db_track = TrackORM(**track.dict())
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

@router.put("/{track_id}", response_model=TrackSchema)
def update_track(track_id: str, track: TrackCreate, db: Session = Depends(get_db)):
    db_track = db.query(TrackORM).filter(TrackORM.id == track_id).first()
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    for key, value in track.dict().items():
        setattr(db_track, key, value)
    
    db.commit()
    db.refresh(db_track)
    return db_track

@router.delete("/{track_id}")
def delete_track(track_id: str, db: Session = Depends(get_db)):
    db_track = db.query(TrackORM).filter(TrackORM.id == track_id).first()
    if not db_track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    db.delete(db_track)
    db.commit()
    return {"message": "Track deleted successfully"} 