import streamlit as st

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
)

from src.analytics import (
    create_ranking,
    calculate_world_total,
    calculate_world_yearly,
    create_comparison,
    create_map_data,
    count_unique_countries,
)

from src.charts import (
    create_balance_chart,
    create_world_map,
    create_world_yearly_chart,
    create_comparison_chart,
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

    st.markdown(f"""
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

    st.markdown(f"""
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
       f"{total_world_transfer / 1_000_000:.2f}M",
    )

with col2:

    with st.container(border=False):
        st.metric(
            "Média Anual (TIV):",
            f"{avg_annual_transfer / 1_000_000:.2f}M",
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

st.select_slider(
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
                    "exports": "Exp.(M TIV)",
                    "imports": "Imp.(M TIV)",
                    "net": "Saldo",
                }
            )
        )
        comparison_display["Exp.(M TIV)"] = (
            comparison_display["Exp.(M TIV)"] / 1_000_000
        )

        comparison_display["Imp.(M TIV)"] = (
            comparison_display["Imp.(M TIV)"] / 1_000_000
        )

        comparison_display["Saldo"] = (
            comparison_display["Saldo"] / 1_000_000
        )
    

        comparison_display.insert(
            0,
            "#",
            range(1, len(comparison_display) + 1),
        )

    st.dataframe(
        comparison_display.style.format({
            "Exp.(M TIV)": "{:,.2f}",
            "Imp.(M TIV)": "{:,.2f}",
            "Saldo": "{:,.2f}",
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


st.divider()
