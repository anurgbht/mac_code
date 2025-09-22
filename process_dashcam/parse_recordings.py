#!/usr/bin/env python3
"""
Dashcam Video Concatenator

This script reads MP4 files from dashcam recordings organized by day folders
and concatenates them into a single video file per day.
"""

import os
import re
import subprocess
import glob
from pathlib import Path
from typing import List, Tuple


def get_mp4_files_from_day_folder(day_folder: Path) -> List[Path]:
    """Get all MP4 files from a day folder, sorted by timestamp."""
    mp4_files = list(day_folder.glob("*.mp4"))
    
    # Sort by timestamp in filename (H_VIDEO_YYYYMMDDHHMMSS_timestamp.mp4)
    def extract_timestamp(filepath: Path) -> int:
        # Extract the timestamp from filename
        match = re.search(r'_(\d+)\.mp4$', filepath.name)
        if match:
            return int(match.group(1))
        return 0
    
    mp4_files.sort(key=extract_timestamp)
    return mp4_files


def create_concat_file(mp4_files: List[Path], concat_file_path: Path) -> None:
    """Create a concat file for ffmpeg with all MP4 files."""
    with open(concat_file_path, 'w') as f:
        for mp4_file in mp4_files:
            # Use relative path from concat file location
            relative_path = mp4_file.relative_to(concat_file_path.parent)
            f.write(f"file '{relative_path}'\n")


def concatenate_videos(day_folder: Path, output_file: Path) -> bool:
    """Concatenate all MP4 files in a day folder into a single video."""
    mp4_files = get_mp4_files_from_day_folder(day_folder)
    
    if not mp4_files:
        print(f"No MP4 files found in {day_folder}")
        return False
    
    print(f"Found {len(mp4_files)} MP4 files in {day_folder.name}")
    
    # Create a temporary concat file
    concat_file = day_folder / "concat_list.txt"
    
    try:
        create_concat_file(mp4_files, concat_file)
        
        # Use ffmpeg to concatenate videos
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-c', 'copy',  # Copy streams without re-encoding for speed
            '-y',  # Overwrite output file if it exists
            str(output_file)
        ]
        
        print(f"Concatenating videos for {day_folder.name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully created: {output_file}")
            return True
        else:
            print(f"Error concatenating videos: {result.stderr}")
            return False
            
    finally:
        # Clean up temporary concat file
        if concat_file.exists():
            concat_file.unlink()


def process_all_days(recordings_dir: Path, output_dir: Path) -> None:
    """Process all day folders in the recordings directory."""
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Find all day folders (folders that contain MP4 files)
    day_folders = []
    for item in recordings_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if this folder contains MP4 files
            if list(item.glob("*.mp4")):
                day_folders.append(item)
    
    if not day_folders:
        print("No day folders with MP4 files found in recordings directory")
        return
    
    print(f"Found {len(day_folders)} day folders to process")
    
    for day_folder in day_folders:
        print(f"\nProcessing {day_folder.name}...")
        
        # Create output filename
        output_file = output_dir / f"{day_folder.name}_concatenated.mp4"
        
        # Skip if output file already exists
        if output_file.exists():
            print(f"Output file already exists: {output_file}")
            continue
        
        success = concatenate_videos(day_folder, output_file)
        if success:
            print(f"✓ Completed: {day_folder.name}")
        else:
            print(f"✗ Failed: {day_folder.name}")


def main():
    """Main function to process dashcam recordings."""
    # Define paths
    recordings_dir = Path("/Users/anuragbhatt/Movies/Dashcam/Recordings")
    output_dir = Path("/Users/anuragbhatt/Movies/Dashcam/Concatenated")
    
    if not recordings_dir.exists():
        print(f"Recordings directory not found: {recordings_dir}")
        return
    
    print("Dashcam Video Concatenator")
    print("=" * 30)
    print(f"Recordings directory: {recordings_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is not installed or not available in PATH")
        print("Please install ffmpeg to use this script")
        return
    
    # Process all day folders
    process_all_days(recordings_dir, output_dir)
    
    print("\nProcessing complete!")


if __name__ == "__main__":
    main()
