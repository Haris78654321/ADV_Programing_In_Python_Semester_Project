import streamlit as st
import pandas as pd
import plotly.express as px
from data.clean_data import load_and_clean_data

def app():
    st.title("🌍 Car Dataset Explorer")

    # Load and clean data
    df = load_and_clean_data()

    # Sidebar filters with interdependencies
    st.sidebar.header("Filters")

    # Define dropdown filter order
    dropdown_order = [
        "Origin", "Make", "Model", "Engine Fuel Type", "Transmission Type",
        "Driven_Wheels", "Market Category", "Vehicle Size", "Vehicle Style",
        "Number of Doors", "Engine Cylinders"
    ]

    dropdown_filters = {}
    temp_df = df.copy()

    # Dynamically generate dropdowns based on prior selections
    for col in dropdown_order:
        options = ["All"] + sorted(temp_df[col].dropna().astype(str).unique())
        selected = st.sidebar.selectbox(f"{col}", options, key=col)
        dropdown_filters[col] = selected

        # Narrow down for next dropdown
        if selected != "All":
            temp_df = temp_df[temp_df[col].astype(str) == selected]

    # Continuous numeric filters
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    slider_cols = [col for col in numeric_cols if col not in ["Number of Doors", "Engine Cylinders"]]

    cont_filters = {}
    for col in slider_cols:
        min_val = int(df[col].min())
        max_val = int(df[col].max())
        selected_range = st.sidebar.slider(f"{col}", min_val, max_val, (min_val, max_val))
        cont_filters[col] = selected_range

    # Apply all filters
    filtered_df = df.copy()
    for col, val in dropdown_filters.items():
        if val != "All":
            filtered_df = filtered_df[filtered_df[col].astype(str) == val]

    for col, (min_val, max_val) in cont_filters.items():
        filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]

    # Visualizations
    if not filtered_df.empty:
        st.subheader("🌐 Car Origin Distribution Map")
        origin_counts = filtered_df["Origin"].value_counts().reset_index()
        origin_counts.columns = ["Country", "Count"]

        fig_choropleth = px.choropleth(
            origin_counts,
            locations="Country",
            locationmode="country names",
            color="Count",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.OrRd,
        )

        fig_choropleth.update_geos(
            showcoastlines=True, coastlinecolor="Gray", coastlinewidth=0.5,
            showcountries=True, countrycolor="Black", countrywidth=0.5,
            showland=True, landcolor="rgb(217, 217, 217)",
            showocean=True, oceancolor="rgb(200, 230, 250)",
            showlakes=True, lakecolor="rgb(180, 220, 250)",
            showrivers=True, rivercolor="rgb(160, 200, 255)",
            projection_type="natural earth", showframe=False
        )
        fig_choropleth.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig_choropleth, use_container_width=True)

        st.subheader("🧮 Country-Level Car Distribution")
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(origin_counts, x="Country", y="Count", color="Country", title="Cars by Country")
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            fig_pie = px.pie(origin_counts, names="Country", values="Count", hole=0.3, title="Country Share")
            st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("🚘 Models by Selected Make")

        if not filtered_df["Make"].empty:
            selected_make = st.selectbox("Select Make", sorted(filtered_df["Make"].unique()))
            make_df = filtered_df[filtered_df["Make"] == selected_make]
            model_counts = make_df["Model"].value_counts().reset_index()
            model_counts.columns = ["Model", "Count"]

            col3, col4 = st.columns(2)
            with col3:
                fig_model_bar = px.bar(model_counts, x="Model", y="Count", color="Model", title="Models Distribution")
                st.plotly_chart(fig_model_bar, use_container_width=True)
            with col4:
                fig_model_pie = px.pie(model_counts, names="Model", values="Count", hole=0.3, title="Model Share")
                st.plotly_chart(fig_model_pie, use_container_width=True)
        else:
            st.info("No makes available with the current filter selection.")
    else:
        st.warning("No cars match the selected filters.")

    st.subheader("📄 Filtered Car Data")
    st.write(f"Showing {filtered_df.shape[0]} cars")
    st.dataframe(filtered_df)

    # Excel export
    if not filtered_df.empty:
        def to_excel(df):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Filtered Cars')
            return output.getvalue()

        excel_data = to_excel(filtered_df)
        st.download_button(
            "Download Filtered Data (Excel)",
            data=excel_data,
            file_name="filtered_cars.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
