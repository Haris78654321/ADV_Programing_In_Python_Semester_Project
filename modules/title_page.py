# modules/title_page.py

import streamlit as st

def app():
    st.markdown("""
        <style>
        .title-container {
            text-align: center;
            padding: 50px 20px 10px 20px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-top: 40px;
        }
        .title-text {
            font-size: 42px;
            font-weight: 700;
            color: #003366;
            margin-bottom: 10px;
        }
        .subtitle-text {
            font-size: 20px;
            color: #555;
            margin-bottom: 30px;
        }
        .group-title {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 5px;
            color: #003366;
        }
        .member {
            font-size: 18px;
            color: #333;
        }
        .logo {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 120px;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<img class="logo" src="https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/National_University_of_Sciences_and_Technology_logo.svg/1200px-National_University_of_Sciences_and_Technology_logo.svg.png" alt="NUST Logo">',
        unsafe_allow_html=True
    )

    st.markdown("""
        <div class="title-container">
            <div class="title-text">Interactive Dashboard on Car Dataset</div>
            <div class="subtitle-text">Final Project | Master’s in Data Science & AI</div>
            <div class="group-title">Group Members:</div>
            <div class="member">1. Harish Zaman</div>
            <div class="member">2. Fahad Khan</div>
            <div class="member">3. Abrar</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚗 Enter the Dashboard"):
        st.success("Use the left sidebar to navigate through the dashboard sections.")
