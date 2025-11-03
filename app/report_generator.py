# app/report_generator.py
from fpdf import FPDF

def generate_report(user_id, mood_logs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weekly Wellbeing Report", ln=True, align="C")

    for day, mood in mood_logs.items():
        pdf.cell(200, 10, txt=f"{day}: {mood}", ln=True)

    pdf.output(f"{user_id}_weekly_report.pdf")
