from dotenv import load_dotenv
from PIL import Image
import os
import google.generativeai as genai
import streamlit as st

load_dotenv()

key=os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=key)

# for model in genai.list_models():
#     if 'generateContent' in model.supported_generation_methods:
#         print(model.name)

model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input, image[0], user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                'mime_type':uploaded_file.type,
                'data':bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')

st.set_page_config(page_title='KartVision')

st.header('KartVision - Data Extraction')
input=st.text_input('Input questions about the image:', key='input')
uploaded_file=st.file_uploader('Choose an image:', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button('Get Response')

input_prompt="""
You are an expert in smart vision technology, tasked with revolutionizing quality testing for a major e-commerce company in India. You will receive input images of various products, packaging, and fresh produce. Your goal is to analyze these images to assess shipment quality, quantity, and identify any defects. Provide insights, classify products, and offer feedback based on the visual information presented in the images.
"""

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt, image_data, input)
    st.subheader('The Response is')
    st.write(response)