import streamlit as st
import page1
import page2
import page3

PAGES = {
    "Data Filter": page1,
    "Performance Analysis": page2,
    "Price & Market Trends": page3
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()