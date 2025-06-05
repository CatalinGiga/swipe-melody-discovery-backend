import pytest
from fastapi.testclient import TestClient
import json
import os
import shutil
from pathlib import Path

# Import the app from the main module
from main import app, TRACKS_FILE, DATA_DIR

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
    
    # Save the original data directory and file paths
    original_data_dir = app.dependency_overrides.get('DATA_DIR', DATA_DIR)
    original_tracks_file = app.dependency_overrides.get('TRACKS_FILE', TRACKS_FILE)
    
    # Override the data directory and file paths for testing
    app.dependency_overrides['DATA_DIR'] = TEST_DATA_DIR
    app.dependency_overrides['TRACKS_FILE'] = test_tracks_file
    
    # Create an empty tracks file
    with open(test_tracks_file, "w") as f:
        json.dump([], f)
    
    yield
    
    # Reset the data directory and file paths
    if 'DATA_DIR' in app.dependency_overrides:
        app.dependency_overrides['DATA_DIR'] = original_data_dir
    if 'TRACKS_FILE' in app.dependency_overrides:
        app.dependency_overrides['TRACKS_FILE'] = original_tracks_file
    
    # Clean up the test data directory
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)

def test_create_track():
    """Test creating a track."""
    response = client.post("/tracks/", json=TEST_TRACK)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == TEST_TRACK["title"]
    assert data["artist"] == TEST_TRACK["artist"]
    assert "id" in data

def test_get_tracks():
    """Test getting all tracks."""
    # Create a track first
    client.post("/tracks/", json=TEST_TRACK)
    
    response = client.get("/tracks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == TEST_TRACK["title"]

def test_get_track_by_id():
    """Test getting a track by ID."""
    # Create a track first
    create_response = client.post("/tracks/", json=TEST_TRACK)
    track_id = create_response.json()["id"]
    
    response = client.get(f"/tracks/{track_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == track_id
    assert data["title"] == TEST_TRACK["title"]

def test_update_track():
    """Test updating a track."""
    # Create a track first
    create_response = client.post("/tracks/", json=TEST_TRACK)
    track_id = create_response.json()["id"]
    
    # Update the track
    updated_track = {**TEST_TRACK, "title": "Updated Track Title"}
    response = client.patch(f"/tracks/{track_id}", json=updated_track)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == track_id
    assert data["title"] == "Updated Track Title"
    
    # Verify the update
    response = client.get(f"/tracks/{track_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Track Title"

def test_delete_track():
    """Test deleting a track."""
    # Create a track first
    create_response = client.post("/tracks/", json=TEST_TRACK)
    track_id = create_response.json()["id"]
    
    # Delete the track
    response = client.delete(f"/tracks/{track_id}")
    assert response.status_code == 200
    
    # Verify the deletion
    response = client.get(f"/tracks/{track_id}")
    assert response.status_code == 404

def test_filter_tracks():
    """Test filtering tracks."""
    # Create tracks with different genres
    rock_track = {**TEST_TRACK, "genre": "Rock", "artist": "Rock Artist"}
    pop_track = {**TEST_TRACK, "genre": "Pop", "artist": "Pop Artist"}
    
    client.post("/tracks/", json=rock_track)
    client.post("/tracks/", json=pop_track)
    
    # Filter by genre
    response = client.get("/tracks/?genre=Rock")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(track["genre"] == "Rock" for track in data)
    
    # Filter by artist
    response = client.get("/tracks/?artist=Pop%20Artist")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(track["artist"] == "Pop Artist" for track in data)

def test_sort_tracks():
    """Test sorting tracks."""
    # Create tracks with different titles
    track_a = {**TEST_TRACK, "title": "A Track"}
    track_b = {**TEST_TRACK, "title": "B Track"}
    track_c = {**TEST_TRACK, "title": "C Track"}
    
    client.post("/tracks/", json=track_c)
    client.post("/tracks/", json=track_a)
    client.post("/tracks/", json=track_b)
    
    # Sort by title ascending
    response = client.get("/tracks/?sort_by=title&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    titles = [track["title"] for track in data]
    assert titles[0] <= titles[1] <= titles[2]
    
    # Sort by title descending
    response = client.get("/tracks/?sort_by=title&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    titles = [track["title"] for track in data]
    assert titles[0] >= titles[1] >= titles[2]

def test_validation():
    """Test validation of track data."""
    # Missing required field
    invalid_track = {**TEST_TRACK}
    del invalid_track["title"]
    response = client.post("/tracks/", json=invalid_track)
    assert response.status_code == 422
    
    # Invalid release year (future)
    invalid_track = {**TEST_TRACK, "releaseYear": 3000}
    response = client.post("/tracks/", json=invalid_track)
    assert response.status_code == 422 