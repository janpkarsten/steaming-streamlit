import streamlit as st

from src.vis import map_plot, temp_plot


st.set_page_config(page_title="main")



st.title("Steaming Streamlit")
st.header("Streamlit investigation on renewable energy")
st.text("Burning fossil fuels allowed the rise of technology, wealth and health but also temperature. Can technology help us?")


# Temperature plot

fig_temp = temp_plot.create_figure()
st.plotly_chart(fig_temp)
