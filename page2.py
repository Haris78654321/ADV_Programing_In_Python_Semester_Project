import streamlit as st
import pandas as pd
import plotly.express as px
from clean import load_and_clean_data

def app():
    st.title("Car Performance Analysis")
    df = load_and_clean_data()

    # Sidebar filters
    st.sidebar.header("Performance Filters")
    
    # Origin filter
    origin_options = df["Origin"].unique()
    origin_filter = st.sidebar.multiselect(
        "Filter by Origin",
        options=origin_options,
        default=origin_options
    )
    
    # Make filter
    make_options = df["Make"].unique()
    make_filter = st.sidebar.multiselect(
        "Filter by Make",
        options=make_options,
        default=make_options[:5] if len(make_options) > 5 else make_options
    )
    
    # Year filter
    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max)
    )
    
    # Apply filters
    filtered_df = df[
        (df["Origin"].isin(origin_filter)) &
        (df["Make"].isin(make_filter)) &
        (df["Year"].between(year_range[0], year_range[1]))
    ].copy()
    
    if filtered_df.empty:
        st.warning("No data matches your filters")
        return
    
    # Performance metrics - using exact column names from your data
    st.sidebar.header("Performance Metrics")
    metrics = {
        "Engine HP": "Engine HP",
        "City MPG": "city mpg",
        "Highway MPG": "highway MPG",  # Note the exact capitalization
        "Engine Cylinders": "Engine Cylinders",
        "Popularity": "Popularity",
        "MSRP": "MSRP"
    }
    selected_metric = st.sidebar.selectbox("Primary Metric", list(metrics.keys()))
    
    # Visualizations
    st.subheader("Performance Analysis")
    
    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.box(
            filtered_df,
            x="Origin", y=metrics[selected_metric],
            title=f"{selected_metric} by Origin",
            color="Origin"
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.box(
            filtered_df,
            x="Vehicle Style", y=metrics[selected_metric],
            title=f"{selected_metric} by Vehicle Style",
            color="Vehicle Style"
        )
        fig2.update_xaxes(tickangle=45)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2
    col3, col4 = st.columns(2)
    with col3:
        year_avg = filtered_df.groupby("Year", as_index=False)[metrics[selected_metric]].mean()
        fig3 = px.line(
            year_avg,
            x="Year", y=metrics[selected_metric],
            title=f"{selected_metric} Trend Over Years",
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        top_makes = filtered_df["Make"].value_counts().nlargest(10).index
        fig4 = px.box(
            filtered_df[filtered_df["Make"].isin(top_makes)],
            x="Make", y=metrics[selected_metric],
            title=f"Top 10 Makes by {selected_metric}",
            color="Make"
        )
        fig4.update_xaxes(tickangle=45)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Row 3 - Using exact column names
    col5, col6 = st.columns(2)
    with col5:
        fig5 = px.scatter(
            filtered_df,
            x="Engine HP", y="city mpg",
            color="Origin",
            title="HP vs City MPG"
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col6:
        fig6 = px.scatter(
            filtered_df,
            x="Engine HP", y="highway MPG",  # Using exact column name
            color="Vehicle Size",
            title="HP vs Highway MPG"
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # Data table
    st.subheader("Filtered Data")
    st.dataframe(filtered_df.head(100))

if __name__ == "__main__":
    app()