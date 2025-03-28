import streamlit as st
from utils import format_number  # تابع جداکننده هزار

def show():
    st.title("📊 محاسبه قیمت")

    # گرفتن مقادیر ذخیره‌شده در تنظیمات
    filament_price_per_kg = st.session_state.get("filament_price_per_kg", 900_000)
    depreciation_per_hour = st.session_state.get("depreciation_per_hour", 6_500)
    packaging_cost = st.session_state.get("packaging_cost", 700)
    processing_cost = st.session_state.get("processing_cost", 7_500)
    warehouse_shipping_cost = st.session_state.get("warehouse_shipping_cost", 13_000)
    orange_label_cost = st.session_state.get("orange_label_cost", 3_000)

    # ورودی‌های کاربر
    filament_used = st.number_input("🔹 میزان فیلامنت مصرفی (گرم)", min_value=0.0, step=0.1)
    print_hours = st.number_input("⏳ مدت پرینت (ساعت)", min_value=0, step=1)
    print_minutes = st.number_input("⏳ مدت پرینت (دقیقه)", min_value=0, max_value=59, step=1)
    commission_percentage = st.number_input("💰 کمیسیون دیجی‌کالا (%)", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("📌 محاسبه قیمت"):
        # تبدیل مدت پرینت به ساعت
        total_print_time_hours = print_hours + (print_minutes / 60)

        # محاسبه هزینه‌های تولید
        filament_cost = (filament_used / 1000) * filament_price_per_kg
        depreciation_cost = total_print_time_hours * depreciation_per_hour
        total_production_cost = filament_cost + depreciation_cost + packaging_cost

        # محاسبه هزینه‌های دیجی‌کالا
        commission = (commission_percentage / 100) * filament_cost
        digikala_costs = commission + processing_cost + warehouse_shipping_cost + orange_label_cost

        # قیمت فروش پیشنهادی (مجموع هزینه تولید + هزینه‌های دیجی‌کالا + ۲۰٪ سود)
        suggested_price = (total_production_cost + digikala_costs) * 1.2

        # محاسبه سود نهایی
        final_income = suggested_price - digikala_costs
        final_profit = final_income - total_production_cost

        # گزارش نهایی با جداکننده هزار
        st.subheader("📌 گزارش مالی نهایی")
        st.markdown(f"**💰 قیمت فروش پیشنهادی:** `{format_number(int(suggested_price))} تومان`")

        st.write("### 🔹 هزینه‌های مربوط به دیجی‌کالا")
        st.write(f"✅ کمیسیون ({commission_percentage}%) → `{format_number(int(commission))} تومان`")
        st.write(f"✅ هزینه پردازش → `{format_number(processing_cost)} تومان`")
        st.write(f"✅ هزینه ارسال از انبار → `{format_number(warehouse_shipping_cost)} تومان`")
        st.write(f"✅ هزینه لیبل نارنجی → `{format_number(orange_label_cost)} تومان`")
        st.markdown(f"**💰 مجموع کسر از مبلغ فروش:** `{format_number(int(digikala_costs))} تومان`")

        st.write("### 🔹 هزینه‌های تولید")
        st.write(f"✅ فیلامنت مصرفی: {filament_used} گرم → `{format_number(int(filament_cost))} تومان`")
        st.write(f"✅ هزینه برق و استهلاک → `{format_number(int(depreciation_cost))} تومان`")
        st.write(f"✅ هزینه بسته‌بندی → `{format_number(packaging_cost)} تومان`")
        st.markdown(f"**💰 مجموع هزینه تولید:** `{format_number(int(total_production_cost))} تومان`")

        st.write("### 🔹 سود نهایی")
        st.write(f"✅ مبلغ دریافتی نهایی: `{format_number(int(final_income))} تومان`")
        st.markdown(f"**✅ سود خالص:** `{format_number(int(final_profit))} تومان`")

