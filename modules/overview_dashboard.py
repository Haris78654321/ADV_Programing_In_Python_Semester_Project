import streamlit as st
import pandas as pd
import plotly.express as px
from data.clean_data import load_and_clean_data


def app():
    df = load_and_clean_data()

    st.sidebar.header("Filter Cars")
    
    # Make filter
    selected_make = st.sidebar.multiselect("Select Make", options=df["Make"].unique(), default=None)

    # Year input range
    min_year = int(df["Year"].min())
    max_year = int(df["Year"].max())

    st.sidebar.markdown(f"📅 **Enter a year range between {min_year} and {max_year}:**")
    start_year = st.sidebar.number_input("Start Year", min_value=min_year, max_value=max_year, value=min_year)
    end_year = st.sidebar.number_input("End Year", min_value=min_year, max_value=max_year, value=max_year)

    if start_year > end_year:
        st.sidebar.error("⚠️ Start year must be less than or equal to end year.")

    # Apply filters
    filtered_df = df[
        ((df["Make"].isin(selected_make)) if selected_make else True) &
        (df["Year"].between(start_year, end_year))
    ]

    st.title("🚗 Car Performance Analysis")

    # Scatter plot: Engine HP vs MSRP
    with st.expander("📈 Engine HP vs MSRP"):
        fig1 = px.scatter(filtered_df, x="Engine HP", y="MSRP", color="Make", size="Popularity",
                          hover_data=["Model", "Year", "Vehicle Style"],
                          title="Engine HP vs MSRP")
        st.plotly_chart(fig1, use_container_width=True)

    # Metric selector
    metrics = {
        "Horsepower": "Engine HP",
        "City MPG": "city mpg",
        "Highway MPG": "highway MPG",
        "MSRP": "MSRP"
    }
    selected_metric = st.selectbox("Select Performance Metric", options=list(metrics.keys()))

    # Box plot: Vehicle Size vs selected metric
    with st.expander("🚙 Box Plot: Performance by Vehicle Size"):
        fig3 = px.box(filtered_df, x="Vehicle Size", y=metrics[selected_metric], color="Vehicle Size",
                      title=f"{selected_metric} by Vehicle Size")
        st.plotly_chart(fig3, use_container_width=True)

    # Top 10 makes by average HP
    with st.expander("🏁 Top 10 Makes by Horsepower"):
        top_hp = (filtered_df.groupby("Make", as_index=False)["Engine HP"]
                  .mean().sort_values("Engine HP", ascending=False).head(10))
        fig5 = px.bar(top_hp, x="Make", y="Engine HP", color="Make",
                      title="Top 10 Makes by Average Horsepower")
        st.plotly_chart(fig5, use_container_width=True)

    # Pie chart: Vehicle Style Distribution
    with st.expander("📊 Vehicle Style Distribution"):
        fig6 = px.pie(filtered_df, names="Vehicle Style", title="Distribution of Vehicle Styles", hole=0.3)
        st.plotly_chart(fig6, use_container_width=True)
