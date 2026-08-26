import streamlit as st

from src.config import (
    EXPORTS_DIR,
    IMPORTS_DIR,
    START_YEAR,
    END_YEAR,
    COUNTRY_ISO3,
    EXPORT_COLOR,
    IMPORT_COLOR,
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
)

from src.charts import (
    create_world_map,
    create_world_yearly_chart,
    create_participation_chart,
    create_comparison_chart,
    create_country_chart,
    create_country_pie,
)


st.set_page_config(
    page_title="SIPRI Arms Transfers",
    page_icon="🌎",
    layout="wide",
)


st.title("SIPRI Arms Transfers")

st.caption(
    "Análise de transferências internacionais de armas "
    "com base no SIPRI Trend-Indicator Value (TIV)."
)


st.sidebar.header("Filtros")

st.sidebar.subheader("Período")

start_year, end_year = st.sidebar.slider(
    "Selecione o período",
    min_value=START_YEAR,
    max_value=END_YEAR,
    value=(START_YEAR, END_YEAR),
)


st.sidebar.subheader("Ranking")

top_n = st.sidebar.slider(
    "Quantidade de países",
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


st.header(
    f"Transferências mundiais — "
    f"{start_year}–{end_year}"
)


st.subheader(
    "Mapa mundial de transferências"
)

st.caption(
    f"Volume acumulado de transferências entre "
    f"{start_year} e {end_year}, segundo o SIPRI TIV."
)


map_type = st.radio(
    "Indicador do mapa",
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


st.subheader("")

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


col1, col2, col3, col4 = st.columns(4)


with col1:
    with st.container(border=True):
        st.metric(
        "Global Arms Transfer *TIV*",
       f"{total_world_transfer / 1_000_000:.2f}M",
    )

with col2:

    with st.container(border=True):
        st.metric(
            "Average Annual Transfer",
            f"{avg_annual_transfer / 1_000_000:.2f}M",
        )

with col3:

    with st.container(border=True):
        st.metric(
            "Active Countries",
            f"{total_active_countries} tracked",
        )

with col4:

    with st.container(border=True):
        st.metric(
            "Top Exporting Country",
            f"{top_country_export}",
        )


st.caption(
    "Valores expressos em milhões de "
    "SIPRI Trend-Indicator Values (TIV)."
)


map_df = create_map_data(
    map_source,
    COUNTRY_ISO3,
)


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



st.header("Totais mundiais por ano")

col1, col2 = st.columns(2)


with col1:

    st.subheader("Total World Export")

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
        )


with col2:

    st.subheader("Total World Import")

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
        )


export_ranking = create_ranking(
    exports_period
)

import_ranking = create_ranking(
    imports_period
)


st.header("Ranking mundial")

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        f"Top {top_n} exportadores"
    )

    data = (
        export_ranking
        .head(top_n)
        .sort_values("tiv")
        .set_index("country")["tiv"]
    )

    st.bar_chart(
        data,
        horizontal=True,
        x_label="Milhões de SIPRI TIV",
        y_label="País",
        color=EXPORT_COLOR,
    )


with col2:

    st.subheader(
        f"Top {top_n} importadores"
    )

    data = (
        import_ranking
        .head(top_n)
        .sort_values("tiv")
        .set_index("country")["tiv"]
    )

    st.bar_chart(
        data,
        horizontal=True,
        x_label="Milhões de SIPRI TIV",
        y_label="País",
        color=IMPORT_COLOR,
    )


st.header("Participação mundial")

col1, col2 = st.columns(2)


with col1:

    fig = create_participation_chart(
        export_ranking,
        top_n,
        "Participação dos exportadores",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with col2:

    fig = create_participation_chart(
        import_ranking,
        top_n,
        "Participação dos importadores",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


st.header(
    "Exportações × Importações"
)


comparison = create_comparison(
    export_ranking,
    import_ranking,
)


fig_comparison = create_comparison_chart(
    comparison,
    top_n,
)


st.plotly_chart(
    fig_comparison,
    use_container_width=True,
)


st.subheader(
    "Tabela — Exportações × Importações"
)


comparison_display = (
    comparison[
        [
            "country",
            "exports",
            "imports",
            "net",
        ]
    ]
    .rename(
        columns={
            "country": "País",
            "exports": "Exportações",
            "imports": "Importações",
            "net": "Saldo",
        }
    )
)


st.dataframe(
    comparison_display,
    use_container_width=True,
    hide_index=True,
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

st.caption(
    "Fonte: SIPRI Arms Transfers Database. "
    "Os valores são expressos em Trend-Indicator "
    "Values (TIV) e não representam preços ou "
    "valores financeiros de mercado."
)