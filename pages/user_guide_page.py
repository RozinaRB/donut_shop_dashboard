import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="User Guide - Donut Shop",
    page_icon="📖",
    layout="wide"
)

root_path = Path(__file__).resolve().parent
guide_file_path = root_path / "USER_GUIDE.md"


if guide_file_path.exists():
    with open(guide_file_path, "r", encoding="utf-8") as f:
        guide_content = f.read()

    # Display file content as markdown
    st.markdown(guide_content, unsafe_allow_html=True)

else:
    st.error("User Guide not found!")
