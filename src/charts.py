import plotly.express as px
import numpy as np

from src.config import (
    CARD_BORDER,
    CHART_TITLE_SIZE,
    AXIS_TITLE_SIZE,
    AXIS_LABEL_SIZE,
    BACKGROUND_COLOR,
    COUNTRY_PALETTE,
    EXPORT_COLOR,
    IMPORT_COLOR,
    MAP_EXPORT_SCALE,
    MAP_IMPORT_SCALE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    MAP_LAND_COLOR,
)

def hex_to_rgba(hex_color, alpha):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r},{g},{b},{alpha})"

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
        projection="robinson",
        labels={
            "TIV": "Milhões de SIPRI TIV",
        },
        title=f"{map_type} — {start_year}–{end_year}",
    )

    fig.update_traces(
        marker_line_width=0.05,
        marker_line_color="rgba(255,255,255,0.04)",
    )

    fig.update_layout(
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
    )

    fig.update_traces(
        marker_line_color="rgba(255,255,255,0.05)",
        marker_line_width=0.2,
    )

    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        showland=True,
        landcolor=MAP_LAND_COLOR,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.05)",
        countrywidth=0.2,
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
        ),
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
    height=400,
):
    MAX_Y= 70_000
    ticks = np.linspace(
        0,
        MAX_Y,
        5
    )

    fig = px.line(
        yearly_df,
        x="year",
        y="tiv",
        labels={
            "year": "Ano",
            "tiv": "M.TIV",
        },
        title=title,
    )

    fig.update_traces(
        opacity=0.70,
        line=dict(
            color=color,
            width=1,
        ),
        fill="tozeroy",
        fillcolor=hex_to_rgba(color, 0.1),
        hovertemplate=(
            "<b>Ano:</b> %{x}<br>"
            "<b>TIV:</b> %{y:,.0f}"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        dragmode=False,
        height=height,

        title=dict(
            font=dict(
                size=CHART_TITLE_SIZE,
                color=TEXT_PRIMARY,
            ),
            x=0,
            xanchor="left",
        ),

        xaxis=dict(
            title_font=dict(
                size=AXIS_TITLE_SIZE,
                color=TEXT_SECONDARY,
            ),
            tickfont=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),
        ),

        yaxis=dict(
            title_font=dict(
                size=AXIS_TITLE_SIZE,
                color=TEXT_SECONDARY,
            ),
            tickfont=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),
            range=[0, MAX_Y],
            tickvals=ticks,
            ticktext=[
                f"{x/1_000_000:.2f}M"
                for x in ticks
            ],
            showgrid=True,
            gridcolor=TEXT_SECONDARY,
            gridwidth=0.1,
            griddash="dot",
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
    top_n=10,
):

    data = comparison.copy()

    data["total_trade"] = (
        data["exports"]
        + data["imports"]
    )

    data = (
        data
        .sort_values(
            "total_trade",
            ascending=False,
        )
        .head(top_n)
    )

    fig = px.bar(
        data,
        y="country",
        x=[
            "exports",
            "imports",
        ],
        orientation="h",
        barmode="stack",
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
            f"Top {top_n} Países - Comércio Global"
        ),
    )

    max_trade = (
        data["total_trade"].max()
    )

    ticks = np.linspace(
        0,
        max_trade,
        5,
    )

    MAX_X = 1_000_000

    ticks = np.linspace(
        0,
        MAX_X,
        5,
    )

    fig.update_layout(
        dragmode=False,
        height=580,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
        title=dict(
            font=dict(
                size=CHART_TITLE_SIZE,
                color=TEXT_PRIMARY,
            ),
            x=0,
            xanchor="left",
        ),
        xaxis=dict(
            title="M.TIV",

            title_font=dict(
                size=AXIS_TITLE_SIZE,
                color=TEXT_SECONDARY,
            ),

            tickfont=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),

            range=[0, MAX_X],
            tickvals=ticks,
            ticktext=[
                f"{x/1_000_000:.2f}M"
                for x in ticks
            ],

            showgrid=True,
            gridcolor=TEXT_SECONDARY,
            gridwidth=0.1,
            griddash="dot",
        ),       
        yaxis=dict(
            title=None,              
            autorange="reversed",
            tickfont=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),
        ),
        legend=dict(
            orientation="h",
            y=0.99,
            x=1,
            xanchor="right",
            yanchor="bottom",
            title=None,
            font=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),
        ),
    )

    fig.update_traces(
        opacity=0.8,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "TIV: %{x:,.0f}"
            "<extra></extra>"
        )
    )

    return fig


def create_balance_chart(
    comparison,
    top_n=10,
):

    data = comparison.copy()

    data = (
        data
        .sort_values(
            "net",
            key=abs,
            ascending=False,
        )
        .head(top_n)
    )

    data["status"] = data["net"].apply(
        lambda x:
        "Exportador Líquido"
        if x >= 0
        else "Importador Líquido"
    )

    fig = px.bar(
        data,
        x="net",
        y="country",
        orientation="h",
        color="status",
        color_discrete_map={
            "Exportador Líquido": EXPORT_COLOR,
            "Importador Líquido": IMPORT_COLOR,
        },
        labels={
            "country": "País",
            "net": "M.TIV",
            "status": "Status",
        },
        title="Saldo Comercial de Armamentos",
    )

    max_balance = abs(data["net"]).max()

    ticks = np.linspace(
        -max_balance,
        max_balance,
        5,
    )

    fig.update_layout(
        height=350,

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),

        title=dict(
            font=dict(
                size=CHART_TITLE_SIZE,
                color=TEXT_PRIMARY,
            ),
            x=0,
            xanchor="left",
        ),

        bargap=0.20,

        legend=dict(
            orientation="h",
            y=1.02,
            x=1,
            xanchor="right",
            yanchor="bottom",
            title=None,
            font=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),
        ),

        xaxis=dict(
            title="Saldo Comercial (M.TIV)",

            tickvals=ticks,

            ticktext=[
                f"{x/1_000_000:.2f}M"
                for x in ticks
            ],

            title_font=dict(
                size=AXIS_TITLE_SIZE,
                color=TEXT_SECONDARY,
            ),

            tickfont=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),

            zeroline=True,
            zerolinewidth=1,
            zerolinecolor=TEXT_SECONDARY,

            showgrid=True,
            gridcolor=TEXT_SECONDARY,
            gridwidth=0.2,
            griddash="dot",
        ),

        yaxis=dict(
            title=None,

            tickfont=dict(
                size=AXIS_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),

            autorange="reversed",
        ),
    )

    fig.update_traces(
        opacity=0.85,

        textposition="auto",

        hovertemplate=(
            "<b>%{y}</b><br>"
            "Saldo: %{x:,.0f}"
            "<extra></extra>"
        ),
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