# Home.py
import streamlit as st

st.set_page_config(page_title="Princess Nourah App", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .source-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        cursor: pointer;
    }
    .source-card:hover {
        transform: translateY(-5px);
    }
    .card-pdf { background-color: #f0f7f4; }
    .card-text { background-color: #f5f5f5; }
    .card-url { background-color: #f5f0ff; }
    .card-youtube { background-color: #fff0f0; }
    .icon { font-size: 24px; margin-right: 10px; }
    h1 { text-align: center; margin-bottom: 40px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Select a Source to Create Questions")

col1, col2 = st.columns(2)

with col1:
    # PDF Card with link
    st.markdown("""
        <a href="pdf_upload" target="_self" style="text-decoration: none; color: inherit;">
            <div class="source-card card-pdf">
                <div style="display: flex; align-items: center;">
                    <span class="icon">📄</span>
                    <h3>From PDF</h3>
                </div>
                <p>Create quiz based on your PDF</p>
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    # URL Card with link
    st.markdown("""
        <a href="url_input" target="_self" style="text-decoration: none; color: inherit;">
            <div class="source-card card-url">
                <div style="display: flex; align-items: center;">
                    <span class="icon">🔗</span>
                    <h3>From URL</h3>
                </div>
                <p>Create quiz based on website URL</p>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col2:
    # Text Card with link
    st.markdown("""
        <a href="text_input" target="_self" style="text-decoration: none; color: inherit;">
            <div class="source-card card-text">
                <div style="display: flex; align-items: center;">
                    <span class="icon">📝</span>
                    <h3>From Text</h3>
                </div>
                <p>Create quiz based on your text</p>
            </div>
        </a>
    """, unsafe_allow_html=True)
    
    # YouTube Card with link
    st.markdown("""
        <a href="youtube_input" target="_self" style="text-decoration: none; color: inherit;">
            <div class="source-card card-youtube">
                <div style="display: flex; align-items: center;">
                    <span class="icon">▶️</span>
                    <h3>From YouTube</h3>
                </div>
                <p>Create quiz based on YouTube video</p>
            </div>
        </a>
    """, unsafe_allow_html=True)
