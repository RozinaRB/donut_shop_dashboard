import sys
import polars as pl
import streamlit as st
from pathlib import Path
import plotly.express as px


# Helper to import module from src directory
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))


# Import all analysis from src/sales_revenue_ana file
from src.sales_revenue_ana import (
    total_revenue_cal,
    categorie_wise,
    sale_by_discount,
    sale_by_month_day
)


# Setup button for refresh full page
if st.button("Refresh", help="Click refresh if database is updated or after insert data related to this page."):
    # Clear all cache
    total_revenue_cal.clear()
    categorie_wise.clear()
    sale_by_discount.clear()
    sale_by_month_day.clear()

    # Rerun all functions
    st.rerun()


# This table contains columns with and without discount sale quantity
df_dis = sale_by_discount().sort(by="donut_id")

# This table has total revenue and profit per donut
df_rev_profit = total_revenue_cal()

# This table contains total sale quantity and total profit by category
df_cat_profit = categorie_wise()

# This table contains sale stats for every month and day
df_sale = sale_by_month_day()


# Extract month name as string
df_sale = df_sale.with_columns(
    pl.col("sale_date").dt.to_string("%B").alias("month_name")
)


# Analysis for showing monthly line chart (ordered chronologically)
df_sale_line = (
    df_sale.group_by(["sale_month", "month_name"]).agg(
        pl.col("total_sale_count").sum().alias("sale_quantity"),
        pl.col("total_revenue").sum().alias("total_revenue")
    )
    .sort(by="sale_month")
)




# ---- Visualization part ----

def line_chart_by_month():
    fig = px.line(
        data_frame=df_sale_line,
        x="month_name",
        y=["sale_quantity", "total_revenue"],
        title="Donut Sale Statistic By Month",
        markers=True
    )

    fig.update_layout(
        title_font_size=20,
        plot_bgcolor="rgba(200, 200, 200, 0.1)",
        hovermode="x unified",
        margin=dict(l=30, r=30, t=30, b=30)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.2)")

    return fig


# This bar chart shows donut sale stats
def donut_sale_bar_chart():
    fig = px.bar(
        data_frame=df_rev_profit,
        x="sale_quantity",
        y="name",
        color="name",
        title="Donuts Sale Statistic",
        text_auto=".1f",
        labels={
            "name": "donut_name"
        }
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",       # Makes chart background transparent
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig



# This donut chart shows sale quantity by category
def cat_donut_sale_quantity():
    fig = px.pie(
        data_frame=df_cat_profit,
        names="categorie",
        values="sale_quantity",
        title="Sale Quantity By Categories",
        hole=0.4
    )

    fig.update_traces(
        pull=[0.2, 0, 0],
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False,
        margin=dict(l=30, r=30, t=50, b=30)
    )

    return fig


# This donut chart shows sale profit by donut category
def cat_donut_chart():
    fig = px.pie(
        data_frame=df_cat_profit,
        names="categorie",
        values="total_profit",
        title="Profit By Category",
        hole=0.4
    )

    fig.update_traces(
        pull=[0.2, 0, 0],
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        title_font_size=20,
        showlegend=False,
        margin=dict(l=30, r=30, t=50, b=30)
    )

    return fig


# This chart shows total spending vs total profit per donut
def scatter_chart_spd_profit():
    fig = px.scatter(
        data_frame=df_rev_profit,
        x="total_spending",
        y="total_profit",
        color="name",
        hover_name="name",
        labels={
            "name": "donut_name"
        },
        title="Total Spending vs Total Profit Per Donut"
    )

    fig.update_layout(
        title_font_size=20,
        plot_bgcolor="rgba(200, 200, 200, 0.1)",
        margin=dict(l=30, r=30, t=50, b=30)
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.2)")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.2)")

    return fig




# ---- Interface part ----

st.title("Sales Revenue Analysis")
st.divider()


# Calculate total profit and quantity for all donuts
df_total_profit = df_rev_profit["total_profit"].sum() if len(df_rev_profit) > 0 else 0
df_total_quantity = df_rev_profit["sale_quantity"].sum() if len(df_rev_profit) > 0 else 0

# Extract top selling donut name safely
top_selling_donut = df_rev_profit["name"][0] if len(df_rev_profit) > 0 else "N/A"


# Show data in columns block
quantity, profit, top_donut = st.columns(3)

with top_donut:
    with st.container(border=True):
        st.metric(
            "Top Selling Donut",
            f"{top_selling_donut}"
        )

with quantity:
    with st.container(border=True):
        st.metric(
            "Total Quantity Sold",
            f"{df_total_quantity}"
        )

with profit:
    with st.container(border=True):
        st.metric(
            "Total Profit",
            f"${round(df_total_profit, 2)}"
        )


# Setup tabs to organize tables and charts
tables, charts = st.tabs(["Tables", "Charts"])

with tables:
    st.header("Sale Statistic With and Without Discount")
    st.dataframe(df_dis)


    st.header("Donut Statistic By Sale Date and Month")
    # Extract all month names
    month_names = (
        df_sale["month_name"]
        .drop_nulls()
        .unique()
        .to_list()
    )
    # Setup selectbox
    selected_month = st.selectbox(
        label="Select Month",
        options=month_names,
        help="Using this you can filter data by month name"
    )
    # Filter data selected by the user by month and select necessary columns
    df_sale_filtered = (
        df_sale.filter(
            pl.col("month_name") == selected_month
        ).with_columns(
            pl.col("total_sale_count").alias("total_sale_quantity")
        ).select(["sale_date", "total_sale_quantity", "total_revenue"])
    )
    st.dataframe(df_sale_filtered)




with charts:
    # Monthly sales trend
    with st.container(border=True):
        line_fig = line_chart_by_month()
        st.plotly_chart(line_fig)


    # Scatter chart for spending and profit
    with st.container(border=True):
        scatter_fig = scatter_chart_spd_profit()
        st.plotly_chart(scatter_fig)


    # Bar chart showing statistic by donut
    with st.container(border=True):
        bar_fig = donut_sale_bar_chart()
        st.plotly_chart(bar_fig)


    # Donut charts for category breakdown
    profit_col, quantity_col = st.columns(2)

    with profit_col:
        with st.container(border=True):
            donut_fig = cat_donut_chart()
            st.plotly_chart(donut_fig)

    with quantity_col:
        with st.container(border=True):
            donut_fig = cat_donut_sale_quantity()
            st.plotly_chart(donut_fig)
