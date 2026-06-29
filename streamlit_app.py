import streamlit as st
import pandas as pd
import time
import altair as alt # مكتبة للرسوم البيانية الملونة
from PIL import Image

# 1. إعدادات الصفحة (أول سطر في الكود)
st.set_page_config(
    page_title="Smart Bio - نظام الفحص الذكي لفراولة",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. تصميم الواجهة بالـ CSS (لجعل الألوان جذابة)
st.markdown("""
<style>
    /* تغيير لون الخلفية العامة */
    .stApp {
        background-color: #1A1A2E; /* كحلي داكن */
        color: white;
    }
    
    /* تصميم العنوان الرئيسي */
    .main-title {
        color: #E94560; /* أحمر فراولي */
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding-bottom: 20px;
    }
    
    /* تصميم العناوين الفرعية */
    .st-d5, .st-c7, .st-c6 {
        color: #16C79A; /* أخضر زمردي */
        font-weight: 700;
    }
    
    /* تصميم صناديق الإحصائيات (Metrics) */
    [data-testid="stMetricValue"] {
        color: #00ADB5; /* تركواز */
        font-size: 3rem;
    }
    [data-testid="stMetricLabel"] {
        color: #E3E3E3;
    }
    
    /* تصميم الحواف (Cards) للرسومات */
    .chart-container {
        border-radius: 15px;
        background-color: #16213E; /* كحلي أفتح قليلاً */
        padding: 20px;
        border: 1px solid #16C79A;
    }
    
    /* تصميم الأزرار (Buttons) */
    .stButton>button {
        color: white;
        background-color: #E94560; /* أحمر */
        border-radius: 20px;
        border: none;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ADB5; /* تركواز عند التمرير */
        color: black;
    }
</style>
""", unsafe_allow_html=True)

# --- محتوى الموقع (العنوان والصور) ---

# العنوان الرئيسي الملون
st.markdown('<h1 class="main-title">🍓 نظام Smart Bio للتحليل المزدوج لفحص الفراولة</h1>', unsafe_allow_html=True)

# محاكاة صورة للفراولة في الأعلى لجعل الواجهة أجمل (اختياري)
# try:
#     img = Image.open('strawberry_field.jpg') # إذا كان لديكِ صورة
#     st.image(img, caption='حقل الفراولة قيد المراقبة الآلية', use_column_width=True)
# except:
#     pass

st.write("📈 **لوحة بيانات البث الحي والتحليل الذكي بالأردوينو والبايثون**")

# --- تقسيم الواجهة (Layout) ---
col_cam, col_spacer, col_dash = st.columns([1.8, 0.2, 1.3])

with col_cam:
    st.markdown('<h2 class="st-d5">📹 الوضع الحي (Live Stream)</h2>', unsafe_allow_html=True)
    
    # مكان عرض شاشة الكاميرا
    frame_placeholder = st.empty()
    
    # محاكاة شاشة البث (لحين توصيل الكاميرا)
    st.error("🔄 النظام في وضع الاستعداد. اضغط زر RST في الكاميرا.")

    st.markdown("---")
    
    # أزرار التحكم الجذابة
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.button("▶️ تشغيل البث الحي والتحليل المباشر")
    with col_btn2:
        st.button("📸 الوضع 2: التقاط صورة وتحليلها")

with col_dash:
    st.markdown('<h2 class="st-d5">📊 لوحة الإحصائيات الذكية (Dashboard)</h2>', unsafe_allow_html=True)
    
    # صناديق البيانات (Metrics) الملونة
    with st.container():
        m1, m2 = st.columns(2)
        m1.metric("حالة الدفيئة", "آمنة 🟡", help="الحالة العامة للأوراق")
        m2.metric("فحوصات اليوم", "14 لقطة ✅")
        st.write("")
        m3, m4 = st.columns(2)
        m3.metric("معدل الرطوبة", "75%", help="رطوبة الحقل المراقبة")
        m4.metric("دقة النموذج", "97.2%", help="دقة نموذج الذكاء الاصطناعي")
        
    st.markdown("---")
    
    # الرسم البياني الملون والاحترافي (Altair)
    st.markdown('<h3 class="st-d5">📈 معدل صحة الأوراق هذا الأسبوع:</h3>', unsafe_allow_html=True)
    
    chart_data = pd.DataFrame({
        'الأيام': ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس'],
        'النسبة المئوية للصحة': [92, 94, 95, 97]
    })
    
    # رسم بياني عصري وملون (خلفية داكنة)
    chart = alt.Chart(chart_data).mark_line(
        point=True, color='#16C79A', size=3 # خط أخضر
    ).encode(
        x='الأيام',
        y=alt.Y('النسبة المئوية للصحة', scale=alt.Scale(domain=[90, 100])),
        tooltip=['الأيام', 'النسبة المئوية للصحة']
    ).properties(


background='#16213E' # نفس خلفية الكارت
    ).configure_view(
        stroke=None # بدون حواف داخلية
    ).configure_axis(
        labelColor='white',
        titleColor='white'
    )
    
    st.altair_chart(chart, use_container_width=True)
