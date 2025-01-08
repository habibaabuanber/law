import streamlit as st
from langchain_openai import ChatOpenAI
import time

# Initialize ChatGPT
chat = ChatOpenAI(temperature=0.7, model="gpt-4")

# Custom CSS for better Arabic support and styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .case-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        direction: rtl;
    }
    
    .role-selector {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        direction: rtl;
    }
    
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
        direction: rtl;
    }
    
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    
    .ai-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    
    .feedback-section {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        direction: rtl;
    }
    
    .resource-card {
        background-color: #f1f8e9;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .resource-card:hover {
        transform: translateY(-2px);
    }
    
    .progress-section {
        background-color: #fce4ec;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("المحكمة الافتراضية الذكية")
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("### القائمة الرئيسية")
        mode = st.radio(
            "اختر نوع التدريب",
            ["التدريب على القضايا", "صياغة المستندات", "المحاكمة الافتراضية", "الموارد التعليمية"]
        )
    
    if mode == "التدريب على القضايا":
        show_case_training()
    elif mode == "صياغة المستندات":
        show_document_drafting()
    elif mode == "المحاكمة الافتراضية":
        show_virtual_trial()
    else:
        show_educational_resources()

def show_case_training():
    st.markdown("### التدريب على القضايا")
    
    # Case type selector
    case_type = st.selectbox(
        "اختر نوع القضية",
        ["الأحوال الشخصية", "القانون التجاري", "القانون الجنائي", "قانون العمل"]
    )
    
    # Role selector
    role = st.selectbox(
        "اختر دورك في القضية",
        ["القاضي", "المدعي العام", "محامي الدفاع", "الباحث القانوني"]
    )
    
    # Display case details
    st.markdown("""
        <div class="case-card">
            <h4>تفاصيل القضية</h4>
            <p>هذه قضية تتعلق بـ[وصف القضية]. يرجى دراسة التفاصيل وتقديم رأيك القانوني.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Interactive chat interface
    user_input = st.text_area("اكتب ردك القانوني هنا", height=100)
    if st.button("إرسال"):
        with st.spinner("جاري تحليل ردك..."):
            time.sleep(1)  # Simulated delay
            st.markdown("""
                <div class="feedback-section">
                    <h4>التحليل والتوجيه</h4>
                    <ul>
                        <li>نقاط القوة في ردك</li>
                        <li>مجالات للتحسين</li>
                        <li>مراجع قانونية مقترحة</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

def show_document_drafting():
    st.markdown("### صياغة المستندات القانونية")
    
    doc_type = st.selectbox(
        "اختر نوع المستند",
        ["مذكرة قانونية", "عقد", "لائحة دعوى", "مذكرة دفاع"]
    )
    
    st.text_area("اكتب المستند هنا", height=300)
    
    if st.button("تحليل المستند"):
        with st.spinner("جاري تحليل المستند..."):
            time.sleep(1)
            st.markdown("""
                <div class="feedback-section">
                    <h4>تحليل المستند</h4>
                    <ul>
                        <li>الهيكل والتنسيق</li>
                        <li>اللغة القانونية</li>
                        <li>المراجع والاستشهادات</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

def show_virtual_trial():
    st.markdown("### المحاكمة الافتراضية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="case-card">
                <h4>معلومات القضية</h4>
                <p>قضية رقم: 123/2025</p>
                <p>نوع القضية: تجارية</p>
                <p>المرحلة: المرافعة</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="role-selector">
                <h4>دورك في المحاكمة</h4>
                <p>أنت تمثل: محامي الدفاع</p>
                <p>المطلوب: تقديم المرافعة</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.text_area("اكتب مرافعتك هنا", height=200)
    
    if st.button("تقديم المرافعة"):
        with st.spinner("جاري تحليل المرافعة..."):
            time.sleep(1)
            st.markdown("""
                <div class="feedback-section">
                    <h4>تقييم المرافعة</h4>
                    <ul>
                        <li>قوة الحجج القانونية</li>
                        <li>الأسلوب والعرض</li>
                        <li>الاستشهاد بالسوابق القضائية</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

def show_educational_resources():
    st.markdown("### الموارد التعليمية")
    
    st.markdown("""
        <div class="resource-card">
            <h4>📚 الأنظمة واللوائح</h4>
            <p>مجموعة من الأنظمة واللوائح السعودية المحدثة</p>
        </div>
        
        <div class="resource-card">
            <h4>⚖️ السوابق القضائية</h4>
            <p>مجموعة مختارة من الأحكام القضائية المهمة</p>
        </div>
        
        <div class="resource-card">
            <h4>📝 نماذج المستندات</h4>
            <p>نماذج للمستندات القانونية المختلفة</p>
        </div>
        
        <div class="resource-card">
            <h4>🎓 دروس تعليمية</h4>
            <p>دروس في المهارات القانونية الأساسية</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()