import streamlit as st
import pandas as pd
import locale
from io import StringIO
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Configure locale for currency formatting
locale.setlocale(locale.LC_ALL, '')

def format_currency(value):
    """Format numbers as currency."""
    try:
        return locale.currency(value, grouping=True)
    except:
        return f"${value:,.2f}"

def format_input_as_currency(input_value):
    """Format input strings as currency."""
    try:
        if not input_value:
            return ""
        input_value = input_value.replace(",", "").replace("$", "")
        value = float(input_value)
        return f"${value:,.2f}"
    except ValueError:
        return ""

def calculate_table_height(num_rows, row_height=35, buffer_height=80):
    """
    Dynamically calculate the height of the table based on the number of rows.
    - num_rows: Number of rows in the table
    - row_height: Height per row in pixels
    - buffer_height: Additional buffer space for the header and padding
    """
    return num_rows * row_height + buffer_height

# Streamlit App Start
st.title("Tuition and Expense Planning Tool")

# Step 1: Previous Year's Total Expenses
st.subheader("Step 1: Previous Year's Total Expenses")
previous_expenses_input = st.text_input("Enter the Previous Year's Total Expenses ($)", "")
formatted_previous_expenses = format_input_as_currency(previous_expenses_input)
try:
    previous_expenses = float(formatted_previous_expenses.replace(",", "").replace("$", ""))
except ValueError:
    previous_expenses = 0.0

if previous_expenses > 0:
    st.success(f"Previous Year's Total Expenses: {format_currency(previous_expenses)}")
else:
    st.warning("Please enter valid total expenses.")

# Step 2: Operational Tuition Increase (OTI) Calculation
st.subheader("Step 2: Operational Tuition Increase (OTI)")
roi = st.number_input("Rate of Inflation (ROI) %", min_value=0.0, step=0.01, value=3.32)
rpi = st.number_input("Rate of Productivity Increase (RPI) %", min_value=0.0, step=0.01, value=2.08)
oti_percentage = roi + rpi
st.info(f"Operational Tuition Increase (OTI): {oti_percentage:.2f}%")

# Step 3: Strategic Items (SI) Input
st.subheader("Step 3: Strategic Items (SI)")
strategic_items = []
num_items = st.number_input("Number of Strategic Items", min_value=0, max_value=10, step=1, value=0)
for i in range(num_items):
    item_name = st.text_input(f"Strategic Item {i+1} Name", f"Item {i+1}")
    item_cost_input = st.text_input(f"Cost of {item_name} ($)", "")
    formatted_cost = format_input_as_currency(item_cost_input)
    try:
        item_cost = float(formatted_cost.replace(",", "").replace("$", ""))
    except ValueError:
        item_cost = 0.0
    item_description = st.text_area(f"Description of {item_name}", f"Details for {item_name}")
    strategic_items.append({"Item": item_name, "Cost": item_cost, "Description": item_description})

total_si_cost = sum(item["Cost"] for item in strategic_items)
si_percentage = (total_si_cost / previous_expenses) * 100 if previous_expenses > 0 else 0.0
st.info(f"Total Strategic Items Cost: {format_currency(total_si_cost)}")
st.info(f"Strategic Items (SI) Percentage: {si_percentage:.2f}%")

# Step 4: Total Expense Growth and Budget Projection
st.subheader("Step 4: Total Expense Growth and Budget Projection")
total_increase_percentage = oti_percentage + si_percentage
new_expense_budget = previous_expenses * (1 + total_increase_percentage / 100)

st.write(f"Total Increase in Expenses: {total_increase_percentage:.2f}%")
st.write(f"Projected New Expense Budget: {format_currency(new_expense_budget)}")

# Step 5: Tuition Assistance
st.subheader("Step 5: Tuition Assistance")
financial_aid_input = st.text_input("Enter the Total Financial Aid Provided ($)", "")
formatted_financial_aid = format_input_as_currency(financial_aid_input)
try:
    financial_aid = float(formatted_financial_aid.replace(",", "").replace("$", ""))
except ValueError:
    financial_aid = 0.0

if financial_aid > 0:
    st.success(f"Total Financial Aid: {format_currency(financial_aid)}")
else:
    st.warning("Please enter a valid financial aid amount.")

# Step 6: Tuition Adjustment by Grade Level
st.subheader("Step 6: Tuition Adjustment by Grade Level")

# Grade-level data input
num_grades = st.number_input("Number of Grade Levels", min_value=1, max_value=12, step=1, value=1)
grades = []
for i in range(num_grades):
    grade_name = st.text_input(f"Grade Level {i+1} Name", f"Grade {i+1}")
    num_students = st.number_input(f"Number of Students in {grade_name}", min_value=0, step=1, value=0)
    current_tuition = st.number_input(f"Current Tuition per Student in {grade_name} ($)", min_value=0.0, step=0.01, value=0.0)
    grades.append({"Grade": grade_name, "Number of Students": num_students, "Current Tuition": current_tuition})

