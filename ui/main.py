import json
from PyPDF2 import PdfReader

def extract_data_from_pdf(pdf_path):
    data = []
    with open(pdf_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page in pdf_reader.pages:
            text = page.extract_text()
            # Parse text to extract relevant information
            # For demonstration purposes, let's assume we are extracting lines containing 'Name' and 'Age'
            lines = text.split('\n')
            for line in lines:
                if 'Name' in line:
                    name = line.split(':')[-1].strip()
                elif 'Age' in line:
                    age = line.split(':')[-1].strip()
                    data.append({'Name': name, 'Age': age})
    return data

def save_to_json(data, json_path):
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    pdf_path = 'example.pdf'  # Path to your PDF file
    json_path = 'output.json' # Path to save the output JSON file

    # Extract data from PDF
    extracted_data = extract_data_from_pdf(pdf_path)

    # Convert extracted data to JSON and save
    save_to_json(extracted_data, json_path)
    print("Data extracted and saved to JSON successfully!")

if __name__ == "__main__":
    main()
