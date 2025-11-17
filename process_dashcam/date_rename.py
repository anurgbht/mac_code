import re
import argparse
from pathlib import Path
from datetime import datetime, date
from typing import Optional

## original file naming example: 01-Nov-2025_concatenated.mp4

# Default path - change with --path when running the script
file_path = Path('/Volumes/Bhatt T7/Videos/Dashcam/Concatenated')

DATE_RE = re.compile(r'(?P<day>\d{1,2})-(?P<mon>[A-Za-z]{3,9})-(?P<year>\d{4})')


def parse_date_from_text(text: str) -> Optional[date]:
	"""Try to extract a date from `text` like '01-Nov-2025' or '1-November-2025'.

	Returns a datetime.date on success or None.
	"""
	m = DATE_RE.search(text)
	if not m:
		return None
	day = m.group('day')
	mon = m.group('mon')
	year = m.group('year')
	date_str = f"{day}-{mon}-{year}"
	# Try abbreviated month first, then full month name
	for fmt in ("%d-%b-%Y", "%d-%B-%Y"):
		try:
			return datetime.strptime(date_str, fmt).date()
		except ValueError:
			continue
	return None


def find_files(path: Path, ext: str):
	return sorted(p for p in path.glob(f'*.{ext}') if p.is_file())


def main():
	parser = argparse.ArgumentParser(description="Rename dashcam files from D-Mon-YYYY_... to YYYY-MM-DD.ext")
	parser.add_argument('--path', '-p', type=Path, default=file_path, help='Directory containing files')
	parser.add_argument('--ext', '-e', default='mp4', help='File extension to process (default: mp4)')
	parser.add_argument('--apply', action='store_true', help='Actually perform renames. Without this flag the script does a dry-run.')
	parser.add_argument('--yes', '-y', action='store_true', help='When --apply, skip confirmations and overwrite checks (still will not overwrite existing files)')
	args = parser.parse_args()

	path: Path = args.path
	if not path.exists() or not path.is_dir():
		print(f"Path does not exist or is not a directory: {path}")
		return 2

	files = find_files(path, args.ext)
	if not files:
		print(f"No .{args.ext} files found in {path}")
		return 0

	proposed = []
	for f in files:
		dt = parse_date_from_text(f.stem)
		if dt is None:
			# skip files we can't parse
			continue
		new_name = f"{dt.isoformat()}{f.suffix.lower()}"
		new_path = f.with_name(new_name)
		proposed.append((f, new_path))

	if not proposed:
		print('No files matched the expected date pattern.')
		return 0

	print('Proposed renames:')
	for src, dst in proposed:
		print(f'  {src.name} -> {dst.name}')

	if not args.apply:
		print('\nDry run complete. To perform the renames re-run with --apply')
		return 0

	# Apply renames with safety checks
	applied = 0
	skipped = 0
	for src, dst in proposed:
		if dst.exists():
			print(f"Skipping '{src.name}': target '{dst.name}' already exists")
			skipped += 1
			continue
		try:
			src.rename(dst)
			print(f"Renamed: {src.name} -> {dst.name}")
			applied += 1
		except Exception as exc:
			print(f"Failed to rename {src.name}: {exc}")
			skipped += 1

	print(f"\nDone. Applied: {applied}, Skipped/Failed: {skipped}")
	return 0


if __name__ == '__main__':
	raise SystemExit(main())

