-- Create database
CREATE DATABASE IF NOT EXISTS swipe_melody;
USE swipe_melody;

-- Create artists table
CREATE TABLE IF NOT EXISTS artists (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image VARCHAR(512) NOT NULL,
    popularity INT NOT NULL CHECK (popularity >= 0 AND popularity <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create artist_genres table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS artist_genres (
    artist_id VARCHAR(36),
    genre VARCHAR(100),
    PRIMARY KEY (artist_id, genre),
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
);

-- Create albums table
CREATE TABLE IF NOT EXISTS albums (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id VARCHAR(36) NOT NULL,
    cover_art VARCHAR(512) NOT NULL,
    release_year INT NOT NULL CHECK (release_year >= 1900),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
);

-- Create tracks table
CREATE TABLE IF NOT EXISTS tracks (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id VARCHAR(36) NOT NULL,
    album_id VARCHAR(36) NOT NULL,
    cover_art VARCHAR(512) NOT NULL,
    duration VARCHAR(10) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    mood VARCHAR(100) NOT NULL,
    release_year INT NOT NULL CHECK (release_year >= 1900),
    listened BOOLEAN DEFAULT FALSE,
    favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
);

-- Create favorites table (polymorphic relationship)
CREATE TABLE IF NOT EXISTS favorites (
    id VARCHAR(36) PRIMARY KEY,
    type ENUM('track', 'album', 'artist') NOT NULL,
    data_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_favorite (type, data_id)
);

-- Create indexes for better performance
CREATE INDEX idx_tracks_artist ON tracks(artist_id);
CREATE INDEX idx_tracks_album ON tracks(album_id);
CREATE INDEX idx_albums_artist ON albums(artist_id);
CREATE INDEX idx_favorites_type_data ON favorites(type, data_id); 