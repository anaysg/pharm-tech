import os
import streamlit as st
import together

# Set your API key directly here or through Streamlit secrets/environment
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    st.error("API key not found. Please set TOGETHER_API_KEY as an environment variable or in Streamlit Secrets.")
    st.stop()

# Initialize Together client using the new format
client = together.Together(api_key=TOGETHER_API_KEY)

# Streamlit app layout
st.set_page_config(page_title="Pharma Code Helper", layout="centered")
st.title("💊 Pharma Code Helper")
st.markdown("Describe what you need help with (e.g., *'calculate creatinine clearance using Cockcroft-Gault equation'*)")

# User input prompt
prompt = st.text_area("What do you want Python code for?", height=150, placeholder="Enter your plain-English task here...")

# Button to trigger code generation
if st.button("Generate Code") and prompt.strip():
    with st.spinner("Generating code... please wait ⏳"):
        try:
            response = client.completions.create(
                prompt=prompt,
                model="mistralai/Mistral-7B-Instruct-v0.1",  # ✅ serverless model
                max_tokens=256,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.1,
                stop=["</s>"]
            )
            generated_code = response['output'].strip()
            st.success("Here’s your code:")
            st.code(generated_code, language="python")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
