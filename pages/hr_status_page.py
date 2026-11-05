import plotly.express as px
from pathlib import Path
import streamlit as st
import polars as pl
import sys


# Setup path for importing hr_analysis module
root_path = str(Path(__file__).resolve().parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)


from src.hr_analysis import (
    employees_details,
    employee_growth,
    shift_wise_emp_stats,
    salary_payments_by_month,
    salary_payments
)


# Setup refresh button to update dashboard data
if st.button("Refresh", help="Click refresh if database is updated or after insert data related to this page."):
    # Clear all cache
    employees_details.clear()
    employee_growth.clear()
    shift_wise_emp_stats.clear()
    salary_payments_by_month.clear()
    salary_payments.clear()

    # Rerun function and collect new data
    st.rerun()


# This table contains details about employees
df_emp = employees_details().sort("employee_id")

# This table contains employee count for every month
df_emp_grow = employee_growth()

# This table contains total employee count and salary for every shift
df_shift_wise = shift_wise_emp_stats()

# Salary payment history for every month
df_pay_month = salary_payments_by_month()

# This table contains salary payment details
df_payments = salary_payments()


# --- Create charts ---

# This bar chart shows employee count for every shift
def emp_count_chart():
    fig = px.bar(
        data_frame=df_shift_wise,
        x="shift_name",
        y="total_employees",
        color="shift_name",
        title="Total Employees For Every Shift"
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False
    )

    return fig


# This histogram chart shows employee count by age group
def age_hist_chart():
    fig = px.histogram(
        data_frame=df_emp,
        x="age",
        nbins=3,
        title="Employees Count By Age Group",
        color_discrete_sequence=["#636EFA"]
    )

    fig.update_layout(
        title_font_size=20
    )

    return fig


# This line chart represents employees joined for every month
def emp_join_chart_month():
    fig = px.line(
        data_frame=df_emp_grow,
        x="month_name",
        y="total_employees",
        title="Employees Joined Per Month",
        markers=True
    )

    fig.update_layout(
        title_font_size=20,
        hovermode="x unified",
        plot_bgcolor="rgba(200,200,200,0.2)",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.3)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.3)")

    return fig


# This line chart represents employee salary for every month
def emp_salary_payment_month():
    fig = px.line(
        data_frame=df_pay_month,
        x="month_name",
        y="total_salary",
        title="Salary Payments For Every Month",
        markers=True
    )

    fig.update_layout(
        title_font_size=20,
        hovermode="x unified",
        plot_bgcolor="rgba(200,200,200,0.2)",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.3)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.3)")

    return fig




st.title("HR & Operational Efficiency")
st.divider()


# --- KPI Part ---

# Setup columns
total_emp, total_salary, emp_avg_salary = st.columns(3)

# Calculate active total employees and total salary
emp_count = df_shift_wise["total_employees"].sum() if len(df_shift_wise) > 0 else 0
emp_salary = df_shift_wise["total_salary"].sum() if len(df_shift_wise) > 0 else 0

# Calculate active employees average salary
avg_salary = (emp_salary / emp_count) if emp_count > 0 else 0


with total_emp:
    with st.container(border=True):
        st.metric(
            "Total Employees",
            emp_count
        )

with total_salary:
    with st.container(border=True):
        st.metric(
            "Total Salary",
            emp_salary
        )

with emp_avg_salary:
    with st.container(border=True):
        st.metric(
            "Average Salary",
            round(avg_salary, 2)
        )


# ---- Table ----
tables, charts = st.tabs(["Tables", "Charts"])

with tables:
    st.header("Employees Details")

    # Setup filter option checkbox
    if st.checkbox("Filter Option", help="Using filter option you can filter employees data by selecting employee role_name"):

        # Extract all role names
        options = (
            df_emp["role_name"]
            .drop_nulls()
            .unique()
            .sort()
            .to_list()
        )

        # Setup for selectbox
        selected = st.selectbox("Select Role Name", options)

        # Extract only selected active employees
        df_emp_display = df_emp.filter(
            (pl.col("role_name") == selected),
            (pl.col("act_stat"))
        )

        st.dataframe(df_emp_display)
    else:

        # Extract all active employees
        df_emp_display = df_emp.filter(
            (pl.col("act_stat"))
        )

        st.dataframe(df_emp_display)


    st.header("Last 10 Salary Payments")

    # Extract last 10 salary payments
    df_recent_payments = (
        df_payments
        .sort(by="payment_date", descending=True)
        .head(10)
    )

    st.dataframe(df_recent_payments)


with charts:

    # Setup columns
    bar, hist = st.columns(2)

    with bar:
        with st.container(border=True):
            shift_emp_count = emp_count_chart()
            st.plotly_chart(shift_emp_count)


    with hist:
        with st.container(border=True):
            age_group = age_hist_chart()
            st.plotly_chart(age_group)


    with st.container(border=True):
        count_emp = emp_join_chart_month()
        st.plotly_chart(count_emp, key="employees_count")


    with st.container(border=True):
        pay_stat = emp_salary_payment_month()
        st.plotly_chart(pay_stat, key="payments")
