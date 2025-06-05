from pathlib import Path

# Directory for storing data
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
 
# Data files
TRACKS_FILE = DATA_DIR / "tracks.json"
ALBUMS_FILE = DATA_DIR / "albums.json"
ARTISTS_FILE = DATA_DIR / "artists.json"
FAVORITES_FILE = DATA_DIR / "favorites.json" 