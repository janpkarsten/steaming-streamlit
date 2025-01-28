import json
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

from ..data_io import get_data

df_temp = get_data("temp")
df_temp["Year"] = pd.to_datetime(df_temp["Year"], format="%Y")
df_temp["direction"] = df_temp["Anomaly"].apply(lambda x: "greater" if x > 0 else "lesser")

def create_figure():

    # Layout
    source_annotation = go.layout.Annotation(
            showarrow=False,
            text='Data source: NOAA Global Surface Temperature Dataset (NOAAGlobalTemp), Version 6.0.0',
            xref="paper",
            yref="paper",
            xanchor='left',
            x=0,
            yanchor='top',
            y=-0.1
        )
    layout = go.Layout(
        # paper_bgcolor="lightgrey",
        title={
            "text": f"Temperature anomalies<br><sup style='font-weight: normal'>Difference in temperature between the median of 1901 - 2000</sup>",
            "font_size": 20,
            "font_weight": "bold"
        },
        # xaxis={

        # }
        # legend={
        #     "title": "Energy sources",
        #     "font_size": 14,
        #     "font_weight": "bold",
        #     "itemsizing": "constant"
        # },
        height=700,
        annotations=[source_annotation],
        showlegend=False,
        modebar={
            "orientation": "h",
            "remove": "toimage"
        },
        dragmode="pan"
    )

    # Hover template
    hovertemplate = """
    <b>%{x:%Y}</b><br>
    Temperature: %{y}
    <extra></extra>
    """

    # fig = go.Figure()
    fig = px.bar(df_temp, 
                 x="Year",
                 y="Anomaly",
                 color="direction",
                 color_discrete_map={
                     "lesser": "#377eb8",
                     "greater": "#e41a1c",
                 },
                    # custom_data=["country", "fossil_change", "wind_share_energy_now", "solar_share_energy_now"],
                    # color_continuous_scale=px.colors.diverging.Temps,color_continuous_midpoint=0,
                    # opacity=.6
                    )

    fig.update_traces(hovertemplate=hovertemplate)
    fig.update_layout(layout)

    return fig