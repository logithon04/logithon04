# this is the python file for PDF to text conversion
import PyPDF2
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# To extract text from tables in PDF
import pdfplumber
# To extract the images from the PDFs
from PIL import Image
from pdf2image import convert_from_path
# To perform OCR to extract text from images 
import pytesseract 
# To remove the additional created files
import os
# Import PYmuPDF
import fitz 
#importing BART

# Library for formatting text
import textwrap


class Pdf_to_Text:
    def __init__(self , pdf_path):
        self.pdf_path = pdf_path
        
    def extract_text_format(self , element):
        line = element.get_text()
        line_format = []
        for textofline in element:
            if isinstance(line , LTTextContainer):
                for char in textofline :
                    if isinstance(char , LTChar):
                        line_format.append(char.fontname)
                        line_format.append(char.size)
        format_per_line = list(set(line_format))
        
        return (line , format_per_line)
    
        
    def extract_table(self, page_num, table_num):
        # Open the pdf file
        pdf = pdfplumber.open(self.pdf_path)
        # Find the examined page
        table_page = pdf.pages[page_num]
        # Extract the appropriate table
        table = table_page.extract_tables()[table_num]
        return table

# Convert table into the appropriate format
    def table_converter(self , table):
        table_string = ''
        # Iterate through each row of the table
        for row_num in range(len(table)):
            row = table[row_num]
            # Remove the line breaker from the wrapped texts
            cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
            # Convert the table into a string 
            table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
        # Removing the last line break
        table_string = table_string[:-1]
        return table_string

    def crop_image(self , element, pageObj):
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
    def convert_to_images(self , input_file,):
        images = convert_from_path(input_file)
        image = images[0]
        output_file = "PDF_image.png"
        image.save(output_file, "PNG")

# Create a function to read text from images
    def image_to_text(self , image_path):
        # Read the image
        img = Image.open(image_path)
        # Extract the text from the image
        text = pytesseract.image_to_string(img)
        return text
    
    def processpdf(self):
        pdfFileObj = open(self.pdf_path, 'rb')
        # create a PDF reader object
        pdfReaded = PyPDF2.PdfReader(pdfFileObj)
        self.lower_side = 0  # Define lower_side outside of the loop
        self.upper_side = 0  #
        # Create the dictionary to extract text from each image
        text_per_page = {}
        strig  = ""
        # We extract the pages from the PDF
        for pagenum, page in enumerate(extract_pages(self.pdf_path)):
        # Initialize the variables needed for the text extraction from the page
            pageObj = pdfReaded.pages[pagenum]
            page_text = []
            line_format = []
            text_from_images = []
            text_from_tables = []
            page_content = []
            # Initialize the number of the examined tables
            table_num = 0
            first_element= True
            table_extraction_flag= False
            # Open the pdf file
            pdf = pdfplumber.open(self.pdf_path)
            # Find the examined page
            page_tables = pdf.pages[pagenum]
            # Find the number of tables on the page
            tables = page_tables.find_tables()
            # Find all the elements
            page_elements = [(element.y1, element) for element in page._objs]
            # Sort all the elements as they appear in the page 
            page_elements.sort(key=lambda a: a[0], reverse=True)
            # Find the elements that composed a page
            for i,component in enumerate(page_elements):
                # Extract the position of the top side of the element in the PDF
                pos= component[0]
                # Extract the element of the page layout
                element = component[1]
        
        # Check if the element is a text element
                if isinstance(element, LTTextContainer):
                    # Check if the text appeared in a table
                    if table_extraction_flag == False:
                        # Use the function to extract the text and format for each text element
                        (line_text, format_per_line) = self.extract_text_format(element)
                        # Append the text of each line to the page text
                        page_text.append(line_text)
                        # Append the format for each line containing text
                        line_format.append(format_per_line)
                        page_content.append(line_text)
                    else:
                        # Omit the text that appeared in a table
                        pass

                # Check the elements for images
                if isinstance(element, LTFigure):
                    # Crop the image from the PDF
                    self.crop_image(element, pageObj)
                    # Convert the cropped pdf to an image
                    self.convert_to_images('cropped_image.pdf')
                    # Extract the text from the image
                    image_text = self.image_to_text('PDF_image.png')
                    text_from_images.append(image_text)
                    page_content.append(image_text)
                    # Add a placeholder in the text and format lists
                    page_text.append('image')
                    line_format.append('image')

                # Check the elements for tables
                if isinstance(element, LTRect):
                    # If the first rectangular element
                    if first_element == True and (table_num+1) <= len(tables):
                        # Find the bounding box of the table

                        # Extract the information from the table
                        table = self.extract_table(pagenum, table_num)
                        # Convert the table information in structured string format
                        table_string = self.table_converter(table)
                        # Append the table string into a list
                        text_from_tables.append(table_string)
                        page_content.append(table_string)
                        # Set the flag as True to avoid the content again
                        table_extraction_flag = True
                        # Make it another element
                        first_element = False
                        # Add a placeholder in the text and format lists
                        page_text.append('table')
                        line_format.append('table')

                    # Check if we already extracted the tables from the page
                    if element.y0 >= self.lower_side and element.y1 <= self.upper_side:
                        pass
                    elif i < len(page_elements) - 1: 
                        if not isinstance(page_elements[i+1][1], LTRect):
                            table_extraction_flag = False
                            first_element = True
                            table_num+=1


            # Create the key of the dictionary
            dctkey = 'Page_'+ str(pagenum)
            # Add the list of list as the value of the page key
            text_per_page[dctkey] = [page_text, line_format, text_from_images,text_from_tables, page_content]
            strig+= '\n'.join(page_content) + "\n"
    # Closing the pdf file object
        pdfFileObj.close()

        # Deleting the additional files created
        if os.path.exists('cropped_image.pdf'):
            os.remove('cropped_image.pdf')
        if os.path.exists('PDF_image.png'):
            os.remove('PDF_image.png')
        
        result = ''.join(text_per_page['Page_0'][4])
        return strig
