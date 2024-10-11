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
    # ... (refactored into smaller functions)

def main():
    st.title("Tuition Calculation Tool")

    # ... (rest of the code)

if __name__ == "__main__":
    main()
