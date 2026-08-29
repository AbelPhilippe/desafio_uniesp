import streamlit as st
####
from src.config import (
    EXPORTS_DIR,
    IMPORTS_DIR,
    START_YEAR,
    END_YEAR,
    COUNTRY_ISO3,
    EXPORT_COLOR,
    IMPORT_COLOR,
    BACKGROUND_COLOR,
    CARD_COLOR,
    CARD_BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WAR_PERIODS,
)


from src.data import (
    load_all_countries,
    prepare_datasets,
    filter_period,
    get_country_data,
)

from src.analytics import (
    create_ranking,
    calculate_world_total,
    calculate_world_yearly,
    create_comparison,
    create_country_yearly,
    calculate_country_metrics,
    create_map_data,
    count_unique_countries,
    calculate_country_growth,
)

from src.charts import (
    create_world_map,
    create_world_yearly_chart,
    create_participation_chart,
    create_comparison_chart,
    create_country_chart,
    create_country_pie,
    create_balance_chart,
)


st.set_page_config(
    page_title="SIPRI Arms Transfers",
    page_icon="📉",
    layout="wide",
)


st.markdown(f"""
<style>

[data-testid="stMetric"] {{
    text-align: left;
    background-color: {CARD_COLOR};
    border-radius: 5px;
    padding: 10px;
    max-height: 100px;    
    max-width: 300px;
    ;
}}

[data-testid="stMetricLabel"] {{
    text-align: left;
    color:{CARD_BORDER};
    font-size: 10px;
    font-weight: 800;
}}

[data-testid="stMetricValue"] {{
    text-align: left;
    color: {BACKGROUND_COLOR};
    font-size: 28px;
    font-weight: 700;
}}

/* Exportações e Importações */
div[role="radiogroup"] label p {{
    color: {TEXT_SECONDARY} !important;
    font-size: 10px !important;
    font-weight: 600 !important;
}}

</style>
""", unsafe_allow_html=True)

#Título e subtítulo

with st.sidebar:

    st.markdown("""
    <h1 style='text-align: left;'>
        <span style='
            color:#FF4B4B;
            font-size:42px;
            font-weight:700;
        '>
            SIPRI
        </span>
        <br>
        <span style='
            font-size:24px;
            font-weight:500;
        '>
            Transferências internacionais de armas
        </span>
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='
        text-align:left;
        font-size:10px;
        color:{TEXT_SECONDARY};
    '>
        Análise global das transferências internacionais 
        de armas baseada no SIPRI Trend Indicator Value (TIV).
    </p>
    """, unsafe_allow_html=True)


#Adicionar espaçamento entre o título e os filtros

with st.sidebar:

    st.markdown("""
    <hr style="margin-top:20px; margin-bottom:20px;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <h3 style="
        text-align:left;
        color:{TEXT_PRIMARY};
        font-size:14px;
        font-weight:600;
        letter-spacing:1px;
    ">
        FILTROS
    </h3>
    """, unsafe_allow_html=True)


if "war_period" not in st.session_state:
    st.session_state.war_period = "Selecionar"


if "period_slider" not in st.session_state:
    st.session_state.period_slider = (
        START_YEAR,
        END_YEAR,
    )


def select_war():

    selected = st.session_state.war_period

    if selected == "Selecionar":

        st.session_state.period_slider = (
            START_YEAR,
            END_YEAR,
        )

    else:

        war_start, war_end = WAR_PERIODS[selected]

        st.session_state.period_slider = (
            max(START_YEAR, war_start),
            min(END_YEAR, war_end),
        )


def manual_period_change():
    """
    Se o usuário modificar manualmente o slider,
    remove a seleção da guerra.
    """


st.sidebar.markdown(
    f"""
    <div style="
        font-size:12px;
        font-weight:600;
        color:{TEXT_SECONDARY};
        margin-top:8px;
        margin-bottom:0px;
    ">
        Período:
    </div>
    """,
    unsafe_allow_html=True
)


start_year, end_year = st.sidebar.slider(
    "",
    min_value=START_YEAR,
    max_value=END_YEAR,
    key="period_slider",
    on_change=manual_period_change,
)

st.sidebar.markdown(
    f"""
    <div style="
        font-size:12px;
        font-weight:600;
        color:{TEXT_SECONDARY};
        margin-bottom:0px;
    ">
        Quantidade de países:
    </div>
    """,
    unsafe_allow_html=True
)

top_n = st.sidebar.slider(
    "",
    min_value=5,
    max_value=30,
    value=10,
)


if not EXPORTS_DIR.exists():

    st.error(
        "Diretório de exportações não encontrado:\n\n"
        f"{EXPORTS_DIR}"
    )

    st.stop()


