from PIL import Image
import pytesseract
import fitz  # PyMuPDF library for working with PDFs

show_image = False
break_early = True

# Path to the input scanned PDF file
pdf_path = 'data/SHAC_Final_Report_3-6-2015.pdf'

# Initialize Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path based on your installation

# Open the PDF file
pdf_document = fitz.open(pdf_path)

text = ""
# Extract text from each page
for page_number in range(pdf_document.page_count):
    page = pdf_document[page_number]
    
    # Convert the page to an image
    image = page.get_pixmap()
    
    # Convert the image to PIL Image
    pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

    # Extract text from the image using Tesseract OCR
    text += f"Text from Page {page_number + 1}\n"
    text += pytesseract.image_to_string(pil_image)

    if show_image:
        # Display the image
        pil_image.show(title=f"Page {page_number + 1}")

        # Print the extracted text
        print(f"Text from Page {page_number + 1}:\n{text}")

        # Close the image display after a short delay (adjust as needed)
        pil_image.close()

    if page_number > 5 and break_early:
        break

# Save or print the extracted text
with open('output_text.txt', 'w', encoding='utf-8') as file:
    file.write(text)

print("Text extraction completed. Check 'output_text.txt' for the result.")
