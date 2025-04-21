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
