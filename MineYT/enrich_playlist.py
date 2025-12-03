import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import eyed3
import requests
import re

# Flag to use folder name as album name
use_folder_as_album = False  # Set to False if you want to keep the original album names

# Spotify API credentials
SPOTIPY_CLIENT_ID = '41858acaa4564710a7f3eabbfe5d55fa'
SPOTIPY_CLIENT_SECRET = 'c709c935add54a4096ac4576025f6353'

# Path to your folder containing MP3 files
folder_path = r'C:\Users\anura\Local Documents\GitDevelop\MineYT\downloaded\YT Favorites'

# Initialize Spotipy client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                                          client_secret=SPOTIPY_CLIENT_SECRET))

# Function to clean file names
def clean_filename(filename):
    return re.sub(r'[^A-Za-z0-9 /-]+', '', filename)

# Function to update metadata and album art of MP3 file
def update_metadata_and_album_art(file_path, metadata, album_art_url, use_folder_as_album, folder_name):
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.artist = metadata['artist']
    audiofile.tag.album = folder_name if use_folder_as_album else metadata['album']
    audiofile.tag.title = metadata['title']
    audiofile.tag.genre = metadata['genre']

    # Download album art and attach to the MP3 file
    if album_art_url:
        response = requests.get(album_art_url)
        if response.status_code == 200:
            album_art_data = response.content
            audiofile.tag.images.set(eyed3.id3.frames.ImageFrame.FRONT_COVER, album_art_data, 'image/jpeg')

    audiofile.tag.save()

# Function to rename the file based on the song name, artist, and album
def rename_file(file_path, title, artist, album):
    directory = os.path.dirname(file_path)
    cleaned_title = clean_filename(title)
    cleaned_artist = clean_filename(artist)
    cleaned_album = clean_filename(album)
    new_file_name = f"{cleaned_title} - {cleaned_artist} - {cleaned_album}.mp3"
    new_file_path = os.path.join(directory, new_file_name)
    os.rename(file_path, new_file_path)
    return new_file_path

# Extract the folder name to use as the playlist name
folder_name = os.path.basename(os.path.normpath(folder_path))
playlist_file = os.path.join(folder_path, f'{folder_name}.m3u')

# Open the playlist file for writing
with open(playlist_file, 'w') as playlist:
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3'):
            file_path = os.path.join(folder_path, filename)

            # Clean track name
            track_name = clean_filename(filename)

            # Search track using Spotify API
            results = sp.search(q=track_name, type='track')

            # Extract metadata and album art from Spotify results
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                artist = track['artists'][0]['name']
                album = track['album']['name']
                title = track['name']
                
                # Fetch genres from the artist's information
                artist_id = track['artists'][0]['id']
                artist_info = sp.artist(artist_id)
                genres = artist_info.get('genres', [])
                genre = genres[0] if genres else "Unknown"

                album_art_url = track['album']['images'][0]['url'] if track['album']['images'] else None

                # Update metadata and album art in the MP3 file
                update_metadata_and_album_art(file_path, {'artist': artist, 'album': album, 'title': title, 'genre': genre}, album_art_url, use_folder_as_album, folder_name)

                # Rename the file based on the song name
                # new_file_path = rename_file(file_path, title, artist, album)
                new_file_path = clean_filename(file_path)

                # Write the path to the renamed file to the playlist
                playlist.write(new_file_path + '\n')
                print(f"Updated and renamed file for {filename}: New Name - {title}, Artist - {artist}, Album - {album if not use_folder_as_album else folder_name}, Genre - {genre}")
            else:
                print(f"No metadata found for {filename}")

print(f"Playlist created at {playlist_file}")
