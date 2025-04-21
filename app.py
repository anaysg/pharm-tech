import os
import streamlit as st
import together

# Set API key (set this in Streamlit Secrets or env vars)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    st.error("API key not found. Please set TOGETHER_API_KEY as an environment variable or in Streamlit Secrets.")
    st.stop()

# Initialize Together client
client = together.Together(api_key=TOGETHER_API_KEY)

# Streamlit UI setup
st.set_page_config(page_title="Pharma Code Helper", layout="centered")
st.title("💊 Pharma Code Helper")
st.markdown("Describe your task (e.g., *'calculate creatinine clearance using Cockcroft-Gault equation'*)")

# User prompt
prompt = st.text_area("What do you want Python code for?", height=150)

# Generate code button
if st.button("Generate Code") and prompt.strip():
    with st.spinner("Generating code..."):
        try:
            response = client.completions.create(
                prompt=prompt,
                model="mistralai/Mistral-7B-Instruct-v0.1",  # ✅ Serverless model
                max_tokens=256,
                temperature=0.7,
                top_p=0.95,
                repetition_penalty=1.1,
                stop=["</s>"]
            )

            # Access the generated text from the response object correctly
            generated_code = response.output.strip()
            st.success("Here’s your code:")
            st.code(generated_code, language="python")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