if not IMPORTS_DIR.exists():

    st.error(
        "Diretório de importações não encontrado:\n\n"
        f"{IMPORTS_DIR}"
    )

    st.stop()


if not IMPORTS_DIR.exists():

    st.error(
        "Diretório de importações não encontrado:\n\n"
        f"{IMPORTS_DIR}"
    )

    st.stop()


exports_df = load_all_countries(
    EXPORTS_DIR
)

imports_df = load_all_countries(
    IMPORTS_DIR
)


if exports_df.empty:

    st.error(
        "Nenhum dado de exportação foi encontrado."
    )

    st.stop()


if imports_df.empty:

    st.error(
        "Nenhum dado de importação foi encontrado."
    )

    st.stop()


(
    exports_countries_df,
    imports_countries_df,
    world_export_df,
    world_import_df,
) = prepare_datasets(
    exports_df,
    imports_df,
)


exports_period = filter_period(
    exports_countries_df,
    start_year,
    end_year,
)

imports_period = filter_period(
    imports_countries_df,
    start_year,
    end_year,
)

world_export_period = filter_period(
    world_export_df,
    start_year,
    end_year,
)

world_import_period = filter_period(
    world_import_df,
    start_year,
    end_year,
)


with st.sidebar:

    st.markdown(
        f"""
        <div style="
            font-size:12px;
            font-weight:600;
            color:{TEXT_SECONDARY};
            margin-bottom:-15px;
        ">
            Tipo de Mapa:
        </div>
        """,
        unsafe_allow_html=True
    )

    map_type = st.radio(
        "",
        [
            "Exportações",
            "Importações",
        ],
        horizontal=True,
    )

    map_source = (
        exports_period
        if map_type == "Exportações"
        else imports_period
    )


total_world_transfer = calculate_world_total(
    world_export_period,
)

total_active_countries = count_unique_countries(
    map_source
)

avg_annual_transfer = (
    total_world_transfer
    / (end_year - start_year + 1)
)

top_country_export = (
    create_ranking(exports_period)
    .iloc[0]["country"]
)

top_country_import = (
    create_ranking(imports_period)
    .iloc[0]["country"]
)

country_iso_export = COUNTRY_ISO3.get(
    top_country_export.lower(),
    "N/A",
)

country_iso_import = COUNTRY_ISO3.get(
    top_country_import.lower(),
    "N/A",
)

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    with st.container(border=False):
        st.metric(
        "Total Global (TIV):",
       f"{total_world_transfer / 1_000:.2f}K",
    )

with col2:

    with st.container(border=False):
        st.metric(
            "Média Anual (TIV):",
            f"{avg_annual_transfer / 1_000:.2f}K",
        )

with col3:

    with st.container(border=False):
        st.metric(
            "Países Ativos:",
            f"{total_active_countries}",
        )

with col4:

    with st.container(border=False):
        st.metric(
            "Maior exportador:",
            f"{country_iso_export}",
        )

with col5:

    with st.container(border=False):
        st.metric(
            "Maior importador:",
            f"{country_iso_import}",
        )        

export_ranking = create_ranking(
    exports_period
)

import_ranking = create_ranking(
    imports_period
)

comparison = create_comparison(
    export_ranking,
    import_ranking,
    map_type,
)

war_period = st.select_slider(
    "Conflito histórico",
    options=list(WAR_PERIODS.keys()),
    key="war_period",
    on_change=select_war,
)

col1, col2 = st.columns(
    [3,2],
    gap="small")

with col1:

    with st.container(border=False):
        map_df = create_map_data(
            map_source,
            COUNTRY_ISO3,
        )
    with st.container(border=False):
        fig_map = create_world_map(
            map_df,
            map_type,
            start_year,
            end_year,
        )

        st.plotly_chart(
        fig_map,
        use_container_width=True,
        )

with col2:
    
    with st.container(border=False):  
        comparison_display = (
            comparison[
                [
                    "country",
                    "exports",
                    "imports",
                    "net",
                ]
            ]
            .reset_index(drop=True)
            .rename(
                columns={
                    "country": "País",
                    "exports": "Exp.(K TIV)",
                    "imports": "Imp.(K TIV)",
                    "net": "Saldo",
                }
            )
        )
        comparison_display["Exp.(K TIV)"] = (
            comparison_display["Exp.(K TIV)"] / 1_000
        )

        comparison_display["Imp.(K TIV)"] = (
            comparison_display["Imp.(K TIV)"] / 1_000
        )

        comparison_display["Saldo"] = (
            comparison_display["Saldo"] / 1_000
        )
    

        comparison_display.insert(
            0,
            "#",
            range(1, len(comparison_display) + 1),
        )

    st.dataframe(
        comparison_display.style.format({
            "Exp.(K TIV)": "{:,.0f}",
            "Imp.(K TIV)": "{:,.0f}",
            "Saldo": "{:,.0f}",
        }),
        use_container_width=True,
        hide_index=True,
        height=500,
    )


