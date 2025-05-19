import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from data.clean_data import load_and_clean_data

def app():
    st.title("🌍 Car Dataset Explorer")

    # Load data
    df = load_and_clean_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Dropdown filters
    dropdown_cols = [
        "Origin", "Make", "Model", "Engine Fuel Type", "Transmission Type",
        "Driven_Wheels", "Market Category", "Vehicle Size", "Vehicle Style",
        "Number of Doors", "Engine Cylinders"
    ]
    
    dropdown_filters = {}
    for col in dropdown_cols:
        options = ["All"] + sorted(df[col].dropna().astype(str).unique().tolist())
        selected = st.sidebar.selectbox(f"{col}", options)
        dropdown_filters[col] = selected

    # Numeric filters
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    slider_cols = [col for col in numeric_cols if col not in ["Number of Doors", "Engine Cylinders"]]
    
    cont_filters = {}
    for col in slider_cols:
        min_val = int(df[col].min())
        max_val = int(df[col].max())
        selected_range = st.sidebar.slider(f"{col}", min_val, max_val, (min_val, max_val))
        cont_filters[col] = selected_range

    # Apply filters
    filtered_df = df.copy()
    for col, val in dropdown_filters.items():
        if val != "All":
            filtered_df = filtered_df[filtered_df[col].astype(str) == val]

    for col, (min_val, max_val) in cont_filters.items():
        filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]

    # Convert categorical columns
    for col in filtered_df.select_dtypes(include=["category"]).columns:
        filtered_df[col] = filtered_df[col].astype(str)
        filtered_df[col] = filtered_df[col].astype(object)

    # Show map first
    st.subheader("Car Origin Heat Distribution")
    
    COUNTRY_COORDINATES = {
        "USA": {"lat": 37.0902, "lon": -95.7129},
        "Germany": {"lat": 51.1657, "lon": 10.4515},
        "Japan": {"lat": 36.2048, "lon": 138.2529},
        "UK": {"lat": 55.3781, "lon": -3.4360},
        "Italy": {"lat": 41.8719, "lon": 12.5674},
        "Sweden": {"lat": 60.1282, "lon": 18.6435},
        "South Korea": {"lat": 35.9078, "lon": 127.7669},
        "Netherlands": {"lat": 52.1326, "lon": 5.2913},
        "France": {"lat": 46.6035, "lon": 1.8883},
        "United States": {"lat": 37.0902, "lon": -95.7129},
        "United Kingdom": {"lat": 55.3781, "lon": -3.4360},
    }

    if not filtered_df.empty:
        # Process origin data
        origin_counts = filtered_df["Origin"].value_counts().reset_index()
        origin_counts.columns = ["Origin", "Count"]
        
        # Add coordinates with case-insensitive matching
        origin_counts["coords"] = origin_counts["Origin"].apply(
            lambda x: next(
                (v for k, v in COUNTRY_COORDINATES.items() 
                 if str(x).lower() in [k.lower(), v.get("name", "").lower()]), 
                None
            )
        )
        
        origin_counts = origin_counts.dropna(subset=["coords"])
        origin_counts["lat"] = origin_counts["coords"].apply(lambda x: x["lat"])
        origin_counts["lon"] = origin_counts["coords"].apply(lambda x: x["lon"])
        
        if not origin_counts.empty:
            # Create heatmap with reference points
            heatmap = pdk.Layer(
                "HeatmapLayer",
                data=origin_counts,
                get_position=["lon", "lat"],
                get_weight="Count",
                aggregation=pdk.types.String("MEAN"),
                radius=120000,
                intensity=1.5,
                threshold=0.03,
                pickable=True
            )

            points = pdk.Layer(
                "ScatterplotLayer",
                data=origin_counts,
                get_position=["lon", "lat"],
                get_radius=60000,
                get_fill_color=[255, 165, 0, 200],  # Orange color
                pickable=True,
                stroked=True,
                line_width_scale=5
            )

            # Render the map
            st.pydeck_chart(pdk.Deck(
                layers=[heatmap, points],
                initial_view_state=pdk.ViewState(
                    latitude=origin_counts["lat"].mean(),
                    longitude=origin_counts["lon"].mean(),
                    zoom=1.5,
                    pitch=0
                ),
                map_style="mapbox://styles/mapbox/light-v10",
                tooltip={
                    "html": "<b>{Origin}</b><br>{Count} cars",
                    "style": {
                        "backgroundColor": "#333333",
                        "color": "white",
                        "fontSize": "14px"
                    }
                }
            ))

            # Country Distribution Charts
            st.subheader("Country Distribution Analysis")
            col1, col2 = st.columns(2)
            
            with col1:
                # Histogram showing total cars per country
                fig_bar = px.bar(
                    origin_counts.sort_values("Count", ascending=False),
                    x="Origin",
                    y="Count",
                    title="Total Cars by Country",
                    color="Origin",
                    labels={"Origin": "Country", "Count": "Number of Cars"},
                    height=400
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Pie chart showing market share
                fig_pie = px.pie(
                    origin_counts,
                    values="Count",
                    names="Origin",
                    title="Market Share by Country",
                    height=400,
                    hole=0.3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

            # NEW: Model Distribution by Manufacturer Section
            st.subheader("Model Distribution by Manufacturer")
            
            # Get unique makes from filtered data
            available_makes = sorted(filtered_df["Make"].unique().tolist())
            selected_make = st.selectbox("Select Manufacturer", available_makes)
            
            if selected_make:
                make_df = filtered_df[filtered_df["Make"] == selected_make]
                model_counts = make_df["Model"].value_counts().reset_index()
                model_counts.columns = ["Model", "Count"]
                
                col3, col4 = st.columns(2)
                
                with col3:
                    # Histogram showing models for selected make
                    fig_model_bar = px.bar(
                        model_counts.sort_values("Count", ascending=False),
                        x="Model",
                        y="Count",
                        title=f"Models by {selected_make}",
                        color="Model",
                        labels={"Model": "Model Name", "Count": "Number of Cars"},
                        height=400
                    )
                    st.plotly_chart(fig_model_bar, use_container_width=True)
                
                with col4:
                    # Pie chart showing model distribution
                    fig_model_pie = px.pie(
                        model_counts,
                        values="Count",
                        names="Model",
                        title=f"Model Share for {selected_make}",
                        height=400,
                        hole=0.3
                    )
                    fig_model_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_model_pie, use_container_width=True)

        else:
            st.warning("No valid country coordinates found for the filtered data")
    else:
        st.warning("No cars match the selected filters")

    # Show data table
    st.subheader("Filtered Car Data")
    st.write(f"Showing {filtered_df.shape[0]} cars")
    st.dataframe(filtered_df)

    # Download button
    if not filtered_df.empty:
        def to_excel(df):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Filtered Cars')
            return output.getvalue()

        excel_data = to_excel(filtered_df)
        st.download_button(
            label="Download Filtered Data (Excel)",
            data=excel_data,
            file_name="filtered_cars.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    app()