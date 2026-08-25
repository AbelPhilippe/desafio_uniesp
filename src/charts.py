import plotly.express as px

from src.config import (
    COUNTRY_PALETTE,
    EXPORT_COLOR,
    IMPORT_COLOR,
    MAP_EXPORT_SCALE,
    MAP_IMPORT_SCALE,
)

def create_world_map(
    map_df,
    map_type,
    start_year,
    end_year,
):
    
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
        colorbar_title="Milhões de TIV"
    )

    fig.update_layout(
        height=650,
        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0,
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
        )
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
        hovertemplate=(
            "<b>%{label}</b><br>"
            "TIV: %{value:,.0f}<br>"
            "Participação: %{percent}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        legend_title_text="Países",
        margin=dict(
            l=20,
            r=20,
            t=50,
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
        )
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
        hovertemplate=(
            "<b>%{label}</b><br>"
            "TIV: %{value:,.0f}<br>"
            "Participação: %{percent}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        legend_title_text="Tipo",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20,
        ),
    )

    return fig