# Swipe Melody Discovery API

This is the backend API for the Swipe Melody Discovery application, built with FastAPI.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Navigate to the backend directory
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the server

To run the development server:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

## API Documentation

After starting the server, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Initializing Demo Data

To initialize the application with demo data, run:

```bash
python init_data.py
```

This will create sample tracks, artists, albums, and favorites in the `data` directory.

## API Endpoints

### Tracks

- `GET /tracks`: Get all tracks with optional filtering and sorting
- `GET /tracks/{track_id}`: Get a specific track by ID
- `POST /tracks/`: Create a new track
- `PATCH /tracks/{track_id}`: Update an existing track
- `DELETE /tracks/{track_id}`: Delete a track

### Albums

- `GET /albums`: Get all albums with optional filtering and sorting
- `GET /albums/{album_id}`: Get a specific album by ID
- `POST /albums/`: Create a new album
- `PATCH /albums/{album_id}`: Update an existing album
- `DELETE /albums/{album_id}`: Delete an album

### Artists

- `GET /artists`: Get all artists with optional filtering and sorting
- `GET /artists/{artist_id}`: Get a specific artist by ID
- `POST /artists/`: Create a new artist
- `PATCH /artists/{artist_id}`: Update an existing artist
- `DELETE /artists/{artist_id}`: Delete an artist

### Favorites

- `GET /favorites`: Get all favorites with optional filtering and sorting
- `GET /favorites/{favorite_id}`: Get a specific favorite by ID
- `POST /favorites/`: Add a new item to favorites
- `DELETE /favorites/{favorite_id}`: Remove an item from favorites
- `GET /favorites/check/{item_type}/{item_id}`: Check if an item is in favorites

## Running Tests

To run the tests:

```bash
pytest
```

This will execute all the unit tests in the `tests` directory.

## Data Storage

Data is stored in JSON files in the `data` directory:

- `tracks.json`: Track data
- `albums.json`: Album data
- `artists.json`: Artist data
- `favorites.json`: Favorite items data 