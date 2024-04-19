import streamlit as st
import os
# import tempfile
from pdf_to_text import Pdf_to_Text  # Assuming your PDF processing library

# Constants (customize directory)
UPLOAD_DIR = "uploaded_pdfs"  # Directory to save uploaded PDFs

def save_uploadedfile(uploadedfile):
    """Saves uploaded PDF to the designated directory."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)  # Create directory if it doesn't exist
    filepath = os.path.join(UPLOAD_DIR, uploadedfile.name)
    with open(filepath, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved File: {uploadedfile.name} to {UPLOAD_DIR}")

def summarize_pdf(filepath):
    
    pdf_processor = Pdf_to_Text(filepath)
    text = pdf_processor.processpdf()
    return text

st.title("PDF Summarization")
st.write("This app converts PDFs to summaries (using a placeholder).")

uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file is not None:
        save_uploadedfile(uploaded_file)  # Save the uploaded file permanently
    
        # Summarization logic triggered by button (placeholder)
        if st.button("Summarize"):
            summary = summarize_pdf("/Users/trish/Downloads/ml/ps/Streamlit app/"+UPLOAD_DIR+"/"+uploaded_file.name)
            print(type(summary))
            st.write("Sumarised Text:" , summary)
            # st.success(summary)

