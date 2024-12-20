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

# Calculate initial projected tuition increases
grades_df = pd.DataFrame(grades)
grades_df["Projected Tuition per Student"] = grades_df["Current Tuition"] * (1 + total_increase_percentage / 100)
grades_df["Total Current Tuition"] = grades_df["Number of Students"] * grades_df["Current Tuition"]
grades_df["Total Projected Tuition"] = grades_df["Number of Students"] * grades_df["Projected Tuition per Student"]

# Button for Initial Results
if st.button("View Initial Results"):
    st.subheader("Results: Initial Tuition Adjustments")
    grades_initial_df = grades_df.copy()
    grades_initial_df["Current Tuition"] = grades_initial_df["Current Tuition"].apply(format_currency)
    grades_initial_df["Projected Tuition per Student"] = grades_initial_df["Projected Tuition per Student"].apply(format_currency)
    grades_initial_df["Total Current Tuition"] = grades_initial_df["Total Current Tuition"].apply(format_currency)
    grades_initial_df["Total Projected Tuition"] = grades_initial_df["Total Projected Tuition"].apply(format_currency)

    # Render initial table
    initial_table_height = calculate_table_height(len(grades_initial_df))
    AgGrid(grades_initial_df, height=initial_table_height, fit_columns_on_grid_load=True)

    # Calculate initial metrics
    tuition_assistance_ratio_initial = (financial_aid / grades_df["Total Projected Tuition"].sum()) * 100 if grades_df["Total Projected Tuition"].sum() > 0 else 0.0
    income_to_expense_ratio_initial = (grades_df["Total Projected Tuition"].sum() / new_expense_budget) * 100 if new_expense_budget > 0 else 0.0
    tuition_rate_increase_initial = ((grades_df["Total Projected Tuition"].sum() - grades_df["Total Current Tuition"].sum()) / grades_df["Total Current Tuition"].sum()) * 100 if grades_df["Total Current Tuition"].sum() > 0 else 0.0

    # Initial Metrics Explanations
    st.write(f"**Initial Total Tuition (Projected):** {format_currency(grades_df['Total Projected Tuition'].sum())}")
    st.write(f"*(The total expected tuition revenue based on projected rates and student numbers.)*")

    st.write(f"**Tuition Assistance Ratio (Initial):** {tuition_assistance_ratio_initial:.2f}%")
    st.write(f"*(Percentage of tuition revenue allocated for financial aid support.)*")

    st.write(f"**Income to Expense Ratio (Initial):** {income_to_expense_ratio_initial:.2f}%")
    st.write(f"*(The proportion of total projected income relative to the planned expense budget.)*")

    st.write(f"**Tuition Rate Increase (Initial):** {tuition_rate_increase_initial:.2f}%")
    st.write(f"*(The percentage increase in tuition revenue compared to current rates.)*")

# Adjust Tuition by Grade Level
st.subheader("Adjust Tuition by Grade Level")
adjusted_grades_df = grades_df.copy()  # Ensure we adjust a copy, not the original DataFrame

for i, grade in adjusted_grades_df.iterrows():
    adjusted_tuition = st.number_input(
        f"Adjusted Tuition for {grade['Grade']} ($)",
        min_value=0.0,
        step=0.01,
        value=grade["Projected Tuition per Student"],
        key=f"adjusted_tuition_{i}"
    )
    adjusted_grades_df.at[i, "Adjusted Tuition per Student"] = adjusted_tuition

# Recalculate totals immediately after adjustments
adjusted_grades_df["Total Adjusted Tuition"] = adjusted_grades_df["Number of Students"] * adjusted_grades_df["Adjusted Tuition per Student"]

# Post-Adjustment Results
st.subheader("Results: Post-Adjustment Tuition")
grades_post_adjustment_df = adjusted_grades_df.copy()
grades_post_adjustment_df["Current Tuition"] = grades_post_adjustment_df["Current Tuition"].apply(format_currency)
grades_post_adjustment_df["Adjusted Tuition per Student"] = grades_post_adjustment_df["Adjusted Tuition per Student"].apply(format_currency)
grades_post_adjustment_df["Total Adjusted Tuition"] = grades_post_adjustment_df["Total Adjusted Tuition"].apply(format_currency)

# Render the adjusted table
post_table_height = calculate_table_height(len(grades_post_adjustment_df))
AgGrid(grades_post_adjustment_df, height=post_table_height, fit_columns_on_grid_load=True)

# Post-Adjustment Metrics Explanations
adjusted_total_tuition = adjusted_grades_df["Total Adjusted Tuition"].sum()
tuition_assistance_ratio_adjusted = (financial_aid / adjusted_total_tuition) * 100 if adjusted_total_tuition > 0 else 0.0
income_to_expense_ratio_adjusted = (adjusted_total_tuition / new_expense_budget) * 100 if new_expense_budget > 0 else 0.0
tuition_rate_increase_adjusted = ((adjusted_total_tuition - grades_df["Total Current Tuition"].sum()) / grades_df["Total Current Tuition"].sum()) * 100 if grades_df["Total Current Tuition"].sum() > 0 else 0.0

st.write(f"**Adjusted Total Tuition (User Adjusted):** {format_currency(adjusted_total_tuition)}")
st.write(f"*(The total tuition revenue based on user-adjusted tuition rates and student numbers.)*")

st.write(f"**Adjusted Tuition Assistance Ratio:** {tuition_assistance_ratio_adjusted:.2f}%")
st.write(f"*(Revised percentage of tuition revenue allocated for financial aid support.)*")

st.write(f"**Adjusted Income to Expense (I/E) Ratio:** {income_to_expense_ratio_adjusted:.2f}%")
st.write(f"*(The proportion of total adjusted income relative to the planned expense budget.)*")

st.write(f"**Tuition Rate Increase (Adjusted):** {tuition_rate_increase_adjusted:.2f}%")
st.write(f"*(The percentage increase in tuition revenue after user adjustments to the rates.)*")

# Download Tuition Rate Summary
csv_buffer = StringIO()
adjusted_grades_df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

st.download_button(
    label="Download Tuition Rate Summary",
    data=csv_data,
    file_name="tuition_rate_summary.csv",
    mime="text/csv",
)
