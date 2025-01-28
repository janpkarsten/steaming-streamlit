import streamlit as st

from src.vis import map_plot, fossil_plot
from src.data_io import get_data

st.set_page_config(page_title="Renewable Energy")
df_energy = get_data("energy")

tab1, tab2= st.tabs(["Map", "Chart"])

row1 = st.columns(2)
row2 = st.columns(1)

col1, col2 = st.columns(2, gap="medium")

with tab1:
    st.header("Decrease of fossil fuel usage across the world")
    fig_map = map_plot.create_figure()

    st.plotly_chart(fig_map, use_container_width=True)

with tab2:      
        st.header("Decrease of fossil fuel usage")
        # with col2:
        # tile = row1[0].container(height=120)
        country = row1[0].multiselect(
            "Select country",
            df_energy.index.unique(),
            default=["Europe", "World"],
            label_visibility="hidden" 
        )
        param = row1[1].selectbox(
            "Select parameter",
            df_energy.columns[3:],
            index=36
        )
        tile = row2[0]
        fig_line = fossil_plot.create_figure(param = param, country=country)
        tile.plotly_chart(fig_line, use_container_width=True)
