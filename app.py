import streamlit as st
import os
import together

# Set up Together.ai client using secret API key
together_client = together.Together(api_key=os.getenv("TOGETHER_API_KEY"))

# Streamlit App UI
st.set_page_config(page_title="PharmTech Code Generator 💊💻")
st.title("💊 Python Code Generator for Healthcare & Pharmacy Students")
st.markdown("Describe your task in plain English and get Python code instantly.")

# User input
prompt = st.text_area("🧠 What do you want the code to do?", height=150, placeholder="e.g. Calculate creatinine clearance using the Cockcroft-Gault equation")

# Generate code on button click
if st.button("🚀 Generate Code"):
    if not prompt.strip():
        st.warning("Please enter a task description.")
    else:
        with st.spinner("Generating your code..."):
            try:
                response = together_client.completions.create(
                    prompt=prompt,
                    model="togethercomputer/CodeLlama-7b-Instruct",  # Must be serverless
                    max_tokens=256,
                    temperature=0.7,
                    top_p=0.95,
                    repetition_penalty=1.1,
                    stop=["</s>"]
                )
                # Display the output
                generated_code = response.get("output", "").strip()
                if generated_code:
                    st.code(generated_code, language="python")
                else:
                    st.error("The model didn't return any code. Try rephrasing your input.")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
