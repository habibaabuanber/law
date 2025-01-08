# pages/2_text_input.py
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os

# Set your OpenAI API key
OPENAI_API_KEY = ""

def split_text(text):
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def generate_mcq(text, num_questions=3):
    system_template = """أنت مساعد متخصص في إنشاء أسئلة اختيار من متعدد. عليك إنشاء {num_questions} أسئلة من النص المقدم.
    يجب أن يكون لكل سؤال 4 خيارات، وإجابة واحدة صحيحة فقط.
    
    قم بتنسيق الإجابة بالشكل التالي:
    السؤال: [نص السؤال]
    أ) [الخيار الأول]
    ب) [الخيار الثاني]
    ج) [الخيار الثالث]
    د) [الخيار الرابع]
    الإجابة الصحيحة: [الحرف المقابل للإجابة الصحيحة]
    
    التفسير: [شرح مختصر لسبب كون هذه الإجابة صحيحة]"""

    human_template = """النص: {text}"""

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        human_message_prompt
    ])

    chat = ChatOpenAI(temperature=0.7, model="gpt-4")
    chain = chat_prompt | chat
    response = chain.invoke({
        "text": text,
        "num_questions": num_questions
    })
    return response.content

def format_question(question_text):
    # Split the question into its components
    lines = question_text.strip().split('\n')
    formatted_text = ""
    
    for line in lines:
        if line.startswith("السؤال:"):
            formatted_text += f"<div style='font-weight: bold; color: #2e4057; margin: 10px 0;'>{line}</div>"
        elif line.startswith(("أ)", "ب)", "ج)", "د)")):
            formatted_text += f"<div style='margin-right: 20px; margin-bottom: 5px;'>{line}</div>"
        elif line.startswith("الإجابة الصحيحة:"):
            formatted_text += f"<div style='color: #28a745; font-weight: bold; margin: 10px 0;'>{line}</div>"
        elif line.startswith("التفسير:"):
            formatted_text += f"<div style='color: #17a2b8; margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-radius: 5px;'>{line}</div>"
        else:
            formatted_text += f"<div>{line}</div>"
    
    return formatted_text

def display_questions(questions_list):
    for i, question_set in enumerate(questions_list, 1):
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h3 style='color: #1f1f1f; border-bottom: 2px solid #1f1f1f; padding-bottom: 10px;'>
                مجموعة الأسئلة {i}
            </h3>
            <div style='white-space: pre-line; direction: rtl; text-align: right;'>
                {question_set}
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    st.markdown("""
        <style>
        .main {
            direction: rtl;
        }
        .stButton>button {
            width: 100%;
        }
        textarea {
            direction: rtl;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("إنشاء اختبار من نص")
    st.write("قم بإدخال النص لإنشاء أسئلة اختيار من متعدد")

    # Text input area with RTL support
    text_input = st.text_area(
        "أدخل النص هنا",
        height=300,
        key="text_input",
        help="قم بنسخ ولصق النص الذي تريد إنشاء أسئلة منه"
    )
    
    if text_input:
        # Split text into chunks
        chunks = split_text(text_input)
        st.success(f'تم تقسيم النص إلى {len(chunks)} أجزاء')
        
        # Questions per chunk slider
        questions_per_chunk = st.slider(
            'عدد الأسئلة لكل جزء',
            min_value=1,
            max_value=5,
            value=2
        )
        
        if st.button("إنشاء الاختبار"):
            all_questions = []
            progress_bar = st.progress(0)
            
            for i, chunk in enumerate(chunks):
                progress_bar.progress((i + 1) / len(chunks))
                with st.spinner(f'جاري إنشاء الأسئلة للجزء {i+1}/{len(chunks)}...'):
                    questions = generate_mcq(chunk, questions_per_chunk)
                    formatted_questions = format_question(questions)
                    all_questions.append(formatted_questions)
            
            # Display formatted questions
            st.markdown("<h2 style='text-align: right;'>الأسئلة المولدة</h2>", unsafe_allow_html=True)
            display_questions(all_questions)
            
            # Download button for questions
            combined_questions = "\n\n".join([q.replace("<div>", "").replace("</div>", "\n") for q in all_questions])
            st.download_button(
                label="تحميل الأسئلة",
                data=combined_questions,
                file_name="quiz_questions.txt",
                mime="text/plain"
            )

# Add custom CSS for better RTL support and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .question-container {
        direction: rtl;
        text-align: right;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .option {
        margin: 10px 20px;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    
    .correct-answer {
        color: #28a745;
        font-weight: bold;
        margin: 15px 0;
    }
    
    .explanation {
        color: #17a2b8;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 5px;
        margin: 15px 0;
    }
    
    .stTextArea textarea {
        direction: rtl;
        font-family: 'Cairo', sans-serif;
        padding: 10px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()