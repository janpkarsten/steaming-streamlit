import json
from pathlib import Path

import streamlit as st
import pandas as pd

# TODO: Convert to Factory pattern

DATA_PATH = Path("data", "raw")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

def get_data(data_name: str, **kwargs) -> pd.DataFrame | dict:

    if data_name == "shares":
        year_past = kwargs.get("year_past", None)
        year_now = kwargs.get("year_now", None)
        return _get_shares(year_past=year_past, year_now=year_now)
    elif data_name == "geojson":
        fname = kwargs.get("fname", None)
        return _get_geojson(fname)
    elif (data_name == "temperature") | (data_name == "temp"):
        return _get_temp()
    elif data_name == "energy":
        return _get_fossil_change()
    elif data_name == "codebook":
        return _get_codebook()

def _get_energy() -> pd.DataFrame:

    fpath = Path(DATA_PATH, "energy","owid-energy-data.csv")
    df_raw = load_data(path=fpath)
    df_energy = df_raw.copy(deep=True)
    return df_energy

def _get_shares(year_past: int, year_now: int) -> pd.DataFrame:

    assert year_past, "Past year not passed"
    assert year_now, "Recent year not passed"

    df_energy = _get_energy()

    # ~~~~~~~~~~~~~~~~~~~~~~~ Clean & Prepare Data ~~~~~~~~~~~~~~~~~~~~~~~
    # Drop missing iso code countries
    df_world_clean = df_energy.dropna(subset=["iso_code"])

    # Get shares between two timepoints
    share_past = df_world_clean.loc[df_world_clean["year"] == year_past, :].set_index("country")
    share_now = df_world_clean.loc[df_world_clean["year"] == year_now, :].set_index("country")
    df_shares = pd.merge(share_past, share_now, on=["country", "iso_code"], suffixes=["_past", "_now"])
    
    df_shares = df_shares.assign(fossil_change=df_shares["fossil_share_energy_now"] - df_shares["fossil_share_energy_past"])
    return df_shares

def _get_geojson(fname: str) -> pd.DataFrame:

    # GeoJson
    with open(Path(DATA_PATH, "geojson", fname)) as f:
        geojson_world = json.load(f)
    return geojson_world

def _get_temp() -> pd.DataFrame:
    fpath = Path(DATA_PATH, "temperature", "global_temp.csv")
    # df_temp = load_data(fpath)
    return pd.read_csv(fpath, skiprows=4)

def _get_fossil_change() -> pd.DataFrame:

    df_energy = _get_energy()
    df_energy = df_energy.set_index("country")

    return df_energy

def _get_codebook():

    fpath = Path(DATA_PATH, "misc", "owid-energy-codebook.csv")
    df = pd.read_csv(fpath)
    df = df.set_index("column")
    return df
