from src.data_loader import load_data_from_db
import streamlit as st
import polars as pl


@st.cache_data()
def total_spending_per_donut():
    """This function calculates total spending per donut."""

    donut_spending = """
        SELECT donut_id,
            ROUND(SUM(price_per_unit * ingred_quantity_needed), 2) AS total_spending
        FROM inventory.donut_ingreds
        INNER JOIN inventory.ingredients USING(ingred_id)
        GROUP BY donut_id
    """
    return load_data_from_db(donut_spending)


@st.cache_data()
def total_sales():
    """This function returns total_sale, donut_name, donut_id, sale_quantity."""

    donut_sale = """
        SELECT name, donut_id,
            SUM(sale_quantity) AS sale_quantity,
            SUM(sub_total) AS total_sale
        FROM sales.sale_items
        INNER JOIN inventory.donuts USING(donut_id)
        GROUP BY name, donut_id
        ORDER BY donut_id
    """
    return load_data_from_db(donut_sale)


@st.cache_data()
def total_revenue_cal():
    """This function shows total spending, revenue, and profit for every donut."""

    df_spend = total_spending_per_donut()
    df_sale = total_sales()

    df = (
        # join df_sale table with df_spend table
        df_sale.join(df_spend, on="donut_id", how="inner")
        .with_columns([
            # calculate total spending for total sale_quantity
            (pl.col("sale_quantity") * pl.col("total_spending")).alias("total_spending"),

            # calculate total profit after deducting spending
            (pl.col("total_sale") - (pl.col("sale_quantity") * pl.col("total_spending"))).alias("total_profit")
        ])
        .select(["donut_id", "name", "sale_quantity", "total_spending", "total_sale", "total_profit"])
        .sort(by="sale_quantity", descending=True)
    )

    return df


@st.cache_data()
def categorie_wise():
    """This function returns table that contains total sale quantity, total_profit by category."""

    # load categories table from database
    query = """
        SELECT cat_id, donut_id, categorie
        FROM inventory.categories
        JOIN inventory.donuts USING(cat_id)
    """
    df_categories = load_data_from_db(query)
    df_donut_summary = total_revenue_cal()

    df = (
        df_categories.join(df_donut_summary, on="donut_id")
        .group_by("categorie").agg(
            sale_quantity=pl.col("sale_quantity").sum(),
            total_profit=pl.col("total_profit").sum()
        )
        .sort(by="sale_quantity", descending=True)
    )

    return df


@st.cache_data()
def sale_by_discount():
    """
    This function calculates sales when a discount is running
    versus sales without any discount.
    """

    query = """
        SELECT *
        FROM sales.sales
        JOIN sales.sale_items USING(sale_id)
        LEFT JOIN inventory.discounts USING(donut_id)
        WHERE sale_stat = 'completed'
    """

    df_row = load_data_from_db(query)

    # mark True if sale date is within discount date range, else False
    df_with_flag = df_row.with_columns(
        pl.when(
            pl.col("discount_percent").is_not_null() &
            pl.col("sale_date").is_between(pl.col("start_date"), pl.col("end_date"))
        )
        .then(True)
        .otherwise(False)
        .alias("is_discount_active")
    )

    df = df_with_flag.group_by("donut_id").agg(
        # calculate sale quantity with discount
        pl.when(pl.col("is_discount_active"))
        .then(pl.col("sale_quantity"))
        .otherwise(0)
        .sum()
        .alias("with_discount_sale"),

        # calculate sale quantity without discount
        pl.when(~pl.col("is_discount_active"))
        .then(pl.col("sale_quantity"))
        .otherwise(0)
        .sum()
        .alias("without_discount_sale")
    )
    return df


@st.cache_data()
def sale_by_month_day():
    """This function returns daily sales aggregated by date, month, and day."""

    query = """
        SELECT *
        FROM sales.sales
        JOIN sales.sale_items USING(sale_id)
    """

    df_row = load_data_from_db(query)

    df = (
        # extract month and day as numbers
        df_row.with_columns(
            pl.col("sale_date").dt.month().alias("sale_month"),
            pl.col("sale_date").dt.day().alias("sale_day")
        )
        # calculate total sale quantity and revenue by date
        .group_by(["sale_date", "sale_month", "sale_day"]).agg(
            pl.col("sale_quantity").sum().alias("total_sale_count"),
            pl.col("sub_total").sum().alias("total_revenue")
        )
        .sort(by="sale_date")
        .select(["sale_date", "sale_month", "sale_day", "total_sale_count", "total_revenue"])
    )

    return df
