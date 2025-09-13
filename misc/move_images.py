import os, re, json
import subprocess
import shutil
from datetime import datetime
import logging
from dateutil import parser
from collections import defaultdict

date_source_counts = defaultdict(int)
folder_counts = defaultdict(int)

# Setup logger
logging.basicConfig(
    filename="photo_sort.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------- CONFIG --------
source_dir = "/Volumes/Bhatt T7/Photos/My Pics"
target_dir = "/Volumes/Bhatt T7/Photos/Organized"
valid_extensions = {".jpg", ".jpeg", ".png", ".heic", ".tiff", ".mov", ".mp4"}

# -------- FUNCTIONS --------

def get_json_date(filepath):
    candidates = [
        filepath + ".suppl.json",
        filepath + ".supplemental-metadata.json"
    ]

    for json_path in candidates:
        if not os.path.exists(json_path):
            continue

        try:
            with open(json_path, "r") as f:
                data = json.load(f)
                date_str = data.get("photoTakenTime", {}).get("formatted")
                if date_str:
                    try:
                        dt = parser.parse(date_str)
                        logging.info(f"Using supplemental metadata from {os.path.basename(json_path)}: {date_str}")
                        return dt
                    except Exception as e:
                        logging.warning(f"Could not parse date from {json_path}: {e}")
        except Exception as e:
            logging.warning(f"Could not read {json_path}: {e}")

    return None

def extract_date_from_filename(filename):
    match = re.search(r"(19|20)\d{6}", filename)
    if match:
        try:
            date = datetime.strptime(match.group(), "%Y%m%d")
            logging.info(f"Filename date extracted: {date} from {filename}")
            return date
        except Exception as e:
            logging.warning(f"Filename date parse failed for {filename}: {e}")
    return None

def get_best_date(filepath):
    filename = os.path.basename(filepath)
    source = "none"

    # 0. Suppl.json override
    json_date = get_json_date(filepath)
    if json_date:
        return json_date, "suppl.json"

    exif_date = get_exif_date(filepath)
    filename_date = extract_date_from_filename(filename)

    if exif_date and filename_date:
        if filename_date.year >= 2005 and filename_date > exif_date:
            logging.info(f"Using filename date over EXIF for {filename} ({filename_date} > {exif_date})")
            return filename_date, "filename > exif"
        logging.info(f"Using EXIF date for {filename}")
        return exif_date, "exif"

    if exif_date:
        logging.info(f"Using EXIF date for {filename}")
        return exif_date, "exif"

    if filename_date:
        logging.info(f"Using filename date for {filename}")
        return filename_date, "filename"


    # Folder name fallback
    folder_path = os.path.dirname(filepath)
    match = re.search(r"\b(19|20)\d{2}\b", folder_path)
    if match:
        year = int(match.group())
        logging.info(f"Using folder name year {year} for {filename}")
        return datetime(year, 1, 1), "folder_name"
    
    # Fallback to filesystem date
    try:
        stat = os.stat(filepath)
        fs_date = datetime.fromtimestamp(
            stat.st_birthtime if hasattr(stat, "st_birthtime") else stat.st_mtime
        )
        logging.info(f"Using filesystem date for {filename}")
        return fs_date, "filesystem"
    except Exception as e:
        logging.warning(f"Filesystem date failed for {filename}: {e}")

    logging.warning(f"Could not determine date for {filename}")
    return None, "unknown"

def is_media_file(filename):
    return os.path.splitext(filename)[1].lower() in valid_extensions

def get_exif_date(filepath):
    try:
        result = subprocess.run(
            ["exiftool", "-MediaCreateDate", "-CreateDate", "-s3", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        date_lines = result.stdout.strip().splitlines()
        for date_str in date_lines:
            date_str = date_str.strip()
            if not date_str:
                continue
            try:
                # First try standard EXIF format
                return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            except:
                try:
                    # Try ISO QuickTime-style format
                    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
                except Exception as e:
                    logging.warning(f"Couldn't parse video date line '{date_str}' for {filepath}: {e}")
        logging.warning(f"No usable date found for {filepath}")
    except Exception as e:
        logging.error(f"EXIF read failed for {filepath}: {e}")
    return None

# -------- MAIN --------
moved_one = False

for root, _, files in os.walk(source_dir):
    for file in files:
        if not is_media_file(file):
            continue

        full_path = os.path.join(root, file)
        date_taken, source = get_best_date(full_path)
        date_source_counts[source] += 1

        if date_taken:
            year = str(date_taken.year)
            month = f"{date_taken.month:02d}" if date_taken.month != 0 else "unknown"
        else:
            year = "unknown"
            month = "unknown"

        folder_key = f"{year}/{month}"
        folder_counts[folder_key] += 1

        if date_taken:
            year = str(date_taken.year)
            month = f"{date_taken.month:02d}" if date_taken.month != 0 else "unknown"
        else:
            year = "unknown"
            month = "unknown"

        dest_folder = os.path.join(target_dir, year, month)
        os.makedirs(dest_folder, exist_ok=True)

        # Create non-conflicting destination filename
        dest_path = os.path.join(dest_folder, file)

        # Move file
        try:
            shutil.move(full_path, dest_path)
            logging.info(f"Moved: {full_path} → {dest_path} | Source: {source}")
        except Exception as e:
            logging.error(f"Failed to move {full_path} → {dest_path}: {e}")

print("\n📦 Organizing Summary:")
print("------------------------")
print("Files organized by folder:")

for folder, count in sorted(folder_counts.items()):
    print(f"  {folder}: {count} file(s)")

print("\n🔍 Parsing methods used:")
for method, count in date_source_counts.items():
    print(f"  {method}: {count} file(s)")