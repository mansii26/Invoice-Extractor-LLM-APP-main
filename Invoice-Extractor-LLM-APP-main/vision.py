# Q&A Chatbot
#from langchain.llms import OpenAI

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get respones

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Size Identifier")




uploaded_file = st.file_uploader("Select your floor plan", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

input=st.text_input("Ask your question ",key="input")
submit=st.button("Get Answer ")    




input_prompt = """
              You are an expert in analyzing architectural floor plans. You will receive images of floor plans and identify the following elements:

* Walls: Look for lines that define the boundaries of rooms.
* Doors: Identify rectangular shapes connected to walls that likely represent doors.
* Windows: Find rectangular shapes within walls that might be windows.

Based on the identified walls, you will calculate the area of each enclosed space, considering it as a room. 

When a user asks a question about a specific room, use the following information to answer:

* Identify the room based on its location or any labels (e.g., "living room", "bedroom"). 
* If no label exists, describe the room's location (e.g., "room on the left side of the entrance").
* When asked for the area, provide the calculated square footage based on the wall dimensions.

If the floor plan is unclear or lacks information, inform the user about the limitations and suggest possible clarifications. 
               """

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)



def footer():
  """Creates a footer component with the text"""
  st.write('<p style="text-align: center; font-size: 12px;">Developed by RajYug Solutions Ltd.</p>', unsafe_allow_html=True)

# Your Streamlit app code...

# Call the footer function at the end
footer()

