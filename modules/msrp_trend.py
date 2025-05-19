import streamlit as st
import pandas as pd
import plotly.express as px
from data.clean_data import load_and_clean_data


def msrp_dashboard(df):
    st.title("🚘 MSRP Dashboard")
    st.markdown("Explore MSRP trends and pricing structures by make and model.")

    # Clean and validate data
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["MSRP"] = pd.to_numeric(df["MSRP"], errors="coerce")
    df = df.dropna(subset=["Year", "MSRP", "Make", "Model", "Vehicle Style", "Origin"])
    df["Year"] = df["Year"].astype(int)

    # Sidebar filters (affect only line chart)
    st.sidebar.header("📊 Filters")
    origin_options = sorted(df["Origin"].unique())
    selected_origin = st.sidebar.multiselect("Select Origin (Country)", origin_options)
    filtered_origin = df[df["Origin"].isin(selected_origin)] if selected_origin else df

    make_options = sorted(filtered_origin["Make"].unique())
    selected_make = st.sidebar.multiselect("Select Make (Company)", make_options)
    filtered_make = filtered_origin[filtered_origin["Make"].isin(selected_make)] if selected_make else filtered_origin

    style_options = sorted(filtered_make["Vehicle Style"].unique())
    selected_style = st.sidebar.multiselect("Select Vehicle Style", style_options)
    filtered_for_line = filtered_make[filtered_make["Vehicle Style"].isin(selected_style)] if selected_style else filtered_make

    # --- Line Chart: Average MSRP over Years ---
    st.subheader("📈 Average MSRP Over the Years")
    if not filtered_for_line.empty:
        msrp_trend = filtered_for_line.groupby("Year", as_index=False)["MSRP"].mean()

        fig_line = px.line(
            msrp_trend,
            x="Year", y="MSRP",
            title="Average MSRP Over the Years",
            markers=True
        )
        fig_line.update_layout(yaxis_tickprefix="$", yaxis_title="Average MSRP ($)")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

    # --- Treemap: Origin → Make → Model by Average MSRP (unfiltered) ---
    st.subheader("📊 Treemap: Origin → Make → Model by Average MSRP")
    if not df.empty:
        treemap_data = df.groupby(["Origin", "Make", "Model"], as_index=False)["MSRP"].mean()

        # Add custom label for leaf nodes (Model + MSRP)
        treemap_data["Label"] = treemap_data["Model"] + "<br>$" + treemap_data["MSRP"].round(0).astype(int).astype(str)

        fig_treemap = px.treemap(
            treemap_data,
            path=["Origin", "Make", "Label"],
            values="MSRP",
            color="Origin",
            title="Treemap of Average MSRP by Origin, Make and Model",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig_treemap.update_traces(
            texttemplate="%{label}",
            textposition="middle center",
            textfont_size=16,
            hovertemplate='<b>%{label}</b><br>MSRP: $%{value:,.0f}<extra></extra>'
        )

        fig_treemap.update_layout(
            margin=dict(t=40, l=10, r=10, b=10),
            uniformtext=dict(minsize=12, mode='hide'),
            font=dict(size=16, family="Arial Black")
        )

        st.plotly_chart(fig_treemap, use_container_width=True)
    else:
        st.info("Treemap not available for current data.")


def app():
    df = load_and_clean_data()
    msrp_dashboard(df)
