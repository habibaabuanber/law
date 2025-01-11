import re
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_core.vectorstores import InMemoryVectorStore
import getpass
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader

st.title("Document Q&A System")

# Load environment variables from .env file
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = InMemoryVectorStore(embeddings)

# File upload
uploaded_file = st.file_uploader("قم بتحميل الملفات ", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Load the uploaded PDF file
    loader = PyPDFLoader(file_path=f"uploaded_file.pdf")
    docs = loader.load()
    st.write("PDF loaded successfully!")

    # Process the document
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    _ = vector_store.add_documents(documents=all_splits)
    st.write("Document split and indexed successfully!")

    # Define prompt for question-answering
    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str

    # Define application steps
    def retrieve(state: State):
        retrieved_docs = vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}

    def clean_text(text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\d+\s*\n', '', text)
        text = re.sub(r'(.)\1{2,}', r'\1', text)
        return text.strip()

    def format_context(docs):
        cleaned_docs = [clean_text(doc.page_content) for doc in docs]
        return "\n\n".join(cleaned_docs)

    def generate(state: State):
        docs_content = format_context(state["context"])
        prompt_template = (
            f"فقط قم بالإعتماد علي البيانات في النص المعطي للإجابة بشكل محدد ودقيق علي السؤال الذي يقترح كن دقيقا\n"
            f"السؤال: {state['question']}\n"
            f"البيانات التي يجب الاعتماد عليها: {docs_content}"
        )
        messages = [{"role": "user", "content": prompt_template}]
        response = llm.invoke(messages)
        return {"answer": response.content}

    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    # User input for question
    question = st.text_input("Enter your question:")

    if question:
        response = graph.invoke({"question": question})
        st.write("Answer:")
        st.write(response["answer"])