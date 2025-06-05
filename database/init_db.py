import json
from pathlib import Path
from sqlalchemy.orm import Session
import uuid
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Base
from models import (
    Artist as ArtistORM,
    ArtistGenre,
    Album as AlbumORM,
    Track as TrackORM,
    Favorite as FavoriteORM
)
from database.config import SessionLocal, engine

def init_db():
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Load JSON data
        data_dir = Path(__file__).parent.parent / "data"
        
        with open(data_dir / "artists.json", "r") as f:
            artists_data = json.load(f)
        
        with open(data_dir / "albums.json", "r") as f:
            albums_data = json.load(f)
        
        with open(data_dir / "tracks.json", "r") as f:
            tracks_data = json.load(f)
        
        with open(data_dir / "favorites.json", "r") as f:
            favorites_data = json.load(f)
        
        # Create artists
        artist_map = {}  # Map to store artist IDs
        for artist_data in artists_data:
            # Create Artist without genres
            artist = ArtistORM(
                id=artist_data["id"],
                name=artist_data["name"],
                image=artist_data["image"],
                popularity=artist_data["popularity"]
            )
            db.add(artist)
            artist_map[artist_data["name"]] = artist_data["id"]
            # Add genres via ArtistGenre
            for genre in artist_data.get("genres", []):
                artist_genre = ArtistGenre(
                    artist_id=artist_data["id"],
                    genre=genre
                )
                db.add(artist_genre)
        
        # Create albums
        album_map = {}  # Map to store album IDs
        for album_data in albums_data:
            album = AlbumORM(
                id=album_data["id"],
                title=album_data["title"],
                artist_id=artist_map[album_data["artist"]],
                cover_art=album_data["coverArt"],
                release_year=album_data["releaseYear"]
            )
            db.add(album)
            album_map[album_data["title"]] = album_data["id"]
        
        # Create tracks and handle missing albums
        for track_data in tracks_data:
            # Check if album exists, if not create it
            if track_data["album"] not in album_map:
                # Create a new album ID
                new_album_id = str(uuid.uuid4())
                # Create the album
                album = AlbumORM(
                    id=new_album_id,
                    title=track_data["album"],
                    artist_id=artist_map[track_data["artist"]],
                    cover_art=track_data["coverArt"],
                    release_year=track_data["releaseYear"]
                )
                db.add(album)
                album_map[track_data["album"]] = new_album_id
            
            track = TrackORM(
                id=track_data["id"],
                title=track_data["title"],
                artist_id=artist_map[track_data["artist"]],
                album_id=album_map[track_data["album"]],
                cover_art=track_data["coverArt"],
                duration=track_data["duration"],
                genre=track_data["genre"],
                mood=track_data["mood"],
                release_year=track_data["releaseYear"],
                listened=track_data["listened"],
                favorite=track_data["favorite"]
            )
            db.add(track)
        
        # Create favorites
        for favorite_data in favorites_data:
            favorite = FavoriteORM(
                id=favorite_data["id"],
                type=favorite_data["type"],
                data_id=favorite_data["data"]["id"]
            )
            db.add(favorite)
        
        # Commit all changes
        db.commit()
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 