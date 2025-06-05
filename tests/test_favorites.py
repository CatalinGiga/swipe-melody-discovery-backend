import pytest
from fastapi.testclient import TestClient
import json
import os
import shutil
from pathlib import Path

# Import the app from the main module
from main import app, TRACKS_FILE, ALBUMS_FILE, ARTISTS_FILE, FAVORITES_FILE, DATA_DIR

# Create a test client for making requests
client = TestClient(app)

# Test data
TEST_TRACK = {
    "title": "Test Track",
    "artist": "Test Artist",
    "album": "Test Album",
    "coverArt": "https://example.com/cover.jpg",
    "duration": "3:30",
    "genre": "Test Genre",
    "mood": "Test Mood",
    "releaseYear": 2023,
    "listened": False,
    "favorite": False
}

TEST_ARTIST = {
    "name": "Test Artist",
    "image": "https://example.com/artist.jpg",
    "genres": ["Test Genre", "Pop"],
    "popularity": 75
}

# Create a test data directory
TEST_DATA_DIR = Path("test_data")

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Setup before each test and teardown after each test.
    """
    # Create test data directory and files
    TEST_DATA_DIR.mkdir(exist_ok=True)
    test_tracks_file = TEST_DATA_DIR / "tracks.json"
    test_albums_file = TEST_DATA_DIR / "albums.json"
    test_artists_file = TEST_DATA_DIR / "artists.json"
    test_favorites_file = TEST_DATA_DIR / "favorites.json"
    
    # Save the original data directory and file paths
    original_data_dir = app.dependency_overrides.get('DATA_DIR', DATA_DIR)
    original_tracks_file = app.dependency_overrides.get('TRACKS_FILE', TRACKS_FILE)
    original_albums_file = app.dependency_overrides.get('ALBUMS_FILE', ALBUMS_FILE)
    original_artists_file = app.dependency_overrides.get('ARTISTS_FILE', ARTISTS_FILE)
    original_favorites_file = app.dependency_overrides.get('FAVORITES_FILE', FAVORITES_FILE)
    
    # Override the data directory and file paths for testing
    app.dependency_overrides['DATA_DIR'] = TEST_DATA_DIR
    app.dependency_overrides['TRACKS_FILE'] = test_tracks_file
    app.dependency_overrides['ALBUMS_FILE'] = test_albums_file
    app.dependency_overrides['ARTISTS_FILE'] = test_artists_file
    app.dependency_overrides['FAVORITES_FILE'] = test_favorites_file
    
    # Create empty data files
    with open(test_tracks_file, "w") as f:
        json.dump([], f)
    with open(test_albums_file, "w") as f:
        json.dump([], f)
    with open(test_artists_file, "w") as f:
        json.dump([], f)
    with open(test_favorites_file, "w") as f:
        json.dump([], f)
    
    yield
    
    # Reset the data directory and file paths
    if 'DATA_DIR' in app.dependency_overrides:
        app.dependency_overrides['DATA_DIR'] = original_data_dir
    if 'TRACKS_FILE' in app.dependency_overrides:
        app.dependency_overrides['TRACKS_FILE'] = original_tracks_file
    if 'ALBUMS_FILE' in app.dependency_overrides:
        app.dependency_overrides['ALBUMS_FILE'] = original_albums_file
    if 'ARTISTS_FILE' in app.dependency_overrides:
        app.dependency_overrides['ARTISTS_FILE'] = original_artists_file
    if 'FAVORITES_FILE' in app.dependency_overrides:
        app.dependency_overrides['FAVORITES_FILE'] = original_favorites_file
    
    # Clean up the test data directory
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)

@pytest.fixture
def create_track_and_artist():
    """Create a test track and artist for testing favorites"""
    # Create a track
    track_response = client.post("/tracks/", json=TEST_TRACK)
    track_id = track_response.json()["id"]
    
    # Create an artist
    artist_response = client.post("/artists/", json=TEST_ARTIST)
    artist_id = artist_response.json()["id"]
    
    return {"track_id": track_id, "artist_id": artist_id}

def test_add_track_to_favorites(create_track_and_artist):
    """Test adding a track to favorites."""
    track_id = create_track_and_artist["track_id"]
    
    # Add the track to favorites
    favorite_data = {
        "type": "track",
        "data_id": track_id
    }
    response = client.post("/favorites/", json=favorite_data)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "track"
    assert data["data"]["id"] == track_id
    assert "id" in data

def test_add_artist_to_favorites(create_track_and_artist):
    """Test adding an artist to favorites."""
    artist_id = create_track_and_artist["artist_id"]
    
    # Add the artist to favorites
    favorite_data = {
        "type": "artist",
        "data_id": artist_id
    }
    response = client.post("/favorites/", json=favorite_data)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "artist"
    assert data["data"]["id"] == artist_id
    assert "id" in data

def test_get_favorites(create_track_and_artist):
    """Test getting all favorites."""
    track_id = create_track_and_artist["track_id"]
    artist_id = create_track_and_artist["artist_id"]

    # First, get the current count of favorites
    initial_response = client.get("/favorites/")
    initial_count = len(initial_response.json())

    # Add items to favorites
    client.post("/favorites/", json={"type": "track", "data_id": track_id})
    client.post("/favorites/", json={"type": "artist", "data_id": artist_id})

    # Get all favorites
    response = client.get("/favorites/")
    assert response.status_code == 200
    data = response.json()
    
    # Verify that there are 2 more favorites than before
    assert len(data) == initial_count + 2

def test_filter_favorites_by_type(create_track_and_artist):
    """Test filtering favorites by type."""
    track_id = create_track_and_artist["track_id"]
    artist_id = create_track_and_artist["artist_id"]

    # First, get the current count of track favorites
    initial_response = client.get("/favorites/?item_type=track")
    initial_track_count = len(initial_response.json())

    # Add items to favorites
    client.post("/favorites/", json={"type": "track", "data_id": track_id})
    client.post("/favorites/", json={"type": "artist", "data_id": artist_id})

    # Filter favorites by type=track
    response = client.get("/favorites/?item_type=track")
    assert response.status_code == 200
    data = response.json()
    
    # Verify that there is 1 more track favorite than before
    assert len(data) == initial_track_count + 1

    # Filter favorites by type=artist
    initial_response = client.get("/favorites/?item_type=artist")
    initial_artist_count = len(initial_response.json()) - 1  # Subtract 1 because we already added an artist above
    
    response = client.get("/favorites/?item_type=artist")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == initial_artist_count + 1

def test_get_favorite_by_id(create_track_and_artist):
    """Test getting a favorite by ID."""
    track_id = create_track_and_artist["track_id"]
    
    # Add an item to favorites
    favorite_response = client.post("/favorites/", json={"type": "track", "data_id": track_id})
    favorite_id = favorite_response.json()["id"]
    
    # Get the favorite by ID
    response = client.get(f"/favorites/{favorite_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == favorite_id
    assert data["type"] == "track"
    assert data["data"]["id"] == track_id

def test_delete_favorite(create_track_and_artist):
    """Test deleting a favorite."""
    track_id = create_track_and_artist["track_id"]

    # Add an item to favorites
    favorite_response = client.post("/favorites/", json={"type": "track", "data_id": track_id})
    favorite_id = favorite_response.json()["id"]

    # Delete the favorite
    response = client.delete(f"/favorites/{favorite_id}")
    assert response.status_code == 200

    # Verify the deletion
    response = client.get(f"/favorites/{favorite_id}")
    assert response.status_code == 404

    # Verify the specific favorite was removed
    response = client.get("/favorites/")
    assert response.status_code == 200
    data = response.json()
    assert all(item["id"] != favorite_id for item in data)

def test_check_favorite(create_track_and_artist):
    """Test checking if an item is in favorites."""
    track_id = create_track_and_artist["track_id"]
    artist_id = create_track_and_artist["artist_id"]
    
    # Add the track to favorites
    client.post("/favorites/", json={"type": "track", "data_id": track_id})
    
    # Check if track is in favorites (should be true)
    response = client.get(f"/favorites/check/track/{track_id}")
    assert response.status_code == 200
    assert response.json() is True
    
    # Check if artist is in favorites (should be false)
    response = client.get(f"/favorites/check/artist/{artist_id}")
    assert response.status_code == 200
    assert response.json() is False

def test_validation_invalid_type():
    """Test validation for invalid item type."""
    # Invalid type
    response = client.post("/favorites/", json={"type": "invalid", "data_id": "123"})
    assert response.status_code == 422  # Validation error

def test_validation_nonexistent_item(create_track_and_artist):
    """Test validation for nonexistent item."""
    # Nonexistent track ID
    response = client.post("/favorites/", json={"type": "track", "data_id": "nonexistent-id"})
    assert response.status_code == 404 