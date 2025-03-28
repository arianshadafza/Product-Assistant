import streamlit as st
from pages import pricing, settings

st.set_page_config(page_title="StudioMorphyTool", layout="wide")

st.sidebar.title("📌 منوی اصلی")
page = st.sidebar.radio("انتخاب صفحه", ["🏠 صفحه اصلی", "📊 محاسبه قیمت", "⚙ تنظیمات"])

if page == "🏠 صفحه اصلی":
    st.title("🎨 StudioMorphyTool")
    st.write("ابزاری برای مدیریت هزینه تولید و قیمت‌گذاری محصولات سه‌بعدی.")

elif page == "📊 محاسبه قیمت":
    pricing.show()

elif page == "⚙ تنظیمات":
    settings.show()
