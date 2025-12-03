import logging
import os
import shutil
import py7zr

my_pass = '5Rq32))&'
fin_7z_path = "/home/anurag/Documents/temp_test.7z"
fin_extract_path = "/home/anurag/Documents/temp_test_extracted"

logging.basicConfig(level=logging.DEBUG)

logging.debug('Extracting 7z file')
with py7zr.SevenZipFile(fin_7z_path, mode='r', password=my_pass) as z:
    z.extractall(fin_extract_path)

logging.debug('Removed original 7z file')
os.remove(fin_7z_path)

## do all the processing of data here
logging.debug('Processing information')

logging.debug('Compressing to new 7z file')
## compress the folder in an encrypted archive again
with py7zr.SevenZipFile(fin_7z_path, 'w', password=my_pass) as archive:
    archive.writeall(fin_extract_path, 'base')

logging.debug('Removing extracted folder. Only archive remains')
shutil.rmtree(fin_extract_path)