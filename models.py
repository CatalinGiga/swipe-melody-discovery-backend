from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum, Table, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
from pydantic import BaseModel, Field, constr, validator
from typing import List, Optional, Union
from datetime import datetime
import uuid

from database.config import Base

# SQLAlchemy Models
class Track(Base):
    __tablename__ = "tracks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    artist_id = Column(String(36), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)
    album_id = Column(String(36), ForeignKey("albums.id", ondelete="CASCADE"), nullable=False)
    cover_art = Column(String(512), nullable=False)
    duration = Column(String(10), nullable=False)
    genre = Column(String(100), nullable=False)
    mood = Column(String(100), nullable=False)
    release_year = Column(Integer, nullable=False)
    listened = Column(Boolean, default=False)
    favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Album(Base):
    __tablename__ = "albums"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    artist_id = Column(String(36), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)
    cover_art = Column(String(512), nullable=False)
    release_year = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Artist(Base):
    __tablename__ = "artists"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    image = Column(String(512), nullable=False)
    popularity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    genres = relationship("ArtistGenre", back_populates="artist", cascade="all, delete-orphan")
    albums = relationship("Album", back_populates="artist", cascade="all, delete-orphan")
    tracks = relationship("Track", back_populates="artist", cascade="all, delete-orphan")

class ArtistGenre(Base):
    __tablename__ = "artist_genres"

    artist_id = Column(String(36), ForeignKey("artists.id", ondelete="CASCADE"), primary_key=True)
    genre = Column(String(100), primary_key=True)
    
    artist = relationship("Artist", back_populates="genres")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(Enum("track", "album", "artist"), nullable=False)
    data_id = Column(String(36), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Pydantic Models for API
class ArtistBase(BaseModel):
    name: constr(min_length=1)
    image: constr(min_length=1)
    genres: List[str]
    popularity: int

    @validator('genres', pre=True)
    def extract_genres(cls, v):
        if not isinstance(v, list):
            return v
        return [genre.genre for genre in v]

    @validator('popularity')
    def validate_popularity(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Popularity must be between 0 and 100')
        return v

class ArtistCreate(ArtistBase):
    pass

class ArtistSchema(ArtistBase):
    id: str

    class Config:
        orm_mode = True

class AlbumBase(BaseModel):
    title: constr(min_length=1)
    artist: constr(min_length=1)
    cover_art: constr(min_length=1)
    release_year: int

    @validator('release_year')
    def validate_release_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year:
            raise ValueError(f'Release year must be between 1900 and {current_year}')
        return v

class AlbumCreate(AlbumBase):
    pass

class AlbumSchema(AlbumBase):
    id: str
    artist: ArtistSchema

    class Config:
        orm_mode = True

class TrackBase(BaseModel):
    title: constr(min_length=1)
    artist: constr(min_length=1)
    album: constr(min_length=1)
    cover_art: constr(min_length=1)
    duration: constr(min_length=1)
    genre: constr(min_length=1)
    mood: constr(min_length=1)
    release_year: int
    listened: bool = False
    favorite: bool = False

    @validator('release_year')
    def validate_release_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year:
            raise ValueError(f'Release year must be between 1900 and {current_year}')
        return v

class TrackCreate(TrackBase):
    pass

class TrackSchema(TrackBase):
    id: str
    artist: ArtistSchema
    album: AlbumSchema

    class Config:
        orm_mode = True

class FavoriteBase(BaseModel):
    type: str
    data_id: str

    @validator('type')
    def validate_type(cls, v):
        if v not in ['track', 'album', 'artist']:
            raise ValueError('Type must be one of: track, album, artist')
        return v

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteSchema(FavoriteBase):
    id: str

    class Config:
        orm_mode = True

# Filter model for query parameters
class FilterParams(BaseModel):
    genre: Optional[str] = None
    artist: Optional[str] = None
    release_year: Optional[int] = None
    mood: Optional[str] = None
    favorite: Optional[bool] = None
    listened: Optional[bool] = None 