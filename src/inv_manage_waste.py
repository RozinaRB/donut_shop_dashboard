from src.data_loader import load_data_from_db
from pathlib import Path
import streamlit as st
import polars as pl
import sys


@st.cache_data()
def ingred_purchases():
    """This function returns a table that contains full purchase history."""

    query = """
        SELECT i.name AS ingred_name, s.name AS supplier_name,
            p.quantity_bought, p.price_per_unit, i.unit_name,
            (p.quantity_bought * p.price_per_unit) AS total_price,
            p.purchase_date
        FROM inventory.suppliers AS s
        JOIN inventory.purchases AS p USING(supplier_id)
        JOIN inventory.ingredients AS i USING(ingred_id)
    """

    return load_data_from_db(query)


@st.cache_data()
def ingred_stock():
    """This function returns a table that contains ingred_name, ingred_current_stock, ingred_required_level."""

    query = """
        SELECT ingred_id, name, current_stock_level,
            min_required_level, unit_name
        FROM inventory.ingred_stock
        JOIN inventory.ingredients USING(ingred_id)
    """

    return load_data_from_db(query)


@st.cache_data()
def donut_waste():
    """This function returns waste records with donut_id, name, quantity, and date."""

    query = """
        SELECT d.donut_id, d.name, w.quantity, d.price, w.date,
            w.quantity * d.price AS lose_price
        FROM inventory.waste_logs AS w
        JOIN inventory.donuts AS d USING(donut_id)
    """

    df = load_data_from_db(query).with_columns(
        pl.col("date").dt.month().alias("month_num"),
        pl.col("date").dt.to_string("%B").alias("month_name")
    )

    return df


@st.cache_data()
def donut_waste_by_month():
    """This function calculates donut waste quantity by month ordered chronologically."""

    df = (
        donut_waste()
        .group_by(["month_num", "month_name"])
        .agg(
            pl.col("quantity").sum().alias("waste_quantity"),
            pl.col("lose_price").sum().alias("total_lose_price")
        )
        .sort(by="month_num")
    )

    return df


@st.cache_data()
def donut_waste_by_name():
    """This function calculates donut waste quantity by donut_name."""

    df = (
        donut_waste()
        .group_by("name")
        .agg(
            pl.col("donut_id").first().alias("donut_id"),
            pl.col("quantity").sum().alias("waste_quantity"),
            pl.col("lose_price").sum().alias("total_lose_price")
        )
        .sort(by="waste_quantity", descending=True)
    )

    return df


@st.cache_data()
def supplier_purchases():
    """This function returns purchase summary by supplier."""

    query = """
        SELECT name AS supplier_name, quantity_bought, price_per_unit,
            quantity_bought * price_per_unit AS total_price
        FROM inventory.purchases
        JOIN inventory.suppliers USING(supplier_id)
    """

    df = (
        load_data_from_db(query)
        .group_by("supplier_name").agg(
            pl.col("total_price").sum().alias("total_price")
        )
    )

    return df
