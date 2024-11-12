import streamlit as st
import pandas as pd
import locale

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

# Streamlit App Start
st.title("Tuition and Expense Planning Tool")

# ... (Previous code remains unchanged for brevity)

if st.button("View Results"):
    st.subheader("Initial Projected Tuition Increase")
    st.table(grades_df)

    # Real-time metrics after results
    projected_total_tuition = grades_df["Total Projected Tuition"].sum()
    tuition_assistance_ratio_projected = (financial_aid / projected_total_tuition) * 100 if projected_total_tuition > 0 else 0.0
    income_to_expense_ratio_projected = (projected_total_tuition / new_expense_budget) * 100 if new_expense_budget > 0 else 0.0
    tuition_rate_increase_projected = ((projected_total_tuition - current_total_tuition) / current_total_tuition) * 100 if current_total_tuition > 0 else 0.0

    # Projected Results with Explanations
    st.subheader("Projected Results")
    
    results_projected = {
        "Metric": ["Current Total Tuition", "Projected Total Tuition", "Tuition Assistance Ratio", "Income to Expense Ratio", "Tuition Rate Increase"],
        "Value": [
            format_currency(current_total_tuition),
            format_currency(projected_total_tuition),
            f"{tuition_assistance_ratio_projected:.2f}%",
            f"{income_to_expense_ratio_projected:.2f}%",
            f"{tuition_rate_increase_projected:.2f}%"
        ],
        "Explanation": [
            "Total tuition revenue currently collected across all grades.",
            "Estimated revenue after applying the calculated percentage increase.",
            "Percentage of tuition revenue allocated to financial aid.",
            "Whether projected tuition revenue covers expenses.",
            "Percentage growth in revenue due to projected tuition changes."
        ]
    }
    
    st.table(pd.DataFrame(results_projected))

# ... (User adjustments for tuition per grade level)

# Adjusted Results with Explanations
st.subheader("Adjusted Results")
    
results_adjusted = {
    "Metric": ["Adjusted Total Tuition", "Adjusted Tuition Assistance Ratio", "Adjusted Income to Expense Ratio", "Adjusted Tuition Rate Increase"],
    "Value": [
        format_currency(adjusted_total_tuition),
        f"{tuition_assistance_ratio_adjusted:.2f}%",
        f"{income_to_expense_ratio_adjusted:.2f}%",
        f"{tuition_rate_increase_adjusted:.2f}%"
    ],
    "Explanation": [
        "Revenue based on user-defined tuition rate adjustments.",
        "Percentage of adjusted tuition revenue allocated to financial aid.",
        "Whether adjusted tuition revenue covers expenses.",
        "Percentage increase in tuition revenue based on adjustments."
    ]
}
    
st.table(pd.DataFrame(results_adjusted))

# Print Button
if st.button("Print Results"):
    st.markdown("### Print this page for records:")
    st.write("Please use your browser's print function (Ctrl+P or Cmd+P) to print this page.")