col1, col2 = st.columns(2)


with col1:

    if world_export_period.empty:

        st.warning(
            "Não foram encontrados dados de "
            "Total World Export para o período."
        )

    else:

        yearly = calculate_world_yearly(
            world_export_period
        )

        fig = create_world_yearly_chart(
            yearly,
            (
                f"Total World Export — "
                f"{start_year}–{end_year}"
            ),
            EXPORT_COLOR,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
            "displayModeBar": False,
            "staticPlot": True,
            },
        )


with col2:

    if world_import_period.empty:

        st.warning(
            "Não foram encontrados dados de "
            "Total World Import para o período."
        )

    else:

        yearly = calculate_world_yearly(
            world_import_period
        )

        fig = create_world_yearly_chart(
            yearly,
            (
                f"Total World Import — "
                f"{start_year}–{end_year}"
            ),
            IMPORT_COLOR,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
            "displayModeBar": False,
            "staticPlot": True,
            },
        )


col1, col2 = st.columns(2)


with col1:

    fig_trade = create_comparison_chart(
        comparison,
        top_n=10,
    )

    fig_trade.update_layout(
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        legend_title=None,
    )

    st.plotly_chart(
        fig_trade,
        use_container_width=True,
        config={
        "displayModeBar": False,
        "staticPlot": True,
        },
    )

with col2:

    fig_balance = create_balance_chart(
        comparison,
        top_n=10,
    )

    fig_balance.update_layout(
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        legend_title=None,
    )

    st.plotly_chart(
        fig_balance,
        use_container_width=True,
        config={
        "displayModeBar": False,
        "staticPlot": True,
        },
    )

st.markdown("")

with st.expander(
    "Qual país dominou o comércio global?"
):
    st.markdown(
        f"""
        <div style="
            font-size:14px;
            line-height:2;
            color:{TEXT_SECONDARY};
        ">
            Os <span style="
                color:{EXPORT_COLOR};
                font-weight:700;
            ">
                Estados Unidos
            </span>
            lideraram o comércio internacional de armamentos no
            período analisado, concentrando o maior volume
            de transferências.
        </div>
        """,
        unsafe_allow_html=True,
)

with st.expander(
"Qual país apresentou o maior saldo exportador?"
):
    st.markdown(
        f"""
        <div style="
            font-size:14px;
            line-height:2;
            color:{TEXT_SECONDARY};
        ">
            <span style="
                color:{EXPORT_COLOR};
                font-weight:700;
            ">
                Estados Unidos
            </span>
            apresentaram o maior saldo positivo entre
            exportações de armamentos
            no período analisado.
        </div>
        """,
        unsafe_allow_html=True,
)

with st.expander(
"Qual país dependeu mais de importações?"
):
    st.markdown(
        f"""
        <div style="
            font-size:14px;
            line-height:2;
            color:{TEXT_SECONDARY};
        ">
            <span style="
                color:{IMPORT_COLOR};
                font-weight:700;
            ">
                Índia
            </span>
            apresentou o maior volume líquido de
            importações entre os países analisados.
        </div>
        """,
        unsafe_allow_html=True,
)

comparison["total_trade"] = (
    comparison["exports"]
    + comparison["imports"]
)

top5_share = (
    comparison
    .sort_values(
        "total_trade",
        ascending=False,
    )
    .head(5)["total_trade"]
    .sum()
    /
    comparison["total_trade"]
    .sum()
)

with st.expander(
    "Onde o comércio global é concentrado?"
):
    st.markdown(
        f"""
        <div style="
            font-size:14px;
            line-height:2;
            color:{TEXT_SECONDARY};
        ">
            Os cinco maiores participantes concentraram
            aproximadamente
            <span style="
                color:{CARD_COLOR};
                font-weight:700;
            ">
                {top5_share:.0%}
            </span>
            de todo o comércio internacional de armamentos
            entre <span style="
                color:{EXPORT_COLOR};
                font-weight:700;
            ">
                {start_year}
            </span>
            e
            <span style="
                color:{EXPORT_COLOR};
                font-weight:700;
            ">
                {end_year}
            </span>.
            Esse nível de concentração indica que poucas
            nações exercem forte influência sobre os fluxos
            globais de armamentos.
        </div>
        """,
        unsafe_allow_html=True,
)


