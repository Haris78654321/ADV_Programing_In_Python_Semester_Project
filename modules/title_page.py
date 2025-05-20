import streamlit as st
from PIL import Image

def app():
    st.markdown("""
        <style>
        .title-container {
            text-align: center;
            padding: 50px 20px 10px 20px;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-top: 0.1px;
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
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="title-container">
            <div class="title-text">Interactive Dashboard on Car Dataset</div>
            <div class="subtitle-text">Final Project | Advanced Python Programming</div>
            <div class="group-title">Group Members:</div>
            <div class="member">1. Muhammad Haris Zaman</div>
            <div class="member">2. Fahad Khan</div>
            <div class="member">3. Muhammad Abrar Baig</div>
        </div>
    """, unsafe_allow_html=True)
