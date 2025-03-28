import streamlit as st
from fpdf import FPDF
from utils import format_number  # Function to separate numbers with commas

# PDF class to create the report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'گزارش مالی نهایی', border=0, ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'صفحه ' + str(self.page_no()), border=0, ln=0, align='C')

def save_report_to_pdf(manual_price, commission_cost, platform_development_cost, processing_cost, warehouse_shipping_cost, orange_label_cost, digikala_costs, net_income, total_production_cost, filament_cost, depreciation_cost, packaging_cost, profit_margin=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title of the report
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, f"گزارش مالی نهایی - محصول موردنظر شما", ln=True, align='R')
    pdf.ln(10)

    # Sales price
    pdf.set_font('Arial', size=12)
    pdf.cell(0, 10, f"💰 قیمت فروش در دیجی‌کالا: {format_number(manual_price)} تومان", ln=True, align='R')
    pdf.ln(5)

    # DigiKala costs
    pdf.cell(0, 10, "🔹 هزینه‌های مربوط به دیجی‌کالا:", ln=True, align='R')
    pdf.cell(0, 10, f"✅ کمیسیون: {format_number(commission_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"✅ هزینه توسعه پلتفرم (5%): {format_number(platform_development_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"✅ هزینه پردازش: {format_number(processing_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"✅ هزینه ارسال از انبار: {format_number(warehouse_shipping_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"✅ هزینه لیبل نارنجی: {format_number(orange_label_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"💰 مجموع کسر از مبلغ فروش: {format_number(digikala_costs)} تومان", ln=True, align='R')
    pdf.ln(10)

    # Production costs
    pdf.cell(0, 10, "🔹 هزینه‌های تولید:", ln=True, align='R')
    pdf.cell(0, 10, f"✅ فیلامنت مصرفی: {format_number(filament_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"✅ هزینه برق و استهلاک: {format_number(depreciation_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"✅ هزینه بسته‌بندی: {format_number(packaging_cost)} تومان", ln=True, align='R')
    pdf.cell(0, 10, f"💰 مجموع هزینه تولید: {format_number(total_production_cost)} تومان", ln=True, align='R')
    pdf.ln(10)

    # Net profit
    if profit_margin:
        pdf.cell(0, 10, "🔹 سود نهایی:", ln=True, align='R')
        pdf.cell(0, 10, f"✅ سود خالص: {format_number(net_income)} تومان", ln=True, align='R')

    # Save PDF file
    pdf.output("financial_report.pdf")
    st.success("📄 گزارش PDF با موفقیت ذخیره شد!")

def show():
    st.title("📌 محاسبه و گزارش مالی")

    # Retrieve saved values or defaults
    filament_price_per_kg = st.session_state.get("filament_price_per_kg", 900_000)
    depreciation_per_hour = st.session_state.get("depreciation_per_hour", 6_500)
    packaging_cost = st.session_state.get("packaging_cost", 700)
    processing_cost = st.session_state.get("processing_cost", 7_500)
    warehouse_shipping_cost = st.session_state.get("warehouse_shipping_cost", 13_000)
    orange_label_cost = st.session_state.get("orange_label_cost", 3_000)

    # User inputs
    filament_used = st.number_input("🔹 میزان فیلامنت مصرفی (گرم):", min_value=0.0, step=0.1)
    print_hours = st.number_input("⏳ مدت زمان پرینت (ساعت):", min_value=0, step=1)
    print_minutes = st.number_input("⏳ مدت زمان پرینت (دقیقه):", min_value=0, max_value=59, step=1)
    commission_percentage = st.number_input("💰 درصد کمیسیون فروش دیجی‌کالا (%):", min_value=0.0, max_value=100.0, step=0.1)

    # Optional profit margin
    use_profit_margin = st.checkbox("✅ استفاده از نرخ سود پیشنهادی", value=True)
    profit_margin = st.slider("💰 نرخ سود پیشنهادی (٪):", min_value=0, max_value=50, value=20, step=1) if use_profit_margin else 0

    # Sales price input
    manual_price = st.number_input("💰 قیمت فروش در دیجی‌کالا (اختیاری):", min_value=0)

    if st.button("📌 محاسبه و نمایش گزارش"):
        # Convert print time to hours
        total_print_time_hours = print_hours + (print_minutes / 60)

        # Production costs
        filament_cost = (filament_used / 1000) * filament_price_per_kg
        depreciation_cost = total_print_time_hours * depreciation_per_hour
        total_production_cost = filament_cost + depreciation_cost + packaging_cost

        # Suggested sales price
        suggested_price = total_production_cost * (1 + profit_margin / 100) if use_profit_margin else 0

        # DigiKala costs
        commission_cost = manual_price * (commission_percentage / 100) if manual_price > 0 else suggested_price * (commission_percentage / 100)
        platform_development_cost = manual_price * 0.05 if manual_price > 0 else suggested_price * 0.05
        digikala_costs = commission_cost + processing_cost + warehouse_shipping_cost + orange_label_cost + platform_development_cost

        # Break-even price
        break_even_price = total_production_cost + digikala_costs

        # Net profit analysis
        if manual_price > 0:
            manual_net_income = manual_price - digikala_costs
            manual_final_profit = manual_net_income - total_production_cost

        # Display report
        st.subheader(f"📌 گزارش مالی نهایی - محصول موردنظر شما")
        st.markdown(f"**💰 قیمت فروش در دیجی‌کالا:** `{format_number(int(manual_price if manual_price > 0 else suggested_price))} تومان`")
        st.write("### 🔹 هزینه‌های مربوط به دیجی‌کالا")
        st.write(f"✅ کمیسیون ({commission_percentage}%) → `{format_number(int(commission_cost))} تومان`")
        st.write(f"✅ هزینه توسعه پلتفرم (5%) → `{format_number(int(platform_development_cost))} تومان`")
        st.write(f"✅ هزینه پردازش → `{format_number(processing_cost)} تومان`")
        st.write(f"✅ هزینه ارسال از انبار → `{format_number(warehouse_shipping_cost)} تومان`")
        st.write(f"✅ هزینه لیبل نارنجی → `{format_number(orange_label_cost)} تومان`")
        st.markdown(f"**💰 مجموع کسر از مبلغ فروش:** `{format_number(int(digikala_costs))} تومان`")
        st.markdown(f"**💰 مبلغ دریافتی نهایی:** `{format_number(int(manual_price - digikala_costs if manual_price > 0 else suggested_price - digikala_costs))} تومان`")
        st.write("### 🔹 هزینه‌های تولید")
        st.write(f"✅ فیلامنت مصرفی: {filament_used} گرم → `{format_number(int(filament_cost))} تومان`")
        st.write(f"✅ هزینه برق و استهلاک پرینتر → `{format_number(int(depreciation_cost))} تومان`")
        st.write(f"✅ هزینه بسته‌بندی → `{format_number(packaging_cost)} تومان`")
        st.markdown(f"**💰 مجموع هزینه تولید:** `{format_number(int(total_production_cost))} تومان`")

        if use_profit_margin:
            st.write("### 🔹 سود نهایی")
            st.markdown(f"**✅ سود خالص:** `{format_number(int(manual_final_profit if manual_price > 0 else suggested_price - break_even_price))} تومان`")

        # Option to save PDF
        if st.button("📄 ذخیره گزارش به PDF"):
            save_report_to_pdf(
                manual_price, commission_cost, platform_development_cost