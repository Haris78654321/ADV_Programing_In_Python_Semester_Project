import streamlit as st
import pandas as pd
from clean import load_and_clean_data

def app():
    st.title("Car Dataset Filter")

    df = load_and_clean_data()

    st.sidebar.header("Filters")

    # Columns to treat as dropdown filters (categorical + discrete numeric)
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

    # Numeric columns for sliders: all numeric except doors & cylinders
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    slider_cols = [col for col in numeric_cols if col not in ["Number of Doors", "Engine Cylinders"]]

    cont_filters = {}
    for col in slider_cols:
        min_val = int(df[col].min())
        max_val = int(df[col].max())
        selected_range = st.sidebar.slider(f"{col}", min_val, max_val, (min_val, max_val))
        cont_filters[col] = selected_range

    # Apply dropdown filters
    filtered_df = df.copy()
    for col, val in dropdown_filters.items():
        if val != "All":
            filtered_df = filtered_df[filtered_df[col].astype(str) == val]

    # Apply slider filters
    for col, (min_val, max_val) in cont_filters.items():
        filtered_df = filtered_df[(filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)]

    # Convert categorical columns to string to avoid pyarrow errors
    for col in filtered_df.select_dtypes(include=["category"]).columns:
        filtered_df[col] = filtered_df[col].astype(str)
        filtered_df[col] = filtered_df[col].astype(object)

    st.write(f"Resulting cars: {filtered_df.shape[0]}")
    st.dataframe(filtered_df)

    # Download filtered data as Excel (using openpyxl engine)
    def to_excel(df):
        import io
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Filtered Cars')
        processed_data = output.getvalue()
        return processed_data

    if not filtered_df.empty:
        excel_data = to_excel(filtered_df)
        st.download_button(
            label="Download filtered data as Excel",
            data=excel_data,
            file_name="filtered_cars.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
