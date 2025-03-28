import streamlit as st
from utils import format_number  # تابع جداکننده اعداد را ایمپورت می‌کنیم

def show():
    st.title("⚙ تنظیمات هزینه‌ها")

    # مقدارهای پیش‌فرض برای تنظیمات (اگر قبلاً تنظیم نشده باشد)
    default_values = {
        "filament_price_per_kg": 900_000,
        "depreciation_per_hour": 6_500,
        "packaging_cost": 700,
        "processing_cost": 7_500,
        "warehouse_shipping_cost": 13_000,
        "orange_label_cost": 3_000
    }

    for key, default in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # نمایش مقدارهای فعلی با جداکننده هزار (,)
    st.write(f"💰 **قیمت فیلامنت:** {format_number(st.session_state['filament_price_per_kg'])} تومان")
    st.write(f"⚙ **هزینه استهلاک:** {format_number(st.session_state['depreciation_per_hour'])} تومان در ساعت")

    # تابعی برای دریافت ورودی و تبدیل آن به عدد صحیح
    def formatted_number_input(label, key):
        formatted_value = format_number(st.session_state[key])  # تبدیل مقدار به فرمت جدا از هزار
        input_value = st.text_input(label, formatted_value)  # نمایش مقدار با جداکننده هزار
        input_value = input_value.replace(",", "")  # حذف جداکننده قبل از ذخیره‌سازی
        if input_value.isnumeric():
            st.session_state[key] = int(input_value)

    # گرفتن مقدار ورودی با جداکننده هزار
    formatted_number_input("💰 قیمت فیلامنت به ازای هر کیلوگرم (تومان):", "filament_price_per_kg")
    formatted_number_input("⚙ هزینه استهلاک دستگاه به ازای هر ساعت (تومان):", "depreciation_per_hour")
    formatted_number_input("📦 هزینه بسته‌بندی (تومان):", "packaging_cost")
    formatted_number_input("🔄 هزینه پردازش (تومان):", "processing_cost")
    formatted_number_input("🚚 هزینه ارسال به انبار تهران (تومان):", "warehouse_shipping_cost")
    formatted_number_input("🏷 هزینه لیبل نارنجی (تومان):", "orange_label_cost")

    st.success("✅ اطلاعات ذخیره شد! می‌توانید صفحه محاسبه قیمت را بررسی کنید.")
