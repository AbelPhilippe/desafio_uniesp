import plotly.express as px
import numpy as np

from src.config import (
    COUNTRY_PALETTE,
    EXPORT_COLOR,
    IMPORT_COLOR,
    MAP_EXPORT_SCALE,
    MAP_IMPORT_SCALE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)

def create_world_map(
    map_df,
    map_type,
    start_year,
    end_year,
):
    max_tiv = map_df["TIV"].max()

    tickvals = np.linspace(
        0,
        max_tiv,
        6
    )

    ticktext = [
        f"{v/1_000_000:.1f}M"
        for v in tickvals
    ]

    color_scale = (
        MAP_EXPORT_SCALE
        if map_type == "Exportações"
        else MAP_IMPORT_SCALE
    )

    fig = px.choropleth(
        map_df,
        locations="iso_alpha",
        color="TIV",
        hover_name="country",
        hover_data={
            "iso_alpha": False,
            "TIV": ":,.0f",
        },
        color_continuous_scale=color_scale,
        projection="natural earth",
        labels={
            "TIV": "Milhões de SIPRI TIV",
        },
        title=(
            f"{map_type} — "
            f"{start_year}–{end_year}"
        ),
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(100,100,100,0.5)",
        showland=True,
        landcolor="rgba(220,220,220,0.25)",
        showcountries=True,
        countrycolor="rgba(100,100,100,0.35)",
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_coloraxes(
    colorbar_title=None,
    colorbar=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=-0.15,
        len=1.0,
        thickness=12,
        tickvals=tickvals,
        ticktext=ticktext,
        tickfont=dict(size=10),
        )
    )

    fig.add_annotation(
    text="TIV",
    x=0.03,
    y=0.009,
    xanchor="left",
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(
        size=11,
        color=TEXT_PRIMARY,
        )
    )

    fig.update_layout(
        height=500,
        margin=dict(
            l=0,
            r=0,
            t=60,
            b=20,
        ),
        title=dict(
            font=dict(size=18),
        ),
    )

    return fig


def create_world_yearly_chart(
    yearly_df,
    title,
    color,
):

    fig = px.bar(
        yearly_df,
        x="year",
        y="tiv",
        labels={
            "year": "Ano",
            "tiv": "Milhões de SIPRI TIV",
        },
        title=title,
    )

    fig.update_traces(
        marker_color=color,
        hovertemplate=(
            "<b>Ano:</b> %{x}<br>"
            "<b>TIV:</b> %{y:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
        title=dict(
            font=dict(size=22),
        ),
        xaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=15),
        ),
        yaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=15),
        ),
    )

    return fig


def create_participation_chart(
    ranking,
    top_n,
    title,
):

    data = (
        ranking
        .head(top_n)
        .copy()
    )

    fig = px.pie(
        data,
        names="country",
        values="tiv",
        hole=0.35,
        color_discrete_sequence=COUNTRY_PALETTE,
        title=title,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(
            size=20,
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "TIV: %{value:,.0f}<br>"
            "Participação: %{percent}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        title=dict(
            font=dict(size=22),
        ),
        legend_title_text="Países",
        legend=dict(
            font=dict(
                size=16,
            ),
            title=dict(
                font=dict(
                    size=17,
                ),
            ),
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    return fig


def create_comparison_chart(
    comparison,
    top_n,
):

    data = (
        comparison
        .sort_values(
            "exports",
            ascending=False,
        )
        .head(top_n)
    )

    fig = px.bar(
        data,
        x="country",
        y=[
            "exports",
            "imports",
        ],
        barmode="group",
        color_discrete_map={
            "exports": EXPORT_COLOR,
            "imports": IMPORT_COLOR,
        },
        labels={
            "country": "País",
            "value": "Milhões de SIPRI TIV",
            "variable": "Tipo",
        },
        title=(
            f"Exportações × Importações — "
            f"Top {top_n}"
        ),
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=80,
        ),
        title=dict(
            font=dict(size=22),
        ),
        xaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=15),
        ),
        yaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=15),
        ),
        legend=dict(
            font=dict(size=16),
        ),
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "TIV: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    return fig


def create_country_chart(
    country_yearly,
    country,
):

    fig = px.bar(
        country_yearly,
        x="year",
        y=[
            "Exportações",
            "Importações",
        ],
        barmode="group",
        color_discrete_map={
            "Exportações": EXPORT_COLOR,
            "Importações": IMPORT_COLOR,
        },
        labels={
            "year": "Ano",
            "value": "Milhões de SIPRI TIV",
            "variable": "Tipo",
        },
        title=(
            f"{country} — "
            "Exportações × Importações"
        ),
    )

    fig.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=40,
        ),
        title=dict(
            font=dict(size=22),
        ),
        xaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=15),
        ),
        yaxis=dict(
            title_font=dict(size=17),
            tickfont=dict(size=15),
        ),
        legend=dict(
            font=dict(size=16),
        ),
    )

    fig.update_traces(
        hovertemplate=(
            "<b>Ano:</b> %{x}<br>"
            "TIV: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    return fig


def create_country_pie(
    export_total,
    import_total,
):

    data = {
        "Tipo": [
            "Exportações",
            "Importações",
        ],
        "TIV": [
            export_total,
            import_total,
        ],
    }

    fig = px.pie(
        data,
        names="Tipo",
        values="TIV",
        hole=0.45,
        color="Tipo",
        color_discrete_map={
            "Exportações": EXPORT_COLOR,
            "Importações": IMPORT_COLOR,
        },
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(
            size=22,
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "TIV: %{value:,.0f}<br>"
            "Participação: %{percent}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        legend_title_text="Tipo",
        legend=dict(
            font=dict(
                size=17,
            ),
            title=dict(
                font=dict(
                    size=18,
                ),
            ),
        ),
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20,
        ),
    )

    return fig