#Data and Model Preprocessing Pharm-Tech doesn’t rely on a dataset in the traditional sense, but it still requires careful input design and prompt engineering to make sure the AI generates relevant and accurate Python code. Since we’re using Together.ai for code generation, most of the preprocessing happens in how the user’s plain-English prompt is formatted before it's sent to the model. 
#To ensure better results, we guide users to phrase their requests clearly and specifically—for example, instead of saying “do PK stuff,” a more effective prompt would be “calculate drug half-life from volume of distribution and clearance.” Internally, the app strips unnecessary whitespace, handles any empty input errors, and passes the cleaned prompt directly to the Together.ai API using a serverless model. 
#Here are a few basic preprocessing steps we included: 
#Stripped leading/trailing whitespace from user input 
#Ensured prompt length doesn't exceed API limits 
#Checked for empty or invalid inputs and returned a warning 
#Removed newline breaks or HTML artifacts that can appear in form text 
#Used consistent temperature and token limits to control output length and creativity 
#This helps make the AI’s output more predictable and relevant to healthcare students who may be unfamiliar with tweaking model parameters. 
#All preprocessing logic is included in the app.py file in the GitHub repo. 

import os
import streamlit as st
from dotenv import load_dotenv
import together

# Load .env variables (for local dev)
load_dotenv()

# Set API key from .env or environment
api_key = os.getenv("TOGETHER_API_KEY")

# Check if the key exists
if not api_key:
    st.error("API key not found. Please set TOGETHER_API_KEY in .env.")
    st.stop()

# Initialize Together.ai client
client = together.Together(api_key=api_key)

# Streamlit UI
st.title("💊 Healthcare Code Generator")
st.write("Describe a healthcare task in plain English and get Python code back!")

prompt = st.text_area("Enter your task (e.g. 'Calculate creatinine clearance...')", height=150)

if st.button("Generate Code"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating code..."):
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You're a helpful Python code generator for healthcare and pharmacy tasks."},
                        {"role": "user", "content": prompt}
                    ],
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    max_tokens=256,
                    temperature=0.7
                )
                generated_code = response.choices[0].message.content
                st.code(generated_code, language="python")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
