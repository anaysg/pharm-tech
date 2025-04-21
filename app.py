import streamlit as st
import together
import os

# Set your Together API key
together.api_key = os.getenv("TOGETHER_API_KEY")

# App title
st.title("💊 Pharmacy & Healthcare Code Generator")
st.write("Describe what you want the code to do (e.g., *calculate BMI*, *plot glucose levels*, *Cockcroft-Gault equation*)")

# User input
prompt = st.text_area("Enter your task in plain English", height=150)

# Generate code
if st.button("Generate Code"):
    if not prompt:
        st.warning("Please enter a prompt first!")
    else:
        with st.spinner("Generating code..."):
            try:
                response = together.Complete.create(
                    model="meta-llama/Llama-3-8B-Instruct",
                    prompt=f"Write Python code to: {prompt}",
                    max_tokens=512,
                    temperature=0.7,
                    top_k=50,
                    top_p=0.95,
                    repetition_penalty=1.1,
                    stop=["</s>"]
                )
                # Display result
                generated_code = response['output'].strip()
                st.code(generated_code, language="python")

            except Exception as e:
                st.error(f"Oops, something went wrong: {e}")
