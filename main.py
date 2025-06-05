from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import uvicorn
import json
import os
from pathlib import Path

from models import Track, Album, ArtistSchema, TrackCreate, AlbumCreate, ArtistCreate
from utils import read_data, write_data
from config import DATA_DIR, TRACKS_FILE, ALBUMS_FILE, ARTISTS_FILE, FAVORITES_FILE

app = FastAPI(
    title="Swipe Melody Discovery API",
    description="Backend API for Swipe Melody Discovery application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data files if they don't exist
def init_data_files():
    if not TRACKS_FILE.exists():
        with open(TRACKS_FILE, "w") as f:
            json.dump([], f)
    
    if not ALBUMS_FILE.exists():
        with open(ALBUMS_FILE, "w") as f:
            json.dump([], f)
    
    if not ARTISTS_FILE.exists():
        with open(ARTISTS_FILE, "w") as f:
            json.dump([], f)
    
    if not FAVORITES_FILE.exists():
        with open(FAVORITES_FILE, "w") as f:
            json.dump([], f)

init_data_files()

@app.get("/")
async def root():
    return {"message": "Welcome to Swipe Melody Discovery API"}

# Include routes from other modules
from routes import tracks, albums, artists, favorites

app.include_router(tracks.router)
app.include_router(albums.router)
app.include_router(artists.router)
app.include_router(favorites.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 