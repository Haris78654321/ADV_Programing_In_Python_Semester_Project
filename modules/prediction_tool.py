import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from data.clean_data import load_and_clean_data

def app():
    st.title("🚗 Car Value & Efficiency Prediction")

    df = load_and_clean_data()

    st.subheader("🔍 Select Target to Predict")
    prediction_target = st.selectbox("What do you want to predict?", options=["MSRP", "City MPG", "Highway MPG"])

    numeric_features = ['Engine HP', 'Engine Cylinders', 'Year']
    categorical_features = ['Vehicle Size', 'Make']
    target_map = {
        "MSRP": "MSRP",
        "City MPG": "city mpg",
        "Highway MPG": "highway MPG"
    }
    target = target_map[prediction_target]

    df = df.dropna(subset=numeric_features + categorical_features + [target])

    X_num = df[numeric_features]
    X_cat = df[categorical_features]
    y = df[target]

    X_cat_encoded = pd.get_dummies(X_cat, drop_first=True)
    X = pd.concat([X_num.reset_index(drop=True), X_cat_encoded.reset_index(drop=True)], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    st.write(f"Model Mean Squared Error for {prediction_target}: {mse:,.2f}")

    st.subheader("🎯 Try It Yourself: Predict")

    engine_hp = st.slider("Engine HP", int(df['Engine HP'].min()), int(df['Engine HP'].max()), 250)
    engine_cyl = st.selectbox("Engine Cylinders", sorted(df['Engine Cylinders'].dropna().unique()))
    year = st.slider("Year", int(df['Year'].min()), int(df['Year'].max()), 2020)
    vehicle_size = st.selectbox("Vehicle Size", sorted(df['Vehicle Size'].dropna().unique()))
    make = st.selectbox("Make", sorted(df['Make'].dropna().unique()))

    input_num = pd.DataFrame([[engine_hp, engine_cyl, year]], columns=numeric_features)
    input_cat = pd.DataFrame([[vehicle_size, make]], columns=categorical_features)
    input_cat_encoded = pd.get_dummies(input_cat)
    input_cat_encoded = input_cat_encoded.reindex(columns=X_cat_encoded.columns, fill_value=0)
    input_data = pd.concat([input_num, input_cat_encoded], axis=1)

    if st.button(f"Predict {prediction_target}"):
        prediction = model.predict(input_data)[0]
        suffix = "$" if prediction_target == "MSRP" else " MPG"
        st.success(f"Estimated {prediction_target}: {prediction:,.2f}{suffix}")
