import pandas as pd


def create_ranking(df):

    return (
        df
        .groupby(
            "country",
            as_index=False,
        )["tiv"]
        .sum()
        .sort_values(
            "tiv",
            ascending=False,
        )
    )


def calculate_world_total(df):

    return float(
        df["tiv"].sum()
    )


def calculate_world_yearly(df):

    return (
        df
        .groupby(
            "year",
            as_index=False,
        )["tiv"]
        .sum()
        .sort_values("year")
    )


def create_comparison(
    export_ranking,
    import_ranking,
    map_type,
):

    comparison = pd.merge(
        export_ranking.rename(
            columns={
                "tiv": "exports",
            }
        ),
        import_ranking.rename(
            columns={
                "tiv": "imports",
            }
        ),
        on="country",
        how="outer",
    )

    comparison[
        [
            "exports",
            "imports",
        ]
    ] = (
        comparison[
            [
                "exports",
                "imports",
            ]
        ]
        .fillna(0)
    )

    comparison["net"] = (
        comparison["exports"]
        -
        comparison["imports"]
    )

    sort_column = (
        "exports"
        if map_type == "Exportações"
        else "imports"
    )

    return comparison.sort_values(
        sort_column,
        ascending=False,
    )


def create_map_data(
    df,
    country_iso3,
):

    map_df = (
        df
        .groupby(
            "country",
            as_index=False,
        )["tiv"]
        .sum()
        .rename(
            columns={
                "tiv": "TIV",
            }
        )
    )

    map_df["country_normalized"] = (
        map_df["country"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(
            "-",
            " ",
            regex=False,
        )
    )

    map_df["iso_alpha"] = (
        map_df["country_normalized"]
        .map(country_iso3)
    )

    return map_df.dropna(
        subset=["iso_alpha"]
    )


def count_unique_countries(df):

    return (
        df["country"]
        .nunique()
    )