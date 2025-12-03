from pathlib import Path
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


def edit_NLHafta(count):
    fpath = Path(r"C:\Users\anura\Downloads\Podcasts\NL Hafta")
    album_art = Path(r"C:\Users\anura\Pictures\Screenshot 2021-08-19 230720.png")
    artist_name = "NL Team"
    album = "NL Hafta"
    edit_basic(fpath, album_art, artist_name, album, count)


def edit_random():
    fpath = Path(r"C:\Users\anura\Downloads\Podcasts\Random Talks")
    album_art = Path(r"C:\Users\anura\Pictures\Screenshot 2021-10-04 202104.png")
    artist_name = "Various Artists"
    album = "Random Talks"
    edit_basic(fpath, album_art, artist_name, album, 1)


def clear_meta(meta_dict):
    for key in meta_dict.keys():
        meta_dict[key] = ""
    return meta_dict


def edit_basic(fpath, album_art, artist_name, album, count):
    for fname in fpath.iterdir():
        print(fname)
        try:
            meta = EasyID3(fname)
            # meta = clear_meta(meta)
        except mutagen.id3.ID3NoHeaderError:
            meta = mutagen.File(fname, easy=True)
            meta.add_tags()
        replace_phrase = "Yt1s.com - "
        meta["title"] = (
            fname.name.lstrip("0123456789. _-")
            .lower()
            .capitalize()
            .replace(".mp3", "")
            .replace(replace_phrase, "")
            .replace("_", " ")
            .rstrip(". _-")
        )
        if artist_name:
            meta["artist"] = artist_name
        meta["album"] = album
        meta["tracknumber"] = str(count)
        count += 1
        print(meta)
        meta.save(fname, v1=2)

        # add album art
        audio = MP3(fname, ID3=ID3)

        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime="image/png",  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc="Cover",
                data=open(str(album_art), "rb").read(),
            )
        )
        audio.save()


def edit_only_album(fpath, album, artist_name=""):
    count = 1
    for fname in fpath.iterdir():
        print(fname)
        try:
            meta = EasyID3(fname)
        except mutagen.id3.ID3NoHeaderError:
            meta = mutagen.File(fname, easy=True)
            meta.add_tags()

        if artist_name:
            # meta["artist"] = artist_name
            meta["albumartist"] = artist_name
        else:
            # meta["artist"] = "Various Artists"
            meta["albumartist"] = "Various Artists"

        meta["album"] = album
        meta["tracknumber"] = str(count)
        count += 1
        print(meta)
        meta.save(fname, v1=2)

        # add album art
        audio = MP3(fname, ID3=ID3)
        audio.save()


def edit_folder():
    edit_all = 0
    fpath = Path(
        r"C:\Users\User\Documents\GitDevelop\MineSpotify\Downloaded\Spotify Public"
    )

    if edit_all:
        album_art = Path(
            r"C:\Users\User\Downloads\Album arts\924faf52097223.590463d34792e.jpg"
        )
        artist_name = "Various Artists"
        album = "YouTube Public"
        count = 1
        edit_basic(fpath, album_art, artist_name, album, count)
    else:
        album = fpath.name
        edit_only_album(fpath, album)


if __name__ == "__main__":
    # edit_NLHafta(346)
    edit_folder()
    # edit_random()
