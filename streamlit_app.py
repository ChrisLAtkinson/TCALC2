import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import locale
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap
from typing import Dict, List

# Constants
MAX_GRADE_LEVELS = 12
MAX_STRATEGIC_ITEMS = 10
TEXT_WRAP_WIDTH = 90

# Configure locale for currency formatting
locale.setlocale(locale.LC_ALL, '')

def format_currency(value: float) -> str:
    """Format numbers as currency"""
    try:
        return locale.currency(value, grouping=True)
    except:
        return f"${value:,.2f}"

def format_input_as_currency(input_value: str) -> str:
    """Format input strings as currency"""
    try:
        if not input_value:
            return ""
        input_value = input_value.replace(",", "").replace("$", "")
        value = float(input_value)
        return f"${value:,.2f}"
    except ValueError:
        return ""

def generate_pdf(report_title: str, df: pd.DataFrame, total_current_tuition: float, 
                 total_new_tuition: float, avg_increase_percentage: float, 
                 tuition_assistance_ratio: float, strategic_items_df: pd.DataFrame, 
                 summary_text: str) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title of the report
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 50, f"Report Title: {report_title}")

    # Summary details
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, height - 80, f"Total Current Tuition: {format_currency(total_current_tuition)}")
    pdf.drawString(50, height - 100, f"Total New Tuition: {format_currency(total_new_tuition)}")
    pdf.drawString(50, height - 120, f"Average Tuition Increase Percentage: {avg_increase_percentage:.2f}%")
    pdf.drawString(50, height - 140, f"Tuition Assistance Ratio: {tuition_assistance_ratio:.2f}%")  # Added closing bracket

    # Add the table for tuition by grade level
    pdf.drawString(50, height - 170, "Tuition by Grade Level:")
    row_y = height - 190
    pdf.setFont("Helvetica", 10)
    for i, row in df.iterrows():
        pdf.drawString(50, row_y, f"{row['Grade']}: {row['Number of Students']} students, "
                                  f"Current Tuition: {row['Current Tuition per Student']}, "
                                  f"New Tuition: {row['New Tuition per Student']}")
        row_y -= 15

    # Strategic Items Section
    if not strategic_items_df.empty:
        row_y -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, row_y, "Strategic Items and Costs:")
        row_y -= 20
        pdf.setFont("Helvetica", 10)
        for i, row in strategic_items_df.iterrows():
            pdf.drawString(50, row_y, f"{row['Strategic Item']}: {row['Cost ($)']}")
            row_y -= 15

    # Add the calculation summary text
    row_y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, row_y, "Summary of Calculations:")
    row_y -= 20
    pdf.setFont("Helvetica", 10)
    for line in textwrap.wrap(summary_text, width=TEXT_WRAP_WIDTH):
        pdf.drawString(50, row_y, line)
        row_y -= 15

    # Finalize PDF
    pdf.save()
    buffer.seek(0)
    return buffer

def main():
    st.title("Tuition Calculation Tool")

    # Step 1: Enter a Custom Title for the Report
    report_title = st.text_input("Enter a Custom Title for the Report", "2025-26 Tuition Projection")

    # Step 2: Add Custom Grade Levels and Tuition Rates
    st.subheader("Step 2: Add Custom Grade Levels and Tuition Rates")
    grades = []
    num_students = []
    current_tuition = []
    num_grades = st.number_input("Number of Grade Levels", min_value=1, max_value=MAX_GRADE_LEVELS, value=1, step=1)

    for i in range(num_grades):
        grade = st.text_input(f"Grade Level {i+1} Name", f"Grade {i+1}")
        students = st.number_input(f"Number of Students in {grade}", min_value=0, step=1,
