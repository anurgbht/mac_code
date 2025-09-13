#!/usr/bin/env python3
"""
Timelapse Video Creator

This script reads JPEG images from timelapse folders and creates MP4 timelapse videos.
"""

import os
import re
import subprocess
import glob
from pathlib import Path
from typing import List, Tuple


def get_jpeg_files_from_folder(folder: Path) -> List[Path]:
    """Get all JPEG files from a folder, sorted by timestamp."""
    jpeg_files = list(folder.glob("*.jpeg")) + list(folder.glob("*.jpg"))
    
    # Sort by timestamp in filename (timelapse_timestamp.jpeg)
    def extract_timestamp(filepath: Path) -> int:
        # Extract the timestamp from filename
        match = re.search(r'timelapse_(\d+)\.jpe?g$', filepath.name)
        if match:
            return int(match.group(1))
        return 0
    
    jpeg_files.sort(key=extract_timestamp)
    return jpeg_files


def create_timelapse_video(image_folder: Path, output_file: Path, fps: int = 10) -> bool:
    """Create a timelapse video from JPEG images in a folder."""
    jpeg_files = get_jpeg_files_from_folder(image_folder)
    
    if not jpeg_files:
        print(f"No JPEG files found in {image_folder}")
        return False
    
    print(f"Found {len(jpeg_files)} JPEG files in {image_folder.name}")
    
    # Create a concat file for ffmpeg with all JPEG files
    concat_file = image_folder / "concat_list.txt"
    
    try:
        with open(concat_file, 'w') as f:
            for jpeg_file in jpeg_files:
                # Use relative path from concat file location
                relative_path = jpeg_file.relative_to(concat_file.parent)
                f.write(f"file '{relative_path}'\n")
                f.write(f"duration {1/fps}\n")  # Duration for each frame
        
        # Use ffmpeg to create timelapse video
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_file),
            '-vsync', 'vfr',  # Variable frame rate
            '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
            '-c:v', 'libx264',  # Video codec
            '-crf', '23',  # Quality setting (lower = better quality)
            '-y',  # Overwrite output file if it exists
            str(output_file)
        ]
        
        print(f"Creating timelapse video for {image_folder.name} at {fps} fps...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully created: {output_file}")
            return True
        else:
            print(f"Error creating timelapse video: {result.stderr}")
            return False
            
    finally:
        # Clean up temporary concat file
        if concat_file.exists():
            concat_file.unlink()


def find_image_folders(timelapse_dir: Path) -> List[Path]:
    """Find all folders that contain JPEG images."""
    image_folders = []
    
    def scan_directory(directory: Path):
        """Recursively scan directory for folders with JPEG images."""
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if this folder contains JPEG files
                jpeg_files = list(item.glob("*.jpeg")) + list(item.glob("*.jpg"))
                if jpeg_files:
                    image_folders.append(item)
                else:
                    # Recursively check subdirectories
                    scan_directory(item)
    
    scan_directory(timelapse_dir)
    return image_folders


def process_all_timelapses(timelapse_dir: Path, output_dir: Path, fps: int = 10) -> None:
    """Process all image folders in the timelapse directory."""
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Find all folders with JPEG images
    image_folders = find_image_folders(timelapse_dir)
    
    if not image_folders:
        print("No folders with JPEG images found in timelapse directory")
        return
    
    print(f"Found {len(image_folders)} folders with JPEG images to process")
    
    for image_folder in image_folders:
        print(f"\nProcessing {image_folder.name}...")
        
        # Create output filename based on folder path
        # Replace path separators with underscores
        relative_path = image_folder.relative_to(timelapse_dir)
        output_filename = str(relative_path).replace('/', '_').replace('\\', '_') + "_timelapse.mp4"
        output_file = output_dir / output_filename
        
        # Skip if output file already exists
        if output_file.exists():
            print(f"Output file already exists: {output_file}")
            continue
        
        success = create_timelapse_video(image_folder, output_file, fps)
        if success:
            print(f"✓ Completed: {image_folder.name}")
        else:
            print(f"✗ Failed: {image_folder.name}")


def main():
    """Main function to process timelapse images."""
    # Define paths
    timelapse_dir = Path("Timelapse")
    output_dir = Path("Timelapse_Videos")
    
    if not timelapse_dir.exists():
        print(f"Timelapse directory not found: {timelapse_dir}")
        return
    
    print("Timelapse Video Creator")
    print("=" * 30)
    print(f"Timelapse directory: {timelapse_dir}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is not installed or not available in PATH")
        print("Please install ffmpeg to use this script")
        return
    
    # Process all image folders
    process_all_timelapses(timelapse_dir, output_dir, fps=10)
    
    print("\nProcessing complete!")


if __name__ == "__main__":
    main()
