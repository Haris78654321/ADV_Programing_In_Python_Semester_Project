# 🚗 Car Data Analytics Dashboard

An interactive Streamlit web application for analyzing and predicting car data using visualizations and machine learning.

---

## 🎯 Project Purpose

This project provides users with an intuitive dashboard to explore a comprehensive dataset of cars. It allows for:
- **Data Exploration** through filters and maps.
- **Trend Analysis** of MSRP over the years.
- **Visual Insights** into performance metrics.
- **Machine Learning Predictions** for MSRP, City MPG, and Highway MPG.

The goal is to help users and analysts discover patterns in the automotive market and make informed predictions based on user-selected features.

---

## 📊 Dataset Description

The dataset contains various attributes of cars manufactured by different companies from different regions around the world. Key features include:

- **General Info**: Make, Model, Year, Country of Origin
- **Engine**: Horsepower, Cylinders, Fuel Type
- **Specifications**: Transmission Type, Drivetrain, Vehicle Size & Style
- **Performance**: City MPG, Highway MPG, Popularity, MSRP
- **Market Information**: Market Category, Origin

Raw data is cleaned and preprocessed in the `data/clean_data.py` module.

---

## 🌟 Major Features

### 1. 🔍 **Data Explorer**
- Filter cars by Make, Origin, Fuel Type, Year, Horsepower, and more
- Visualize origin distribution on an interactive world map
- Breakdown of selected car models
- Export filtered results to Excel

### 2. 📊 **Overview Dashboard**
- Scatter plot: Engine Horsepower vs MSRP
- Box plot: MPG by vehicle size
- Bar chart: Top 10 car makes by average horsepower
- Pie chart: Vehicle style distribution

### 3. 📈 **MSRP Trend Analysis**
- View average MSRP changes across years
- Analyze trends by make, vehicle style, and origin

### 4. 🤖 **ML Price & MPG Predictor**
- Predict MSRP, City MPG, or Highway MPG
- Select input parameters using sliders and dropdowns
- Random Forest Regression model with prediction error displayed

---
📦 Dependencies

All dependencies are listed 

    streamlit>=1.30.0
    pandas>=1.5.0
    numpy>=1.23.0
    plotly>=5.18.0
    scikit-learn>=1.3.0
    openpyxl>=3.1.0

Install them using:

    pip install -r requirements.txt

🧠 Technologies Used
    
    Python

    Streamlit for UI

    Pandas / NumPy for data wrangling

    Plotly for interactive charts

    Scikit-learn for machine learning

    OpenPyXL for Excel export

