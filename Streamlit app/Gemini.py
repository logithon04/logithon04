#importing import libraries  
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
import json
import re 
#setting the enviroment of the google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyA5S1Zuux8FG1JP1eS9Gw8QXQdH_F_lYzI"
# Congiuguring the API key with the environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#loading the API 
model = genai.GenerativeModel('gemini-pro')

class Gemini:
    def __init__(self , texts):
        self.text = texts
        self.input1 = "YOU are an Self Learning AI assistant who extracts the data and fires it in form of JSON"
        self.pattern = r'[^\x20-\x7E\\]'
    
    def get_text_chunks(self , text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        return chunks

    def get_vector_store(self , text_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    
    def get_gemini_responses(self , input, pdf_content, prompt):
        response = model.generate_content([input, pdf_content, prompt])
        return response.text
    
    def get_conversational_chain(self):
        prompt_template = """
        Answer the question as detailed as possible from the provided document given to you , try to give answer in as much precisely as you can
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """

        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        return chain
    
    def user_input(self , user_question):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        new_db = FAISS.load_local("faiss_index", embeddings ,allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)

        chain = self.get_conversational_chain()

        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True)

        return response["output_text"]

    def response_generator(self , user_question):
        response = self.user_input(user_question)
        for word in response.split():
            yield word + " "
    def to_json(self , text ):
        json_file = self.get_gemini_responses(self.input1 , text , "please convert this into a json format strting with { and ending with }")
        json_file =  re.sub(self.pattern, '', json_file)
        json_file = json_file.encode('utf-8').decode('utf-8-sig')
        response_dict = {"Data": json_file}
        json_response = json.dumps(response_dict)
        return json_response
        
        
        
        
        