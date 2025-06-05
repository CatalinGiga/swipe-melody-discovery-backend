"""
Script to initialize demo data for the Swipe Melody Discovery API.
"""
import json
import os
from pathlib import Path

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Data files
TRACKS_FILE = DATA_DIR / "tracks.json"
ALBUMS_FILE = DATA_DIR / "albums.json"
ARTISTS_FILE = DATA_DIR / "artists.json"
FAVORITES_FILE = DATA_DIR / "favorites.json"

# Demo data with numeric IDs
demo_tracks = [
    {
        "id": "1",
        "title": "Midnight Serenade",
        "artist": "Luna Echo",
        "album": "Twilight Hours",
        "coverArt": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "duration": "3:45",
        "genre": "Indie Pop",
        "mood": "Chill",
        "releaseYear": 2023,
        "listened": False,
        "favorite": False,
    },
    {
        "id": "2",
        "title": "Electric Dreams",
        "artist": "Neon Pulse",
        "album": "Synthetic Memories",
        "coverArt": "https://images.unsplash.com/photo-1614149162883-504ce4d13909?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "duration": "4:20",
        "genre": "Synthwave",
        "mood": "Energetic",
        "releaseYear": 2022,
        "listened": False,
        "favorite": False,
    },
    {
        "id": "3",
        "title": "Velvet Moon",
        "artist": "Aurora Skies",
        "album": "Celestial Journey",
        "coverArt": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "duration": "3:28",
        "genre": "Dream Pop",
        "mood": "Dreamy",
        "releaseYear": 2023,
        "listened": True,
        "favorite": True,
    },
    {
        "id": "4",
        "title": "Urban Symphony",
        "artist": "Metro Echoes",
        "album": "City Lights",
        "coverArt": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "duration": "5:12",
        "genre": "Electronic",
        "mood": "Atmospheric",
        "releaseYear": 2022,
        "listened": False,
        "favorite": False,
    },
    {
        "id": "5",
        "title": "Silent Waves",
        "artist": "Ocean Drift",
        "album": "Coastal Memories",
        "coverArt": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "duration": "4:50",
        "genre": "Ambient",
        "mood": "Relaxing",
        "releaseYear": 2021,
        "listened": True,
        "favorite": False,
    },
]

demo_artists = [
    {
        "id": "1",
        "name": "Luna Echo",
        "image": "https://images.unsplash.com/photo-1516575150278-77136aed6920?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "genres": ["Indie Pop", "Alternative"],
        "popularity": 85,
    },
    {
        "id": "2",
        "name": "Neon Pulse",
        "image": "https://images.unsplash.com/photo-1511367461989-f85a21fda167?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "genres": ["Synthwave", "Electronic"],
        "popularity": 78,
    },
    {
        "id": "3",
        "name": "Aurora Skies",
        "image": "https://images.unsplash.com/photo-1507041957456-9c397ce39c97?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "genres": ["Dream Pop", "Ambient"],
        "popularity": 92,
    },
    {
        "id": "4",
        "name": "Metro Echoes",
        "image": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "genres": ["Electronic", "Techno"],
        "popularity": 74,
    },
    {
        "id": "5",
        "name": "Ocean Drift",
        "image": "https://images.unsplash.com/photo-1508186225823-0963cf9ab0de?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "genres": ["Ambient", "Chillout"],
        "popularity": 68,
    },
]

# Create albums referencing the first 3 tracks
demo_albums = [
    {
        "id": "1",
        "title": "Twilight Hours",
        "artist": "Luna Echo",
        "coverArt": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "releaseYear": 2023,
        "tracks": [demo_tracks[0]["id"]],
    },
    {
        "id": "2",
        "title": "Synthetic Memories",
        "artist": "Neon Pulse",
        "coverArt": "https://images.unsplash.com/photo-1614149162883-504ce4d13909?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "releaseYear": 2022,
        "tracks": [demo_tracks[1]["id"]],
    },
    {
        "id": "3",
        "title": "Celestial Journey",
        "artist": "Aurora Skies",
        "coverArt": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=500",
        "releaseYear": 2023,
        "tracks": [demo_tracks[2]["id"]],
    },
]

# Create favorites with one track and one artist
demo_favorites = [
    {
        "id": "1",
        "type": "track",
        "data": demo_tracks[2],
    },
    {
        "id": "2",
        "type": "artist",
        "data": demo_artists[2],
    },
]

def write_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def init_data():
    # Write data to files
    write_data(TRACKS_FILE, demo_tracks)
    write_data(ARTISTS_FILE, demo_artists)
    write_data(ALBUMS_FILE, demo_albums)
    write_data(FAVORITES_FILE, demo_favorites)
    
    print(f"Initialized {len(demo_tracks)} tracks")
    print(f"Initialized {len(demo_artists)} artists")
    print(f"Initialized {len(demo_albums)} albums")
    print(f"Initialized {len(demo_favorites)} favorites")

if __name__ == "__main__":
    init_data() 