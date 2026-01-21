import os
from pathlib import Path

print('Hello world.')

SRC_DIR = Path(r"/home/anurag/Videos/Ergo Proxy")

#Ergo Proxy 23.mkv
start_with = ""
end_with = ""
sep = " "

replace_these = {
    "Ergo Proxy Ergo Proxy   ": "Ergo Proxy "
    }

for fpath in SRC_DIR.glob("*"):
    print(fpath)
    if start_with:
        new_name = start_with + sep + fpath.name
    else:
        new_name = fpath.name

    for replace_phrase, replace_with in replace_these.items():
        new_name = new_name.replace(replace_phrase, replace_with)
    if end_with:
        new_name += sep
        new_name += end_with
    os.rename(fpath, Path(SRC_DIR, new_name))


## rename PDF files in a directory

PDF_DIR = Path(r'/Users/anuragbhatt/Documents/.AHA/Savita Bhabhi')


# vdoc.pub_savita-bhabhi-ep-01-bra-salesman-hindi.pdf
for fpath in PDF_DIR.glob("*.pdf"):
    new_name = fpath.stem.replace("vdoc.pub_", "").replace("savita-bhabhi-", "Savita Bhabhi - ").replace("ep-", "Episode ").replace("hindi", "Hindi").replace("-", " ").replace("   ", " - ") + fpath.suffix
    new_name = ' '.join(word.capitalize() for word in new_name.split())
    print(new_name)
    os.rename(fpath, Path(PDF_DIR, new_name))