grades_df = pd.DataFrame(grades)
grades_df["Projected Tuition per Student"] = grades_df["Current Tuition"] * (1 + total_increase_percentage / 100)
grades_df["Total Current Tuition"] = grades_df["Number of Students"] * grades_df["Current Tuition"]
grades_df["Total Projected Tuition"] = grades_df["Number of Students"] * grades_df["Projected Tuition per Student"]

# Initial Results Button
if st.button("View Initial Results"):
    st.subheader("Results: Initial Tuition Adjustments")
    grades_initial_df = grades_df.copy()
    grades_initial_df["Current Tuition"] = grades_initial_df["Current Tuition"].apply(format_currency)
    grades_initial_df["Projected Tuition per Student"] = grades_initial_df["Projected Tuition per Student"].apply(format_currency)
    grades_initial_df["Total Current Tuition"] = grades_initial_df["Total Current Tuition"].apply(format_currency)
    grades_initial_df["Total Projected Tuition"] = grades_initial_df["Total Projected Tuition"].apply(format_currency)

    initial_total_tuition = grades_df["Total Projected Tuition"].sum()
    initial_tuition_assistance_ratio = (financial_aid / initial_total_tuition) * 100 if initial_total_tuition > 0 else 0.0
    initial_income_to_expense_ratio = (initial_total_tuition / new_expense_budget) * 100 if new_expense_budget > 0 else 0.0
    initial_tuition_rate_increase = ((initial_total_tuition - grades_df["Total Current Tuition"].sum()) / grades_df["Total Current Tuition"].sum()) * 100 if grades_df["Total Current Tuition"].sum() > 0 else 0.0

    table_height = calculate_table_height(len(grades_initial_df))
    AgGrid(grades_initial_df, height=table_height)

    st.write(f"**Initial Total Tuition (Projected):** {format_currency(initial_total_tuition)}")
    st.caption("This is the projected revenue collected based on initial tuition rates and calculated increases.")
    st.write(f"**Initial Tuition Assistance Ratio:** {initial_tuition_assistance_ratio:.2f}%")
    st.caption("This measures how much of the projected tuition revenue is allocated to financial aid.")
    st.write(f"**Initial Income to Expense Ratio:** {initial_income_to_expense_ratio:.2f}%")
    st.caption("This shows whether the projected tuition revenue is sufficient to cover the school’s expenses before adjustments.")
    st.write(f"**Initial Tuition Rate Increase:** {initial_tuition_rate_increase:.2f}%")
    st.caption("This shows the percentage increase in tuition revenue based on the calculated tuition adjustments before user modifications.")

# Adjustments and Post-Adjustment Results
st.subheader("Results: Post-Adjustment Tuition")
adjusted_tuitions = []
for i, row in grades_df.iterrows():
    adjusted_tuition = st.number_input(
        f"Adjusted Tuition for {row['Grade']} ($)",
        min_value=0.0,
        step=0.01,
        value=row["Projected Tuition per Student"],
        key=f"adjusted_tuition_{i}",
    )
    adjusted_tuitions.append(adjusted_tuition)

grades_df["Adjusted Tuition per Student"] = adjusted_tuitions
grades_df["Total Adjusted Tuition"] = grades_df["Number of Students"] * grades_df["Adjusted Tuition per Student"]

post_total_tuition = grades_df["Total Adjusted Tuition"].sum()
post_tuition_assistance_ratio = (financial_aid / post_total_tuition) * 100 if post_total_tuition > 0 else 0.0
post_income_to_expense_ratio = (post_total_tuition / new_expense_budget) * 100 if new_expense_budget > 0 else 0.0
post_tuition_rate_increase = ((post_total_tuition - grades_df["Total Current Tuition"].sum()) / grades_df["Total Current Tuition"].sum()) * 100 if grades_df["Total Current Tuition"].sum() > 0 else 0.0

grades_post_adjustment_df = grades_df.copy()
grades_post_adjustment_df["Adjusted Tuition per Student"] = grades_post_adjustment_df["Adjusted Tuition per Student"].apply(format_currency)
grades_post_adjustment_df["Total Adjusted Tuition"] = grades_post_adjustment_df["Total Adjusted Tuition"].apply(format_currency)

post_table_height = calculate_table_height(len(grades_post_adjustment_df))
AgGrid(grades_post_adjustment_df, height=post_table_height)

st.write(f"**Adjusted Total Tuition (User Adjusted):** {format_currency(post_total_tuition)}")
st.caption("This is the revenue collected based on user-defined adjustments to tuition rates for each grade.")
st.write(f"**Adjusted Tuition Assistance Ratio:** {post_tuition_assistance_ratio:.2f}%")
st.caption("This measures how much of the adjusted tuition revenue is allocated to financial aid.")
st.write(f"**Adjusted Income to Expense Ratio:** {post_income_to_expense_ratio:.2f}%")
st.caption("This shows whether adjusted tuition revenue is sufficient to cover the school’s expenses after adjustments.")
st.write(f"**Tuition Rate Increase (Adjusted):** {post_tuition_rate_increase:.2f}%")
st.caption("This shows the percentage increase in tuition revenue based on the user’s adjustments.")
