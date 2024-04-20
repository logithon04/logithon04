import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

from pdf_to_text import Pdf_to_Text
from Gemini import Gemini
import base64



global json_response
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Click here to download {file_label}</a>'
    return href
def download_json_file(data):
  """
  Downloads the JSON data as a file.
  """
  json_str = json.dumps(data, indent=4)
  b64 = base64.b64encode(json_str.encode()).decode()
  href = f'<a href="data:application/json;base64,{b64}" download="invoice.json">Download JSON</a>'
  st.write(href, unsafe_allow_html=True)
  
# Constants
UPLOAD_DIR = "uploaded_pdfs"
textas = None

# Function to save uploaded PDF file
def save_uploadedfile(uploadedfile):
    """Saves uploaded PDF to the designated directory."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    filepath = os.path.join(UPLOAD_DIR, uploadedfile.name)
    with open(filepath, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return filepath

# Function to extract text from PDF
def text_from_pdf(filepath):
    pdf_processor = Pdf_to_Text(filepath)
    return pdf_processor.processpdf()

# Function to save JSON data to file
def save_json_to_file(json_data, filename):
    with open(filename, "w") as json_file:
        json_file.write(json_data)

# Streamlit app
st.set_page_config(page_title="Json Gun", page_icon=r"logo.png", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.header(":Purple[PDF] to Data")
st.title("Pdf to Data Convertor")
st.write("This app converts PDFs to Data points to a downloadable format")

uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file is not None:

    filepath = save_uploadedfile(uploaded_file)  # Save the uploaded file permanently

    # Check session state for download readiness
    if 'download_ready' not in st.session_state:
        st.session_state['download_ready'] = False
        st.session_state['extracted_data'] = None
        # st.json(json_response)
    # Summarization logic triggered by button
    if st.button("Data Extract"):
        try:
            textas = text_from_pdf(filepath)
            gemini_instance = Gemini(textas)

            json_response = gemini_instance.to_json(textas)
            # Update session state with data and download flag
            st.session_state['download_ready'] = True
            st.session_state['extracted_data'] = json_response
            
            st.json(json_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Display download button only if data is ready
    if st.session_state['download_ready']:
        st.download_button(
            label="Download JSON",
            key="download_json_button",
            file_name="data.json",
            mime="application/json",
            data=st.session_state['extracted_data'],)
        
    else :
        st.write("Upload a pdf file")


    with st.sidebar:
        
        textas = text_from_pdf(filepath)

        gemini_instance = Gemini(textas)
        # Process the PDF file automatically
        text_chunks = gemini_instance.get_text_chunks(textas)
        gemini_instance.get_vector_store(text_chunks)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        if prompt := st.chat_input("Chat wiht me "):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                response = st.write_stream(gemini_instance.response_generator(prompt))
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
