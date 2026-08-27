from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EXPORTS_DIR = (
    BASE_DIR
    / "output"
    / "Country_exports_by"
)

IMPORTS_DIR = (
    BASE_DIR
    / "output"
    / "Country_recipient"
)

START_YEAR = 1950
END_YEAR = 2025

EXPORT_COLOR = "#2563EB"
EXPORT_LIGHT = "#60A5FA"

IMPORT_COLOR = "#F97316"
IMPORT_LIGHT = "#FDBA74"

POSITIVE_COLOR = "#16A34A"
NEGATIVE_COLOR = "#DC2626"

NEUTRAL_COLOR = "#64748B"

BACKGROUND_COLOR = "#F1DDDD"
CARD_COLOR = "#FF4B4B"
CARD_BORDER = "#852D2D"

TEXT_PRIMARY = "#F8FAFC"
TEXT_SECONDARY = "#7D7E80"


COUNTRY_PALETTE = [
    "#2563EB",
    "#F97316",
    "#16A34A",
    "#9333EA",
    "#0891B2",
    "#E11D48",
    "#CA8A04",
    "#4F46E5",
    "#059669",
    "#DB2777",
    "#7C3AED",
    "#EA580C",
]


MAP_EXPORT_SCALE = [
    [0.00, "#EFF6FF"],
    [0.20, "#BFDBFE"],
    [0.40, "#60A5FA"],
    [0.60, "#2563EB"],
    [0.80, "#1D4ED8"],
    [1.00, "#1E3A8A"],
]


MAP_IMPORT_SCALE = [
    [0.00, "#FFF7ED"],
    [0.20, "#FED7AA"],
    [0.40, "#FDBA74"],
    [0.60, "#F97316"],
    [0.80, "#EA580C"],
    [1.00, "#9A3412"],
]


WORLD_EXPORT_NAMES = {
    "total world export",
    "total_world_export",
    "total world exports",
    "total_world_exports",
}


WORLD_IMPORT_NAMES = {
    "total world import",
    "total_world_import",
    "total world imports",
    "total_world_imports",
}

