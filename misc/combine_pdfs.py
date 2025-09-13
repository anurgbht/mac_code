import os
from PyPDF2 import PdfMerger, PdfReader

def remove_page_labels(pdf_path):
    reader = PdfReader(pdf_path)
    if "/PageLabels" in reader.trailer["/Root"]:
        del reader.trailer["/Root"]["/PageLabels"]
    return reader

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        reader = remove_page_labels(pdf)
        merger.append(reader)
    merger.write(output_path)
    merger.close()


pdf_file_path = '/Users/anuragbhatt/Downloads/lech2dd'

# Example usage:
pdf_files = sorted([os.path.join(pdf_file_path, f) for f in os.listdir(pdf_file_path) if f.endswith('.pdf')])
print(pdf_files)

output_file = '/Users/anuragbhatt/Downloads/Class 12 Part 2.pdf'

merge_pdfs(pdf_files, output_file)