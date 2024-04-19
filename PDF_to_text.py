import os 
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

def crop_image(element, pageObj):
    # Get the coordinates to crop the image from the PDF
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1] 
    # Crop the page using coordinates (left, bottom, right, top)
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    # Save the cropped page to a new PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    # Save the cropped PDF to a new file
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Create a function to convert the PDF to images
def convert_to_images(input_file,):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = "PDF_image.png"
    image.save(output_file, "PNG")

# Create a function to read text from images
def image_to_text(image_path):
    # Read the image
    img = Image.open(image_path)
    # Extract the text from the image
    text = pytesseract.image_to_string(img)
    return text

def convert_pdfs_to_text(input_folder, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            # Get the full path of the input PDF file
            input_pdf_path = os.path.join(input_folder, filename)
            
            # Convert PDF to image
            convert_to_images(input_pdf_path)
            
            # Get the path of the generated image
            image_path = "PDF_image.png"
            
            # Convert image to text
            text = image_to_text(image_path)
            
            # Get the name of the text file (same as PDF but with .txt extension)
            text_filename = os.path.splitext(filename)[0] + ".txt"
            
            # Get the full path of the output text file
            output_text_path = os.path.join(output_folder, text_filename)
            
            # Save the text to the output text file
            with open(output_text_path, 'w') as text_file:
                text_file.write(text)
                
            # Remove the temporary image file
            os.remove(image_path)

# Example usage:
input_folder = "/Users/trish/Downloads/1000+ PDF_Invoice_Folder"
output_folder = "/Users/trish/Downloads/output_texts"
convert_pdfs_to_text(input_folder, output_folder)

