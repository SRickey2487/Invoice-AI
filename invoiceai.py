# !pip install streamlit, google-generativeai, python-dotenv

# IOT use google-generativeai, you need to make sure you have your local development environment set up with your
# google credentials. How to do this is: 1.) install gCloud CLI (https://cloud.google.com/sdk/docs/install),
# 2.) create your credential file using the 'gcloud auth application-default login' command in you terminal.
# This may not be necessary after some more research, but it is what I have done on my system.

from dotenv import load_dotenv # Loads the GOOGLE_API_KEY from .env
from PIL import Image # Python Import Library to import images.

import streamlit as sl
import google.generativeai as genai
import os

# Set up genai
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # Allows GOOGLE_API_KEY to be read into genai while hidden.
model = genai.GenerativeModel(model_name='gemini-pro-vision')

#sl.set_page_config(page_title="MultiLanguage Invoice Extractor") # For some reason this keeps giving an error, so we'll just ignore it because it seems to work well without it.
sl.header("MultiLanguage Purchase Order Analyser")

def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input, image[0], user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded")

input_prompt = sl.text_input("Input Prompt", key='input')
uploaded_file = sl.file_uploader("Provide an image of the invoice", type = ["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    sl.image(image, caption='Uploaded Image', use_column_width=True)

submit = sl.button("Tell me about the invoice")

input_prompt_guide = """
You are an expert at analyzing users purchase orders in any language. We will upload an image of an purchase, and you will be tasked with addressing inquiries related to the content
of the uploaded purchase order. This could include deciphering details such as billing amounts, item descriptions, dates, and any other pertinent information found
within the purchase order. You will apply your proficiency to extract and interpret relevent data accurately from the purchase orders image, enabling us to effectively
address queries and manage invoice-related tasks.You will be a ble to generate a spending report with all of the given purchase orders. 
If the image does not contain any invoice information, respond with Inappropriate Input.
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt_guide, image_data, input_prompt)
    sl.subheader("The purchase order contains the following")
    sl.write(response) 
