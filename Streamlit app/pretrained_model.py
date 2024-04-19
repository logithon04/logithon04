# # Python file to use the pretrained BART model 
# from transformers import BartForConditionalGeneration, BartTokenizer
# # Library for formatting text
# import textwrap
# import pathlib
# class Pretrained_Summariser :
#     def __init__(self, model_name="facebook/bart-large-cnn", max_input_length=1024, segment_length=512):
#         self.model = BartForConditionalGeneration.from_pretrained(model_name)
#         self.tokenizer = BartTokenizer.from_pretrained(model_name)
#         self.max_input_length = max_input_length
#         self.segment_length = segment_length

#     def _summarize_segment(self, segment_text):
#         input_ids = self.tokenizer.encode(segment_text, return_tensors="pt", max_length=self.segment_length, truncation=True)
#         summary_ids = self.model.generate(input_ids, max_length=5000, min_length=500, length_penalty=3.0, num_beams=4, early_stopping=True)
#         summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#         return summary

#     def summarize_from_pdf(self, pdf_text):
#         if len(pdf_text) <= self.max_input_length:
#             # If input text is within max length, summarize directly
#             return self._summarize_segment(pdf_text)
#         else:
#             # Truncate input text into segments and summarize each segment
#             segments = [pdf_text[i:i+self.segment_length] for i in range(0, len(pdf_text), self.segment_length)]
#             summaries = [self._summarize_segment(segment) for segment in segments]
#             combined_summary = "\n".join(summaries)
#             return combined_summary

from pdf_to_text import Pdf_to_Text  # Assuming your PDF processing library

def summarize_pdf(filepath):
    
    pdf_processor = Pdf_to_Text(filepath)
    text = pdf_processor.processpdf()
    return text

UPLOAD_DIR = "Streamlit app/uploaded_pdfs/Copy of Expt No 1.pdf" 
summary = summarize_pdf(filepath=UPLOAD_DIR)
print(summary)
                                    