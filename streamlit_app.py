import streamlit as st
import pandas as pd
import plotly.graph_objects as go  # Though not used in this snippet
import locale
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

# Configure locale for currency formatting
locale.setlocale(locale.LC_ALL, '')

# Helper function to format numbers as currency
def format_currency(value):
    try:
        return locale.currency(value, grouping=True)
    except:
        return f"<span class='math-inline'>{value:,.2f}</span>"

# Function to generate a downloadable PDF report
def generate_pdf(report_title, df, total_current_tuition, total_new_tuition, 
                 avg_increase_percentage, tuition_assistance_ratio, 
                 strategic_items_df, summary_text):
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
    pdf.drawString(50, height - 140, f"Tuition Assistance Ratio: {tuition_assistance_ratio:.2f}%")

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
            pdf.drawString(50, row_y, f"{row['Strategic Item']}: {row['Cost']}")
            row_y -= 15

    # Add the calculation summary text
    row_y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, row_y, "Summary of Calculations:")
    row_y -= 20
    pdf.setFont("Helvetica", 10)
    for line in textwrap.wrap(summary_text, width=90):  # Adjust width as needed
        pdf.drawString(50, row_y, line)
        row_y -= 15

    # Finalize PDF
    pdf.save()
    buffer.seek(0)
    return buffer

# Streamlit App Start
st.title("Tuition Calculation Tool")

# Step 1: Enter a Custom Title for the Report
report_title = st.text_input("Enter a Custom Title for the Report", "2025-26 Tuition Projection")

# Step 2: Add Custom Grade Levels and Tuition Rates
st.subheader("Step 2: Add Custom Grade Levels and Tuition Rates")
grades = []
num_students = []
current_tuition = []
num_grades = st.number_input("Number of Grade Levels", min_value=1, max_value=12, value=1, step=1)

for i in range(num_grades):
    grade = st.text_input(f"Grade Level {i+1} Name", f"Grade {i+1}")
    students = st.number_input(f"Number of Students in {grade}", min_value=0, step=1, value=0)
    tuition_input = st.text_input(f"Current Tuition per Student in {grade} (<span class='math-inline'><span class="math-inline"></span\>\)", ""\)
try\:
if tuition\_input\:
tuition \= float\(tuition\_input\.replace\(",", ""\)\) 
else\:
tuition \= 0\.0
except ValueError\:
st\.error\(f"Invalid input for tuition in \{grade\}\. Please enter a valid number\."\)
tuition \= 0\.0
formatted\_tuition \= format\_currency\(tuition\)
st\.text\(f"Formatted Tuition\: \{formatted\_tuition\}"\)
grades\.append\(grade\)
num\_students\.append\(students\)
current\_tuition\.append\(tuition\)
\# Step 3\: Automatically Calculate Average Tuition
if sum\(num\_students\) \> 0\:
total\_tuition \= sum\(\[students \* tuition for students, tuition in zip\(num\_students, current\_tuition\)\]\)
avg\_tuition \= total\_tuition / sum\(num\_students\)
st\.text\(f"Automatically Calculated Average Tuition per Student\: \{format\_currency\(avg\_tuition\)\}"\)
else\:
avg\_tuition \= 0\.0
st\.error\("Please enter valid student numbers and tuition rates to calculate average tuition\."\)
\# Step 4\: Add Strategic Items
st\.subheader\("Step 4\: Add Strategic Items"\)
strategic\_items\_costs \= \[\]
strategic\_item\_names \= \[\]
num\_items \= st\.number\_input\("Number of Strategic Items", min\_value\=0, max\_value\=10, value\=0, step\=1\)
for i in range\(int\(num\_items\)\)\:
item\_name \= st\.text\_input\(f"Strategic Item \{i\+1\} Name", f"Item \{i\+1\}"\)
item\_cost\_input \= st\.text\_input\(f"Cost of \{item\_name\} \(<span class\='math\-inline'\></span></span>)", "")
    
    try:
        if item_cost_input:
            item_cost = float(item_cost_input.replace(",", ""))
        else:
            item_cost = 0.0
    except ValueError:
        st.error(f"Invalid input for the cost of {item_name}. Please enter a valid number.")
        item_cost = 0.0

    formatted_item_cost = format_currency(item_cost)
    st.text(f"Formatted Cost: {formatted_item_cost}")
    
    strategic_item_names.append(item_name)
    strategic_
