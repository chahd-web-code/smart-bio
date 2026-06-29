import streamlit as st
import pandas as pd
import time
import altair as alt # مكتبة للرسوم البيانية الملونة
from PIL import Image
import cv2 # مكتبة معالجة الصور واستقبال البث

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="Smart Bio - نظام الفحص الذكي لفراولة",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# الرابط السحري الجديد الخاص بالكاميرا الممرر عبر النفق
ESP32_CAM_URL = "https://359813fb8e5a51.lhr.life/mjpeg" 

# 2. تصميم الواجهة بالـ CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1A1A2E; 
        color: white;
    }
    .main-title {
        color: #E94560; 
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding-bottom: 20px;
    }
    .st-d5, .st-c7, .st-c6 {
        color: #16C79A; 
        font-weight: 700;
    }
    [data-testid="stMetricValue"] {
        color: #00ADB5; 
        font-size: 3rem;
    }
    [data-testid="stMetricLabel"] {
        color: #E3E3E3;
    }
    .stButton>button {
        color: white;
        background-color: #E94560; 
        border-radius: 20px;
        border: none;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ADB5; 
        color: black;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🍓 نظام Smart Bio للتحليل المزدوج لفحص الفراولة</h1>', unsafe_allow_html=True)
st.write("📈 **لوحة بيانات البث الحي والتحليل الذكي بالأردوينو والبايثون**")

# --- تقسيم الواجهة ---
col_cam, col_spacer, col_dash = st.columns([1.8, 0.2, 1.3])

with col_cam:
    st.markdown('<h2 class="st-d5">📹 الوضع الحي (Live Stream)</h2>', unsafe_allow_html=True)
    
    frame_placeholder = st.empty()
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        run_stream = st.button("▶️ تشغيل البث الحي والتحليل المباشر")
    with col_btn2:
        st.button("📸 الوضع 2: التقاط صورة وتحليلها")

    # تشغيل البث عند الضغط على الزر
    if run_stream:
        st.success("⚡ جاري الاتصال بنفق الكاميرا المباشر...")
        cap = cv2.VideoCapture(ESP32_CAM_URL)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("❌ انقطع الاتصال بالكاميرا أو تحقق من تشغيل السيرفر المحلي.")
                break
            
            # تحويل الألوان لتناسب Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            time.sleep(0.03)
        cap.release()
    else:
        frame_placeholder.error("🔄 النظام في وضع الاستعداد. اضغط على الزر الأحمر بالأسفل لبدء البث.")

with col_dash:
    st.markdown('<h2 class="st-d5">📊 لوحة الإحصائيات الذكية (Dashboard)</h2>', unsafe_allow_html=True)
    
    with st.container():
        m1, m2 = st.columns(2)
        m1.metric("حالة الدفيئة", "آمنة 🟡")
        m2.metric("فحوصات اليوم", "14 لقطة ✅")
        st.write("")
        m3, m4 = st.columns(2)
        m3.metric("معدل الرطوبة", "75%")
        m4.metric("دقة النموذج", "97.2%")
        
    st.markdown("---")
    st.markdown('<h3 class="st-d5">📈 معدل صحة الأوراق هذا الأسبوع:</h3>', unsafe_allow_html=True)
    
    chart_data = pd.DataFrame({
        'الأيام': ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس'],
        'النسبة المئوية للصحة': [92, 94, 95, 97]
    })
    
    chart = alt.Chart(chart_data).mark_line(
        point=True, color='#16C79A', size=3
    ).encode(
        x='الأيام',
        y=alt.Y('النسبة المئوية للصحة', scale=alt.Scale(domain=[90, 100])),
        tooltip=['الأيام', 'النسبة المئوية للصحة']
    ).properties(
        background='#16213E'
    ).configure_view(
        stroke=None
    ).configure_axis(
        labelColor='white',
        titleColor='white'
    )
    
    st.altair_chart(chart, use_container_width=True)
