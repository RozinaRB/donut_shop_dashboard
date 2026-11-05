import plotly.express as px
from pathlib import Path
import streamlit as st
import polars as pl
import sys


# Setup path for importing inv_manage_waste module
root_path = str(Path(__file__).resolve().parent.parent)
if root_path not in sys.path:
    sys.path.append(root_path)


from src.inv_manage_waste import (
    ingred_purchases,
    donut_waste,
    ingred_stock,
    donut_waste_by_month,
    donut_waste_by_name,
    supplier_purchases
)


# Setup refresh button to update dashboard data
if st.button("Refresh", help="Click refresh if database is updated or after insert data related to this page."):
    # Clear all cache
    donut_waste.clear()
    ingred_purchases.clear()
    ingred_stock.clear()
    donut_waste_by_month.clear()
    donut_waste_by_name.clear()
    supplier_purchases.clear()

    # Rerun function and collect new data
    st.rerun()


# This table contains full purchases history
df_purchases = ingred_purchases()

# This table records waste
df_waste = donut_waste()

# This table contains donut waste statistics by month
df_waste_month = donut_waste_by_month()

# This table contains donut waste by donut_name
df_waste_name = donut_waste_by_name()

# This table contains all stock status
df_stock = ingred_stock()

# This table contains purchase summary for every supplier
df_supplier = supplier_purchases()


# This line chart shows donut waste statistics by month
def waste_month_line_chart():
    fig = px.line(
        data_frame=df_waste_month,
        x="month_name",
        y="total_lose_price",
        title="Donut Waste Stats For Every Month",
        markers=True
    )

    fig.update_layout(
        title_font_size=20,
        hovermode="x unified",
        plot_bgcolor="rgba(200,200,200,0.2)",
        margin=dict(l=30, r=30, t=30, b=30)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.3)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.3)")

    return fig


# This bar chart shows which donut is wasted most
def donut_waste_chart():
    fig = px.bar(
        data_frame=df_waste_name,
        x="name",
        y="waste_quantity",
        color="name",
        title="Donut Waste Status For Every Donut",
        text_auto=".2f",
        labels={
            "name": "donut_name"
        }
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False
    )

    return fig


# This bar chart shows ingredient current stock level and min required level
def stock_status_with_bar():
    fig = px.bar(
        data_frame=df_stock,
        x="name",
        y=["min_required_level", "current_stock_level"],
        title="Ingredients Stock Status",
        text_auto=".2f",
        labels={
            "name": "ingredient_name"
        }
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False
    )

    return fig


# This bar chart shows purchases status for every supplier
def ingred_purchase_chart():
    fig = px.bar(
        data_frame=df_supplier,
        x="supplier_name",
        y="total_price",
        color="supplier_name",
        title="Supplier Performance"
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False
    )

    return fig




st.title("Inventory & Food Waste Management")
st.divider()


# Calculate total purchases amount, waste quantity, loss amount
total_purchases = df_purchases["total_price"].sum() if len(df_purchases) > 0 else 0
total_waste = df_waste_month["waste_quantity"].sum() if len(df_waste_month) > 0 else 0
total_loss = df_waste_month["total_lose_price"].sum() if len(df_waste_month) > 0 else 0


# Setup columns
purchases, waste, loss = st.columns(3)

# Show in metric
with purchases:
    with st.container(border=True):
        st.metric(
            "Total Purchases Amount",
            f"${round(total_purchases)}"
        )

with waste:
    with st.container(border=True):
        st.metric(
            "Total Donut Waste Quantity",
            f"{total_waste}"
        )

with loss:
    with st.container(border=True):
        st.metric(
            "Total Loss Price",
            f"${round(total_loss, 2)}"
        )




# Setup tabs
tables, charts = st.tabs(["Tables", "Charts"])


# Show all tables
with tables:
    # Extract all month names
    month_names = (
        df_waste["month_name"]
        .drop_nulls()
        .unique()
        .to_list()
    )

    # Setup selectbox for filter
    month_name = st.selectbox(
        label="Select Month Name",
        options=month_names,
        help="Using this you can filter data by month name"
    )

    # Filter table and extract selected month details
    df_waste_display = (
        df_waste.filter(
            pl.col("month_name") == month_name
        )
        .select(["donut_id", "name", "quantity", "lose_price", "date"])
        .sort(by="date")
    )

    st.header("Donut Waste History")
    # Show data frame
    st.dataframe(df_waste_display)


    st.header("Full Purchases History")
    # Show full purchases history
    st.dataframe(df_purchases)


# Show all charts
with charts:
    with st.container(border=True):
        fig = waste_month_line_chart()
        st.plotly_chart(fig)


    with st.container(border=True):
        fig = donut_waste_chart()
        st.plotly_chart(fig)


    with st.container(border=True):
        fig = stock_status_with_bar()
        st.plotly_chart(fig)


    with st.container(border=True):
        fig = ingred_purchase_chart()
        st.plotly_chart(fig)
