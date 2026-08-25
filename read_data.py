from pathlib import Path
import csv
import re

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"

START_YEAR = 1950
END_YEAR = 2025

def clean_cell(value: str) -> str:
    """Limpa o conteúdo de uma célula."""

    if value is None:
        return ""

    value = str(value).strip()

    # Essa linha aqui remove BOM
    value = value.replace("\ufeff", "")

    return value.strip()


def safe_name(value: str) -> str:
    """Transforma texto em nome seguro para arquivo/diretório."""

    value = clean_cell(value)
    value = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        value
    )

    value = re.sub(
        r"\s+",
        "_",
        value
    )

    value = re.sub(
        r"_+",
        "_",
        value
    )

    return value.strip("_")

def detect_delimiter(file_path: Path) -> str:

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        sample = file.read(8192)

    try:

        dialect = csv.Sniffer().sniff(
            sample,
            delimiters=",;|\t"
        )

        return dialect.delimiter

    except csv.Error:

        return ","

def read_csv(file_path: Path):

    delimiter = detect_delimiter(
        file_path
    )

    print(
        f"  Separador detectado: "
        f"{repr(delimiter)}"
    )

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.reader(
            file,
            delimiter=delimiter
        )

        return list(reader)

def find_header(rows):
    """
    Procura a linha que contém os anos.

    Exemplo:

    Exports by,1950,1951,...,2025,1950-2025,...

    Retorna:

        índice da linha
        conteúdo do cabeçalho
    """

    for row_index, row in enumerate(rows):

        cells = [
            clean_cell(cell)
            for cell in row
        ]

        if not cells:
            continue

        years_found = []

        for cell in cells:

            if re.fullmatch(
                r"\d{4}",
                cell
            ):

                year = int(cell)

                if (
                    START_YEAR
                    <= year
                    <= END_YEAR
                ):
                    years_found.append(
                        year
                    )

        # Obs: 5 anos já são suficientes para
        #      identificar a linha como cabeçalho.
        if len(years_found) >= 5:

            identifier = cells[0]

            if identifier:

                return (
                    row_index,
                    cells
                )

    return None, None

def get_year_indexes(header):

    year_indexes = {}

    for index, column in enumerate(header):

        column = clean_cell(column)

        if re.fullmatch(
            r"\d{4}",
            column
        ):

            year = int(column)

            if (
                START_YEAR
                <= year
                <= END_YEAR
            ):

                year_indexes[year] = index

    return year_indexes

def parse_value(value):

    value = clean_cell(value)

    if value == "":
        return ""

    # Mantém o 0 como 0
    try:

        number = float(value)

        if number.is_integer():
            return int(number)

        return number

    except ValueError:

        return value

def process_file(file_path: Path):

    print()
    print("=" * 70)
    print(f"CSV: {file_path.name}")
    print("=" * 70)

    rows = read_csv(
        file_path
    )

    if not rows:

        print("[ERRO] CSV vazio.")
        return

    header_index, header = find_header(
        rows
    )

    if header is None:

        print(
            "[ERRO] Não encontrei uma linha "
            "com os anos 1950-2025."
        )

        return

    reference = clean_cell(
        header[0]
    )

    print(
        f"Referência encontrada: "
        f"'{reference}'"
    )

    reference_name = safe_name(
        reference
    ).lower()

    output_directory = (
        OUTPUT_DIR
        / f"Country_{reference_name}"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"Diretório de saída: "
        f"{output_directory}"
    )

    year_indexes = get_year_indexes(
        header
    )

    expected_years = (
        END_YEAR
        - START_YEAR
        + 1
    )

    print(
        f"Anos encontrados: "
        f"{len(year_indexes)}"
    )

    if len(year_indexes) != expected_years:

        print(
            f"[AVISO] Esperados "
            f"{expected_years} anos."
        )

    countries_created = 0

    for row in rows[
        header_index + 1:
    ]:

        if not row:
            continue

        country = clean_cell(
            row[0]
        )

        if not country:
            continue

        if country.lower() in (
            "source",
            "data generated",
            "figures",
            "recipient",
            "supplier",
            "exports by",
            "imports by"
        ):
            continue

        country_name = safe_name(
            country
        )

        if not country_name:
            continue

        output_file = (
            output_directory
            / f"{country_name}.csv"
        )

        with output_file.open(
            "w",
            encoding="utf-8",
            newline=""
        ) as file:

            writer = csv.writer(
                file
            )

            writer.writerow([
                "country",
                "year",
                "tiv"
            ])

            for year in range(
                START_YEAR,
                END_YEAR + 1
            ):

                column_index = (
                    year_indexes.get(year)
                )

                if (
                    column_index is None
                    or column_index >= len(row)
                ):

                    value = ""

                else:

                    value = parse_value(
                        row[column_index]
                    )

                writer.writerow([
                    country,
                    year,
                    value
                ])

        countries_created += 1

        print(
            f"  [OK] {country}"
        )

    print(
        f"\nPaíses criados: "
        f"{countries_created}"
    )

def main():
    csv_files = sorted(
        BASE_DIR.glob("*.csv")
    )

    if not csv_files:

        print(
            "[ERRO] Nenhum CSV encontrado em:"
        )

        print(
            BASE_DIR
        )

        return

    print(
        f"Encontrados {len(csv_files)} CSV(s):"
    )

    for file_path in csv_files:

        print(
            f"  - {file_path.name}"
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    for file_path in csv_files:

        try:

            process_file(
                file_path
            )

        except Exception as error:

            print(
                f"\n[ERRO] Falha ao processar "
                f"{file_path.name}:"
            )

            print(
                f"       {error}"
            )

    print()
    print("=" * 25)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 25)


if __name__ == "__main__":
    main()