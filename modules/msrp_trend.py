import streamlit as st
import pandas as pd
import plotly.express as px
from data.clean_data import load_and_clean_data


def app():
    df = load_and_clean_data()

    st.title("📉 Trend: Average MSRP Over the Years")
    st.sidebar.header("Filter Trend Plot")

    trend_make = st.sidebar.multiselect("Select Make (Company)", options=df["Make"].unique(), default=list(df["Make"].unique()))
    trend_vehicle_style = st.sidebar.multiselect("Select Vehicle Style", options=df["Vehicle Style"].unique(), default=list(df["Vehicle Style"].unique()))
    trend_origin = st.sidebar.multiselect("Select Origin", options=df["Origin"].unique(), default=list(df["Origin"].unique()))

    if trend_make:
        df = df[df["Make"].isin(trend_make)]
    if trend_vehicle_style:
        df = df[df["Vehicle Style"].isin(trend_vehicle_style)]
    if trend_origin:
        df = df[df["Origin"].isin(trend_origin)]

    msrp_trend = df.groupby("Year", as_index=False)["MSRP"].mean()

    fig = px.line(msrp_trend, x="Year", y="MSRP", title="Average MSRP Over the Years", markers=True)
    st.plotly_chart(fig, use_container_width=True)
