from src.data_loader import load_data_from_db
from pathlib import Path
import streamlit as st
import polars as pl
import sys


@st.cache_data()
def employees_details():
    """This function is used to collect employee details."""

    query = """
        SELECT e.employee_id, e.role_id, e.shift_id, e.name, e.username, e.email, e.age, e.current_salary,
        r.role_name, s.shift_name, e.join_date, e.act_stat, s.start_time, s.end_time
        FROM hr.employees AS e
        JOIN hr.job_roles AS r USING(role_id)
        JOIN hr.shifts AS s USING(shift_id)
    """

    return load_data_from_db(query)


@st.cache_data()
def salary_payments():
    """This function returns a table that contains employees' salary payment history."""

    query = """
        SELECT e.name, e.username, j.role_name, p.salary,
            p.pay_type, p.account_company, p.payment_date
        FROM hr.payments_history AS p
        JOIN hr.employees AS e USING(employee_id)
        JOIN hr.job_roles AS j
            ON j.role_id = p.role_id
    """

    return load_data_from_db(query)


@st.cache_data()
def employee_growth():
    """This calculates total employees joined for every month in chronological order."""

    df = (
        employees_details()
        # extract month number and month name
        .with_columns(
            pl.col("join_date").dt.month().alias("month_num"),
            pl.col("join_date").dt.to_string("%B").alias("month_name")
        )
        # calculate total employees for every month
        .group_by(["month_num", "month_name"]).agg(
            pl.col("employee_id").count().alias("total_employees"),
        )
        .sort(by="month_num")
        .select(["month_name", "total_employees"])
    )

    return df


@st.cache_data()
def salary_payments_by_month():
    """This function returns a table that contains month_name and total_salary for every month in chronological order."""

    query = """
        SELECT salary, payment_date
        FROM hr.payments_history
    """

    df = (
        load_data_from_db(query)
        # extract month number and month name
        .with_columns(
            pl.col("payment_date").dt.month().alias("month_num"),
            pl.col("payment_date").dt.to_string("%B").alias("month_name")
        )
        # calculate total salary for every month
        .group_by(["month_num", "month_name"]).agg(
            pl.col("salary").sum().alias("total_salary")
        )
        .sort(by="month_num")
        .select(["month_name", "total_salary"])
    )

    return df


@st.cache_data()
def shift_wise_emp_stats():
    """This function returns a table that contains total salary and total active employees by shift."""

    df = (
        employees_details().group_by("shift_name").agg(
            # count active employees for every shift
            pl.when(pl.col("act_stat"))
            .then(1)
            .otherwise(0)
            .sum()
            .alias("total_employees"),

            # calculate total salary for every shift for active employees
            pl.when(pl.col("act_stat"))
            .then(pl.col("current_salary"))
            .otherwise(0)
            .sum()
            .alias("total_salary")
        )
    )

    return df
