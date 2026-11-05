import streamlit as st


# Setup for pages
user_guide = st.Page(
    page="./pages/user_guide_page.py",
    title="User Guide"
)

sale_revenue = st.Page(
    page="./pages/sales_revenue_page.py",
    title="Sales & Revenue"
)

inv_manage = st.Page(
    page="./pages/inv_manage_waste_page.py",
    title="Inventory"
)

hr_status = st.Page(
    page="./pages/hr_status_page.py",
    title="Employee Status"
)


# Setup navigation sidebar
pages = st.navigation([user_guide, sale_revenue, inv_manage, hr_status])

# Run dashboard
pages.run()
