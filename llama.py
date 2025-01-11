import os
from together import Together
from PyPDF2 import PdfReader
import streamlit as st

# Streamlit App
st.title("AI Question Answering from PDF")

# Upload PDF
uploaded_file = st.file_uploader("ارفاق ملف pdf", type="pdf")

# Enter Question
question = st.text_input("ادخل سؤالك ...")

# Button to submit the query
if st.button("Get Answer"):
    if uploaded_file and question:
        # Extract text from the uploaded PDF
        def extract_text_from_pdf(pdf_file):
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        
        # Extract text
        pdf_text = extract_text_from_pdf(uploaded_file)

        # Limit the extracted text to the first 4000 characters
        pdf_text = pdf_text

        # Initialize Together client
        client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

        # Create the prompt
        prompt = (f"فقط قم بالإعتماد علي البيانات في النص المعطي للإجابة بشكل محدد ودقيق علي السؤال الذي يقترح كن دقيقا\n"
            f"السؤال: {question}\n"
            f"البيانات التي يجب الاعتماد عليها: {pdf_text}")
        # Send the request to Together
        try:
            stream = client.chat.completions.create(
                model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                messages=[{"role": "user", "content": prompt}],
                stream=True,temperature=0.0
            )

            # Display the response
            answer = ""
            for chunk in stream:
                answer += chunk.choices[0].delta.content or ""
            
            # Display the complete answer
            st.text("Answer:")
            st.write(answer) 
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a PDF and enter a question.")