COUNTRY_ISO3 = {
    "afghanistan": "AFG",
    "albania": "ALB",
    "algeria": "DZA",
    "angola": "AGO",
    "argentina": "ARG",
    "armenia": "ARM",
    "australia": "AUS",
    "austria": "AUT",
    "azerbaijan": "AZE",
    "bahamas": "BHS",
    "bahrain": "BHR",
    "bangladesh": "BGD",
    "belarus": "BLR",
    "belgium": "BEL",
    "belize": "BLZ",
    "benin": "BEN",
    "bhutan": "BTN",
    "bolivia": "BOL",
    "bosnia and herzegovina": "BIH",
    "botswana": "BWA",
    "brazil": "BRA",
    "brunei": "BRN",
    "bulgaria": "BGR",
    "burkina faso": "BFA",
    "burundi": "BDI",
    "cambodia": "KHM",
    "cameroon": "CMR",
    "canada": "CAN",
    "cape verde": "CPV",
    "central african republic": "CAF",
    "chad": "TCD",
    "chile": "CHL",
    "china": "CHN",
    "colombia": "COL",
    "comoros": "COM",
    "congo": "COG",
    "democratic republic of the congo": "COD",
    "costa rica": "CRI",
    "croatia": "HRV",
    "cuba": "CUB",
    "cyprus": "CYP",
    "czech republic": "CZE",
    "czechia": "CZE",
    "denmark": "DNK",
    "djibouti": "DJI",
    "dominican republic": "DOM",
    "ecuador": "ECU",
    "egypt": "EGY",
    "el salvador": "SLV",
    "equatorial guinea": "GNQ",
    "eritrea": "ERI",
    "estonia": "EST",
    "ethiopia": "ETH",
    "fiji": "FJI",
    "finland": "FIN",
    "france": "FRA",
    "gabon": "GAB",
    "gambia": "GMB",
    "georgia": "GEO",
    "germany": "DEU",
    "ghana": "GHA",
    "greece": "GRC",
    "guatemala": "GTM",
    "guinea": "GIN",
    "guinea bissau": "GNB",
    "guyana": "GUY",
    "haiti": "HTI",
    "honduras": "HND",
    "hungary": "HUN",
    "iceland": "ISL",
    "india": "IND",
    "indonesia": "IDN",
    "iran": "IRN",
    "iraq": "IRQ",
    "ireland": "IRL",
    "israel": "ISR",
    "italy": "ITA",
    "jamaica": "JAM",
    "japan": "JPN",
    "jordan": "JOR",
    "kazakhstan": "KAZ",
    "kenya": "KEN",
    "kuwait": "KWT",
    "kyrgyzstan": "KGZ",
    "laos": "LAO",
    "latvia": "LVA",
    "lebanon": "LBN",
    "liberia": "LBR",
    "libya": "LBY",
    "lithuania": "LTU",
    "luxembourg": "LUX",
    "madagascar": "MDG",
    "malawi": "MWI",
    "malaysia": "MYS",
    "maldives": "MDV",
    "mali": "MLI",
    "malta": "MLT",
    "mauritania": "MRT",
    "mauritius": "MUS",
    "mexico": "MEX",
    "moldova": "MDA",
    "mongolia": "MNG",
    "montenegro": "MNE",
    "morocco": "MAR",
    "mozambique": "MOZ",
    "myanmar": "MMR",
    "namibia": "NAM",
    "nepal": "NPL",
    "netherlands": "NLD",
    "new zealand": "NZL",
    "nicaragua": "NIC",
    "niger": "NER",
    "nigeria": "NGA",
    "north korea": "PRK",
    "north macedonia": "MKD",
    "norway": "NOR",
    "oman": "OMN",
    "pakistan": "PAK",
    "panama": "PAN",
    "papua new guinea": "PNG",
    "paraguay": "PRY",
    "peru": "PER",
    "philippines": "PHL",
    "poland": "POL",
    "portugal": "PRT",
    "qatar": "QAT",
    "romania": "ROU",
    "russia": "RUS",
    "rwanda": "RWA",
    "saudi arabia": "SAU",
    "senegal": "SEN",
    "serbia": "SRB",
    "sierra leone": "SLE",
    "singapore": "SGP",
    "slovakia": "SVK",
    "slovenia": "SVN",
    "somalia": "SOM",
    "south africa": "ZAF",
    "south korea": "KOR",
    "south sudan": "SSD",
    "spain": "ESP",
    "sri lanka": "LKA",
    "sudan": "SDN",
    "suriname": "SUR",
    "sweden": "SWE",
    "switzerland": "CHE",
    "syria": "SYR",
    "taiwan": "TWN",
    "tajikistan": "TJK",
    "tanzania": "TZA",
    "thailand": "THA",
    "togo": "TGO",
    "trinidad and tobago": "TTO",
    "tunisia": "TUN",
    "turkey": "TUR",
    "turkmenistan": "TKM",
    "uganda": "UGA",
    "ukraine": "UKR",
    "united arab emirates": "ARE",
    "united kingdom": "GBR",
    "united states": "USA",
    "uruguay": "URY",
    "uzbekistan": "UZB",
    "venezuela": "VEN",
    "vietnam": "VNM",
    "yemen": "YEM",
    "zambia": "ZMB",
    "zimbabwe": "ZWE",
}

WAR_PERIODS = {
    "Personalizado": None,

    "Guerra da Coreia": (1950, 1953),
    "Guerra do Vietnã": (1955, 1975),
    "Guerra dos Seis Dias": (1967, 1967),
    "Guerra de Yom Kippur": (1973, 1973),
    "Guerra do Afeganistão (URSS)": (1979, 1989),
    "Guerra Irã-Iraque": (1980, 1988),
    "Guerra do Golfo": (1990, 1991),
    "Guerra da Bósnia": (1992, 1995),
    "Guerra do Kosovo": (1998, 1999),
    "Guerra do Afeganistão": (2001, 2021),
    "Guerra do Iraque": (2003, 2011),
    "Guerra da Líbia": (2011, 2011),
    "Guerra Civil Síria": (2011, 2025),
    "Guerra do Iêmen": (2014, 2025),
    "Guerra Rússia-Ucrânia": (2014, 2025),
    "Guerra Israel-Hamas": (2023, 2025),
}