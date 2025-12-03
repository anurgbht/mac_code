import yt_dlp

def download_single(url: str, path: str):
    """
    Downloads a YouTube video using the yt-dlp library.

    Args:
        url (str): The URL of the YouTube video to download.
        path (str): The file path where the video should be saved.

    Returns:
        None
    """
    # yt-dlp options to specify the output path and filename format
    ydl_opts = {
        'outtmpl': path  # Path where the video will be saved
    }

    # Use yt-dlp to download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
# video_url = "https://www.youtube.com/watch?v=example_video_id"
# save_path = "/path/to/save/video.mp4"
# download_youtube_video(video_url, save_path)

def download_playlist(playlist_url: str, output_path: str, quality: str = '720'):
    """
    Downloads all videos in a YouTube playlist using the yt-dlp library.

    Args:
        playlist_url (str): The URL of the YouTube playlist to download.
        path (str): The directory path where the videos should be saved.
        quality (str): The desired video quality (default is '720p').

    Returns:
        None
    """
    # yt-dlp options to specify the output path, filename format, and video quality
    ydl_opts = {
        'format': f'bestvideo[height<=?{quality}]+bestaudio/best[height<=?{quality}]',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',  # Optional: Set a specific output format if needed
        'postprocessors': [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

def download_playlist_audio(playlist_url: str, path: str, max_duration: int = 20):
    """
    Downloads audio only from all videos in a YouTube playlist using the yt-dlp library,
    filtering out videos longer than the specified maximum duration.

    Args:
        playlist_url (str): The URL of the YouTube playlist to download.
        path (str): The directory path where the audio files should be saved.
        max_duration (int): The maximum duration of videos to download in minutes (default is 20 minutes).

    Returns:
        None
    """
    # yt-dlp options to specify the output path, filename format, audio format, and duration filter
    ydl_opts = {
        'outtmpl': f'{path}/%(title)s.%(ext)s',  # Path where the audio files will be saved
        'format': 'bestaudio/best',  # Download the best available audio quality
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert audio to mp3 format
            'preferredquality': '192',  # Audio quality
        }],
        'match_filter': yt_dlp.utils.match_filter_func(f"duration <= {max_duration * 60}"),
        'ignoreerrors': True
    }

    # Use yt-dlp to download the playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


if __name__ == "__main__":
    PLAYLIST_URL = r"https://www.youtube.com/playlist?list=PLISjr39sa8gqTM0R9HTn9fqKhSFYfIDJD"
    OUTPUT_PATH = r'C:\Users\anura\Music\Best of Gujarati'

    # download_playlist(PLAYLIST_URL, OUTPUT_PATH, "720")
    download_playlist_audio(PLAYLIST_URL, OUTPUT_PATH)
