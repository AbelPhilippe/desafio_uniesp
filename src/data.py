import pandas as pd
import streamlit as st

from src.config import (
    WORLD_EXPORT_NAMES,
    WORLD_IMPORT_NAMES,
)

def normalize_country_name(value):
    return (
        str(value)
        .strip()
        .lower()
        .replace("-", " ")
    )


@st.cache_data
def load_all_countries(directory):

    dataframes = []

    files = sorted(directory.glob("*.csv"))

    for file in files:

        try:

            df = pd.read_csv(file)

            required_columns = {
                "country",
                "year",
                "tiv",
            }

            if not required_columns.issubset(df.columns):
                continue

            df["country"] = (
                df["country"]
                .astype(str)
                .str.strip()
            )

            df["year"] = pd.to_numeric(
                df["year"],
                errors="coerce",
            )

            df["tiv"] = pd.to_numeric(
                df["tiv"],
                errors="coerce",
            )

            df = df.dropna(
                subset=[
                    "year",
                    "tiv",
                ]
            )

            dataframes.append(df)

        except Exception:
            continue

    if not dataframes:

        return pd.DataFrame(
            columns=[
                "country",
                "year",
                "tiv",
            ]
        )

    return pd.concat(
        dataframes,
        ignore_index=True,
    )


def prepare_datasets(exports_df, imports_df):

    exports_df = exports_df.copy()
    imports_df = imports_df.copy()

    exports_df["_country_normalized"] = (
        exports_df["country"]
        .apply(normalize_country_name)
    )

    imports_df["_country_normalized"] = (
        imports_df["country"]
        .apply(normalize_country_name)
    )

    world_export_df = exports_df[
        exports_df["_country_normalized"].isin(
            WORLD_EXPORT_NAMES
        )
    ].copy()

    world_import_df = imports_df[
        imports_df["_country_normalized"].isin(
            WORLD_IMPORT_NAMES
        )
    ].copy()

    exports_countries_df = exports_df[
        ~exports_df["_country_normalized"].isin(
            WORLD_EXPORT_NAMES
        )
    ].copy()

    imports_countries_df = imports_df[
        ~imports_df["_country_normalized"].isin(
            WORLD_IMPORT_NAMES
        )
    ].copy()

    return (
        exports_countries_df,
        imports_countries_df,
        world_export_df,
        world_import_df,
    )


def filter_period(df, start_year, end_year):

    return df[
        (df["year"] >= start_year)
        &
        (df["year"] <= end_year)
    ].copy()

def get_country_data(
    exports_df,
    imports_df,
    country,
    start_year,
    end_year,
):

    country_exports = exports_df[
        exports_df["country"] == country
    ].copy()

    country_imports = imports_df[
        imports_df["country"] == country
    ].copy()

    country_exports = filter_period(
        country_exports,
        start_year,
        end_year,
    )

    country_imports = filter_period(
        country_imports,
        start_year,
        end_year,
    )

    return country_exports, country_imports