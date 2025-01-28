import json
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

from ..data_io import get_data

# @st.cache_data
# def load_data(path):
#     df = pd.read_csv(path)
#     return df

# GeoJson
geojson_world = get_data("geojson", fname="countries.geojson")

# Share data
year_past = 1990
year_now = 2022
df_shares = get_data("shares", year_past=year_past, year_now=year_now)

def create_figure():
    source_annotation = go.layout.Annotation(
            showarrow=False,
            text='Data source: Energy Institute - Statistical Review of World Energy (2024)',
            xanchor='left',
            x=0,
            yanchor='top',
            y=0
        )
    layout = go.Layout(
        # paper_bgcolor="lightgrey",
        title={
            "text": f"Renewables on the rise<br><sup>The change in fossil fuel share between {year_past} and {year_now}</sup>",
            "font_size": 20,
            "font_weight": "bold"
        },
        legend={
            "title": "Energy sources",
            "font_size": 14,
            "font_weight": "bold",
            "itemsizing": "constant"
        },
        coloraxis_colorbar={
        "title_text": f"Change in fossil energy share between {year_past} and {year_now}",
        "title_side":"top",
        "orientation": "h",
        "y": 1,
        # "xanchor": "center"
        },
        mapbox_style='open-street-map',
        # mapbox_center={"lat": df_eu_clean.lat[0], "lon": df_eu_clean.lon[0]},
        mapbox_zoom=1,
        height=700,
        annotations=[source_annotation],
        modebar={
            "orientation": "h",
            "remove": "toimage"
        },
        dragmode="pan",
    )

    # Hover template
    hovertemplate = """
    <b>%{customdata[0]}</b><br>
    Change: %{customdata[1]:.2f}<br>
    Wind: %{customdata[2]:.2f}%<br>
    Solar: %{customdata[3]:.2f}%
    """

    fig_map = go.Figure()
    fig_map = px.choropleth_mapbox(df_shares.reset_index(), geojson=geojson_world, 
                            locations=df_shares["iso_code"], 
                            featureidkey="properties.ISO_A3", 
                            color=df_shares["fossil_change"],
                            custom_data=["country", "fossil_change", "wind_share_energy_now", "solar_share_energy_now"],
                            color_continuous_scale=px.colors.diverging.Temps,
                            color_continuous_midpoint=0,
                            opacity=.6)

    fig_map.update_traces(hovertemplate=hovertemplate)
    fig_map.update_layout(layout)

    return fig_map