st.subheader(
    "Tabela — Exportações X Importações"
)

st.divider()

st.header("Análise individual")


countries = sorted(
    set(
        exports_countries_df[
            "country"
        ].unique()
    )
    |
    set(
        imports_countries_df[
            "country"
        ].unique()
    )
)


country = st.selectbox(
    "Selecione um país",
    countries,
)


country_exports, country_imports = get_country_data(
    exports_countries_df,
    imports_countries_df,
    country,
    start_year,
    end_year,
)


metrics = calculate_country_metrics(
    country_exports,
    country_imports,
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Exportações",
    f"{metrics['export_total']:,.0f}",
)

col2.metric(
    "Importações",
    f"{metrics['import_total']:,.0f}",
)

col3.metric(
    "Média exportada / ano",
    f"{metrics['export_average']:,.0f}",
)

col4.metric(
    "Média importada / ano",
    f"{metrics['import_average']:,.0f}",
)


st.subheader(
    f"Transferências de {country}"
)


country_yearly = create_country_yearly(
    country_exports,
    country_imports,
)


fig_country = create_country_chart(
    country_yearly,
    country,
)


st.plotly_chart(
    fig_country,
    use_container_width=True,
)

st.subheader(
    f"Proporção e dados — {country}"
)


col1, col2 = st.columns(
    [1, 1.5]
)


with col1:

    fig = create_country_pie(
        metrics["export_total"],
        metrics["import_total"],
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with col2:

    st.markdown(
        f"**Dados anuais de {country}**"
    )

    country_yearly_display = (
        country_yearly
        .rename(
            columns={
                "year": "Ano",
            }
        )
    )

    st.dataframe(
        country_yearly_display,
        use_container_width=True,
        hide_index=True,
        height=430,
    )

st.divider()

st.header("Dados dos rankings")


tab1, tab2 = st.tabs(
    [
        "Exportadores",
        "Importadores",
    ]
)


with tab1:

    export_display = (
        export_ranking
        .copy()
    )

    export_display.index = range(
        1,
        len(export_display) + 1,
    )

    export_display.index.name = "Posição"

    export_display = (
        export_display
        .rename(
            columns={
                "country": "País",
                "tiv": "TIV",
            }
        )
    )

    st.dataframe(
        export_display,
        use_container_width=True,
    )


with tab2:

    import_display = (
        import_ranking
        .copy()
    )

    import_display.index = range(
        1,
        len(import_display) + 1,
    )

    import_display.index.name = "Posição"

    import_display = (
        import_display
        .rename(
            columns={
                "country": "País",
                "tiv": "TIV",
            }
        )
    )

    st.dataframe(
        import_display,
        use_container_width=True,
    )

st.divider()


st.divider()

st.header(" Insights")

st.markdown(
    f"""
    Crescimento percentual das transferências entre
    **{start_year}** e **{end_year}**.
    """
)


st.subheader(
    f"Crescimento das importações — {start_year} → {end_year}"
)

import_growth = calculate_country_growth(
    imports_countries_df,
    start_year,
    end_year,
)

if import_growth.empty:

    st.info(
        "Não há dados suficientes para calcular "
        "o crescimento no período."
    )

else:

    import_growth_display = (
        import_growth[
            [
                "country",
                "growth",
            ]
        ]
        .rename(
            columns={
                "country": "País",
                "growth": "Crescimento (%)",
            }
        )
    )

    import_growth_display[
        "Crescimento (%)"
    ] = (
        import_growth_display[
            "Crescimento (%)"
        ]
        .round(2)
    )

    st.dataframe(
        import_growth_display,
        use_container_width=True,
        hide_index=True,
    )


st.subheader(
    f"Crescimento das exportações — {start_year} → {end_year}"
)

export_growth = calculate_country_growth(
    exports_countries_df,
    start_year,
    end_year,
)

# Verificação extra
if export_growth.empty:

    st.info(
        "Não há dados suficientes para calcular "
        "o crescimento no período."
    )

else:

    export_growth_display = (
        export_growth[
            [
                "country",
                "growth",
            ]
        ]
        .rename(
            columns={
                "country": "País",
                "growth": "Crescimento (%)",
            }
        )
    )

    export_growth_display[
        "Crescimento (%)"
    ] = (
        export_growth_display[
            "Crescimento (%)"
        ]
        .round(2)
    )

    st.dataframe(
        export_growth_display,
        use_container_width=True,
        hide_index=True,
    )


st.caption(
    "Fonte: SIPRI Arms Transfers Database. "
    "Os valores são expressos em Trend-Indicator "
    "Values (TIV) e não representam preços ou "
    "valores financeiros de mercado."
)