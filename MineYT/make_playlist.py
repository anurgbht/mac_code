import os
import eyed3
import re

# Function to clean file names
def clean_filename(filename):
    return re.sub(r'[^A-Za-z0-9 ]+', '', filename)

# Function to rename the file based on its metadata
def rename_file_with_metadata(file_path, use_folder_as_album, folder_name):
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()
    
    artist = audiofile.tag.artist if audiofile.tag.artist else "Unknown Artist"
    album = audiofile.tag.album if audiofile.tag.album else "Unknown Album"
    title = audiofile.tag.title if audiofile.tag.title else "Unknown Title"

    # Use folder name as album if flag is set
    album = folder_name if use_folder_as_album else album
    
    cleaned_title = clean_filename(title)
    cleaned_artist = clean_filename(artist)
    cleaned_album = clean_filename(album)
    
    new_file_name = f"{cleaned_title} - {cleaned_artist} - {cleaned_album}.mp3"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    
    os.rename(file_path, new_file_path)
    return new_file_path

# Function to create a playlist from all MP3 files in a folder
def create_playlist_from_folder(folder_path, use_folder_as_album):
    folder_name = os.path.basename(os.path.normpath(folder_path))
    playlist_file = os.path.join(folder_path, f'{folder_name}.m3u')

    with open(playlist_file, 'w') as playlist:
        for filename in os.listdir(folder_path):
            if filename.endswith('.mp3'):
                file_path = os.path.join(folder_path, filename)
                new_file_path = rename_file_with_metadata(file_path, use_folder_as_album, folder_name)
                playlist.write(new_file_path + '\n')
                print(f"Renamed and added to playlist: {new_file_path}")

    print(f"Playlist created at {playlist_file}")

# Path to your folder containing MP3 files
folder_path = r"C:\Users\anura\Music\test"

# Flag to use folder name as album name
use_folder_as_album = True  # Set to False if you want to keep the original album names

# Create playlist from all MP3 files in the folder
create_playlist_from_folder(folder_path, use_folder_as_album)
