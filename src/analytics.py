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


def calculate_country_growth(
    df,
    start_year,
    end_year,
):
    """
    Calcula o crescimento percentual do TIV
    entre o primeiro e o último ano do período.
    """

    if df.empty:
        return pd.DataFrame()

    yearly = (
        df
        .groupby(
            ["country", "year"],
            as_index=False,
        )["tiv"]
        .sum()
    )

    start = (
        yearly[
            yearly["year"] == start_year
        ]
        [
            [
                "country",
                "tiv",
            ]
        ]
        .rename(
            columns={
                "tiv": "start_tiv",
            }
        )
    )

    end = (
        yearly[
            yearly["year"] == end_year
        ]
        [
            [
                "country",
                "tiv",
            ]
        ]
        .rename(
            columns={
                "tiv": "end_tiv",
            }
        )
    )

    result = pd.merge(
        start,
        end,
        on="country",
        how="inner",
    )

    # Evita divisão por zero
    result = result[
        result["start_tiv"] > 0
    ].copy()

    result["growth"] = (
        (
            result["end_tiv"]
            /
            result["start_tiv"]
        )
        - 1
    ) * 100

    return (
        result
        .sort_values(
            "growth",
            ascending=False,
        )
        .reset_index(drop=True)
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


def create_country_yearly(
    country_exports,
    country_imports,
):

    exports = (
        country_exports[
            [
                "year",
                "tiv",
            ]
        ]
        .rename(
            columns={
                "tiv": "Exportações",
            }
        )
    )

    imports = (
        country_imports[
            [
                "year",
                "tiv",
            ]
        ]
        .rename(
            columns={
                "tiv": "Importações",
            }
        )
    )

    return (
        pd.merge(
            exports,
            imports,
            on="year",
            how="outer",
        )
        .sort_values("year")
        .fillna(0)
    )


def calculate_country_metrics(
    country_exports,
    country_imports,
):

    export_total = float(
        country_exports["tiv"].sum()
    )

    import_total = float(
        country_imports["tiv"].sum()
    )

    export_average = (
        float(country_exports["tiv"].mean())
        if not country_exports.empty
        else 0.0
    )

    import_average = (
        float(country_imports["tiv"].mean())
        if not country_imports.empty
        else 0.0
    )

    return {
        "export_total": export_total,
        "import_total": import_total,
        "export_average": export_average,
        "import_average": import_average,
    }


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