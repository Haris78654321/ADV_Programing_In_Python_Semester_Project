import streamlit as st
import pandas as pd
import plotly.express as px
from data.clean_data import load_and_clean_data

def app():
    st.title("Vehicle Price & Market Trends")
    
    # Load data
    df = load_and_clean_data()
    
    # Sidebar filters
    st.sidebar.header("Price Analysis Filters")
    
    # Basic filters
    price_range = st.sidebar.slider(
        "MSRP Range ($)",
        min_value=int(df["MSRP"].min()),
        max_value=int(df["MSRP"].max()),
        value=(int(df["MSRP"].quantile(0.25)), int(df["MSRP"].quantile(0.75)))
    )
    
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(2010, 2020)
    )
    
    # Apply filters
    filtered_df = df[
        (df["MSRP"].between(price_range[0], price_range[1])) &
        (df["Year"].between(year_range[0], year_range[1]))
    ]
    
    if filtered_df.empty:
        st.warning("No vehicles match your price/year filters")
        return
    
    # Section 1: Price Distribution
    st.header("1. Price Distribution Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.histogram(
            filtered_df,
            x="MSRP",
            nbins=50,
            title="Price Distribution",
            color_discrete_sequence=["#636EFA"]
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.box(
            filtered_df,
            x="Vehicle Style",
            y="MSRP",
            title="Price by Vehicle Style",
            color="Vehicle Style"
        )
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Section 2: Market Trends
    st.header("2. Market Trends Over Time")
    
    col3, col4 = st.columns(2)
    with col3:
        trend_data = filtered_df.groupby("Year").agg({
            "MSRP": "mean",
            "Make": "count"
        }).reset_index()
        
        fig3 = px.line(
            trend_data,
            x="Year",
            y="MSRP",
            title="Average Price Trend",
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        fig4 = px.line(
            trend_data,
            x="Year",
            y="Make",
            title="Vehicle Count Trend",
            markers=True,
            color_discrete_sequence=["#EF553B"]
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Section 3: Price Correlations
    st.header("3. Price Correlations")
    
    col5, col6 = st.columns(2)
    with col5:
        fig5 = px.scatter(
            filtered_df,
            x="Engine HP",
            y="MSRP",
            color="Origin",
            title="HP vs Price",
            trendline="ols"
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col6:
        fig6 = px.scatter(
            filtered_df,
            x="highway MPG",
            y="MSRP",
            color="Vehicle Size",
            title="Fuel Efficiency vs Price",
            trendline="ols"
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # Section 4: Top Models Table
    st.header("4. Top Priced Models")
    top_models = filtered_df.nlargest(10, "MSRP")[["Make", "Model", "Year", "MSRP", "Origin"]]
    st.dataframe(top_models.style.format({"MSRP": "${:,.2f}"}))

if __name__ == "__main__":
    app()