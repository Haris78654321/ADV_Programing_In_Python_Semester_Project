import streamlit as st
from modules import data_explorer, overview_dashboard, msrp_trend, prediction_tool

st.set_page_config(page_title="Car Analytics Dashboard", layout="wide")


PAGES = {
    "🔎 Data Explorer": data_explorer,
    "📊 Overview Dashboard": overview_dashboard,
    "📈 MSRP Trend Analysis": msrp_trend,
    "🤖 ML Price & MPG Predictor": prediction_tool
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()