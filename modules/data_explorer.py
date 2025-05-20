import streamlit as st
import pandas as pd
import plotly.express as px
from data.clean_data import load_and_clean_data

def app():
    st.title("🌍 Car Dataset Explorer")

    # Load and clean data
    df = load_and_clean_data()

    # Sidebar filters with interdependencies (multi-select with "All" option)
    st.sidebar.header("Filters")

    dropdown_order = [
        "Origin", "Make", "Model", "Engine Fuel Type", "Transmission Type",
        "Driven_Wheels", "Market Category", "Vehicle Size", "Vehicle Style",
        "Number of Doors", "Engine Cylinders"
    ]

    dropdown_filters = {}
    temp_df = df.copy()

    for col in dropdown_order:
        options = sorted(temp_df[col].dropna().astype(str).unique())
        options = ["All"] + options  # Add 'All' option at the top

        selected = st.sidebar.multiselect(
            f"{col}",
            options=options,
            default=["All"],  # default no filter
            key=col
        )

        if "All" in selected or len(selected) == 0:
            # No filtering on this column
            dropdown_filters[col] = options[1:]  # all real options
        else:
            # Filter by selected excluding "All"
            dropdown_filters[col] = [x for x in selected if x != "All"]

        # Narrow down next dropdown options if filtering applied
        if len(dropdown_filters[col]) < len(options) - 1:
            temp_df = temp_df[temp_df[col].astype(str).isin(dropdown_filters[col])]

    # Continuous numeric filters (sliders)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    slider_cols = [col for col in numeric_cols if col not in ["Number of Doors", "Engine Cylinders"]]

    cont_filters = {}
    for col in slider_cols:
        min_val = float(df[col].min())
        max_val = float(df[col].max())
        step = (max_val - min_val) / 100 if max_val > min_val else 1
        selected_range = st.sidebar.slider(
            f"{col}", min_val, max_val, (min_val, max_val), step=step, key=col+"_slider"
        )
        cont_filters[col] = selected_range

    # Apply all filters to dataframe
    filtered_df = df.copy()

    # Apply multi-select dropdown filters
    for col, selected_vals in dropdown_filters.items():
        if len(selected_vals) < len(df[col].dropna().unique()):
            filtered_df = filtered_df[filtered_df[col].astype(str).isin(selected_vals)]

    # Apply numeric range filters
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

        makes_available = filtered_df["Make"].dropna().unique()
        if len(makes_available) > 0:
            selected_make = st.selectbox("Select Make", sorted(makes_available))
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
