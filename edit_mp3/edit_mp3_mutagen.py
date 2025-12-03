import os
import logging
import mutagen
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
from mutagen.mp4 import MP4

def print_mp3_attributes(file_path):
    try:
        audio = EasyID3(file_path)
    except ID3NoHeaderError:
        audio = File(file_path, easy=True)
        audio.add_tags()

    logging.info(f"Current MP3 Attributes for {file_path}:")
    for tag in audio.keys():
        logging.info(f"{tag}: {audio[tag][0]}")
        
    return audio

def remove_mp4_tags(file_path):
    try:
        audio = MP4(file_path)
        if audio.tags:
            audio.tags.clear()
            audio.save()
            logging.info(f"Removed existing MP4 tags from {file_path}")
    except Exception as e:
        logging.error(f"Error removing MP4 tags from {file_path}: {e}")

def update_mp3_attributes(file_path, album_art_path=None, **kwargs):
    try:
        # remove_mp4_tags(file_path)  # Remove existing MP4 tags before updating
        audio = print_mp3_attributes(file_path)
        
        # Update attributes based on kwargs
        for key, value in kwargs.items():
            print(key,value)
            audio[key] = value
        
        # Add album art if provided
        if album_art_path:
            audio = ID3(file_path)
            with open(album_art_path, 'rb') as albumart:
                audio['APIC'] = APIC(
                    encoding=3, 
                    mime='image/jpeg', 
                    type=3, 
                    desc=u'Cover',
                    data=albumart.read()
                )
            audio.save()
        else:
            audio.save(v2_version=3)
        
        logging.info(f"Updated MP3 Attributes for {file_path}")
        print_mp3_attributes(file_path)
    except Exception as e:
        logging.error(f"Error updating {file_path}: {e}")

def update_all_files_in_folder(folder_path, album_art_path=None, **kwargs):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            logging.info(f"Processing file: {file_path}")
            update_mp3_attributes(file_path, album_art_path, **kwargs)
            logging.info(f"Finished processing file: {file_path}")
            # break

folder_path = r'C:\Users\anura\Music\Gym Playlist'
album_art_path = r"C:\Users\anura\Downloads\gym_cover.jpg"
attributes_to_update = {
    'album': 'Gym Playlist'
}

logging.basicConfig(
    filemode = 'a',
    filename='mp3_metadata_update.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

update_all_files_in_folder(folder_path, album_art_path, **attributes_to_update)
