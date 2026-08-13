import streamlit as st
import pandas as pd
import yfinance as yf
import math
import requests
from io import StringIO
from datetime import date, timedelta

st.set_page_config(
    page_title="Aktien-Screener",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Aktien-Screener")
st.caption(
    "EURO STOXX 50 • TecDAX • Dow Jones • Nasdaq-100 | "
    "Qualität • Bewertung • Momentum • Risiko"
)

# ============================================================
# AKTIENUNIVERSUM
# ============================================================

DOW = {
    "3M": "MMM",
    "American Express": "AXP",
    "Amgen": "AMGN",
    "Amazon": "AMZN",
    "Apple": "AAPL",
    "Boeing": "BA",
    "Caterpillar": "CAT",
    "Chevron": "CVX",
    "Cisco": "CSCO",
    "Coca-Cola": "KO",
    "Disney": "DIS",
    "Goldman Sachs": "GS",
    "Home Depot": "HD",
    "Honeywell": "HON",
    "IBM": "IBM",
    "Johnson & Johnson": "JNJ",
    "JPMorgan Chase": "JPM",
    "McDonald's": "MCD",
    "Merck": "MRK",
    "Microsoft": "MSFT",
    "Nike": "NKE",
    "Nvidia": "NVDA",
    "Procter & Gamble": "PG",
    "Salesforce": "CRM",
    "Sherwin-Williams": "SHW",
    "Travelers": "TRV",
    "UnitedHealth": "UNH",
    "Verizon": "VZ",
    "Visa": "V",
    "Walmart": "WMT",
}

NASDAQ100 = {
    "Adobe": "ADBE",
    "Advanced Micro Devices": "AMD",
    "Airbnb": "ABNB",
    "Alphabet A": "GOOGL",
    "Alphabet C": "GOOG",
    "Amazon": "AMZN",
    "American Electric Power": "AEP",
    "Amgen": "AMGN",
    "Analog Devices": "ADI",
    "Apple": "AAPL",
    "Applied Materials": "AMAT",
    "Arm Holdings": "ARM",
    "ASML": "ASML",
    "Atlassian": "TEAM",
    "Autodesk": "ADSK",
    "Automatic Data Processing": "ADP",
    "Axon Enterprise": "AXON",
    "Baker Hughes": "BKR",
    "Booking Holdings": "BKNG",
    "Broadcom": "AVGO",
    "Cadence Design Systems": "CDNS",
    "Charter Communications": "CHTR",
    "Cintas": "CTAS",
    "Cisco": "CSCO",
    "Coca-Cola Europacific": "CCEP",
    "Cognizant": "CTSH",
    "Comcast": "CMCSA",
    "Constellation Energy": "CEG",
    "Copart": "CPRT",
    "Costco": "COST",
    "CrowdStrike": "CRWD",
    "CSX": "CSX",
    "Datadog": "DDOG",
    "DexCom": "DXCM",
    "Diamondback Energy": "FANG",
    "DoorDash": "DASH",
    "Electronic Arts": "EA",
    "Exelon": "EXC",
    "Fastenal": "FAST",
    "Fortinet": "FTNT",
    "GE HealthCare": "GEHC",
    "Gilead Sciences": "GILD",
    "Honeywell": "HON",
    "IDEXX Laboratories": "IDXX",
    "Intel": "INTC",
    "Intuit": "INTU",
    "Intuitive Surgical": "ISRG",
    "Keurig Dr Pepper": "KDP",
    "KLA": "KLAC",
    "Kraft Heinz": "KHC",
    "Lam Research": "LRCX",
    "Linde": "LIN",
    "Marriott": "MAR",
    "Marvell Technology": "MRVL",
    "MercadoLibre": "MELI",
    "Meta Platforms": "META",
    "Microchip Technology": "MCHP",
    "Micron Technology": "MU",
    "Microsoft": "MSFT",
    "Mondelez": "MDLZ",
    "Monster Beverage": "MNST",
    "Netflix": "NFLX",
    "Nvidia": "NVDA",
    "NXP Semiconductors": "NXPI",
    "Old Dominion Freight Line": "ODFL",
    "O'Reilly Automotive": "ORLY",
    "Palantir": "PLTR",
    "Palo Alto Networks": "PANW",
    "Paychex": "PAYX",
    "PayPal": "PYPL",
    "PDD Holdings": "PDD",
    "PepsiCo": "PEP",
    "Qualcomm": "QCOM",
    "Regeneron": "REGN",
    "Roper Technologies": "ROP",
    "Ross Stores": "ROST",
    "Starbucks": "SBUX",
    "Synopsys": "SNPS",
    "T-Mobile US": "TMUS",
    "Take-Two Interactive": "TTWO",
    "Tesla": "TSLA",
    "Texas Instruments": "TXN",
    "Verisk Analytics": "VRSK",
    "Vertex Pharmaceuticals": "VRTX",
    "Warner Bros. Discovery": "WBD",
    "Workday": "WDAY",
    "Xcel Energy": "XEL",
    "Zscaler": "ZS",
}

EUROSTOXX50 = {
    'Adidas': 'ADS.DE',
    'Adyen': 'ADYEN.AS',
    'Ahold Delhaize': 'AD.AS',
    'Air Liquide': 'AI.PA',
    'Airbus': 'AIR.PA',
    'Allianz': 'ALV.DE',
    'Anheuser-Busch InBev': 'ABI.BR',
    'argenx': 'ARGX.BR',
    'ASML': 'ASML.AS',
    'AXA': 'CS.PA',
    'Banco Santander': 'SAN.MC',
    'BASF': 'BAS.DE',
    'Bayer': 'BAYN.DE',
    'BBVA': 'BBVA.MC',
    'BMW': 'BMW.DE',
    'BNP Paribas': 'BNP.PA',
    'Danone': 'BN.PA',
    'Deutsche Bank': 'DBK.DE',
    'Deutsche Börse': 'DB1.DE',
    'DHL Group': 'DHL.DE',
    'Deutsche Telekom': 'DTE.DE',
    'Enel': 'ENEL.MI',
    'Eni': 'ENI.MI',
    'EssilorLuxottica': 'EL.PA',
    'Ferrari': 'RACE.MI',
    'Hermès': 'RMS.PA',
    'Iberdrola': 'IBE.MC',
    'Inditex': 'ITX.MC',
    'Infineon': 'IFX.DE',
    'ING': 'INGA.AS',
    'Intesa Sanpaolo': 'ISP.MI',
    "L'Oréal": 'OR.PA',
    'LVMH': 'MC.PA',
    'Mercedes-Benz': 'MBG.DE',
    'Münchener Rück': 'MUV2.DE',
    'Nordea': 'NDA-FI.HE',
    'Prosus': 'PRX.AS',
    'Rheinmetall': 'RHM.DE',
    'Safran': 'SAF.PA',
    'Saint-Gobain': 'SGO.PA',
    'Sanofi': 'SAN.PA',
    'SAP': 'SAP.DE',
    'Schneider Electric': 'SU.PA',
    'Siemens': 'SIE.DE',
    'Siemens Energy': 'ENR.DE',
    'TotalEnergies': 'TTE.PA',
    'UniCredit': 'UCG.MI',
    'Vinci': 'DG.PA',
    'Volkswagen Vz.': 'VOW3.DE',
    'Wolters Kluwer': 'WKL.AS',
}

TECDAX = {
    "Aixtron": "AIXA.DE",
    "Bechtle": "BC8.DE",
    "Carl Zeiss Meditec": "AFX.DE",
    "CompuGroup Medical": "COP.DE",
    "Deutsche Telekom": "DTE.DE",
    "Drägerwerk Vz.": "DRW3.DE",
    "Eckert & Ziegler": "EUZ.DE",
    "Elmos Semiconductor": "ELG.DE",
    "Evotec": "EVT.DE",
    "Freenet": "FNTN.DE",
    "Hensoldt": "HAG.DE",
    "Infineon": "IFX.DE",
    "Jenoptik": "JEN.DE",
    "Kontron": "KTN.DE",
    "Nemetschek": "NEM.DE",
    "Nordex": "NDX1.DE",
    "PNE": "PNE3.DE",
    "Qiagen": "QIA.DE",
    "SAP": "SAP.DE",
    "Sartorius Vz.": "SRT3.DE",
    "Siltronic": "WAF.DE",
    "Siemens Healthineers": "SHL.DE",
    "TeamViewer": "TMV.DE",
    "United Internet": "UTDI.DE",
    "Verbio": "VBK.DE",
    "1&1": "1U1.DE",
}

INDEX_DATA = {
    "EURO STOXX 50": EUROSTOXX50,
    "TecDAX": TECDAX,
    "Dow Jones": DOW,
    "Nasdaq-100": NASDAQ100,
}

# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def safe_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def pct(value):
    value = safe_float(value)
    if value is None:
        return None
    if abs(value) <= 2:
        value *= 100
    return value


def clamp(value):
    return max(0.0, min(100.0, value))


def bounded(value, low=None, high=None):
    if value is None:
        return None
    if low is not None:
        value = max(low, value)
    if high is not None:
        value = min(high, value)
    return value


# ============================================================
# DATEN – REDUNDANTE QUELLEN
# ============================================================

def get_secret(name):
    try:
        return st.secrets.get(name, "")
    except Exception:
        return ""


EODHD_API_TOKEN = get_secret("EODHD_API_TOKEN")


def yahoo_to_eodhd(symbol):
    suffix_map = {
        ".DE": ".XETRA",
        ".PA": ".PA",
        ".AS": ".AS",
        ".BR": ".BR",
        ".MI": ".MI",
        ".MC": ".MC",
        ".HE": ".HE",
    }
    for yahoo_suffix, eod_suffix in suffix_map.items():
        if symbol.endswith(yahoo_suffix):
            return symbol[:-len(yahoo_suffix)] + eod_suffix

    # US-Aktien ohne Suffix
    if "." not in symbol:
        return symbol + ".US"

    return symbol


def yahoo_to_stooq(symbol):
    # Stooq nutzt überwiegend Länder-Suffixe.
    suffix_map = {
        ".DE": ".de",
        ".PA": ".fr",
        ".AS": ".nl",
        ".BR": ".be",
        ".MI": ".it",
        ".MC": ".es",
        ".HE": ".fi",
    }
    for yahoo_suffix, stooq_suffix in suffix_map.items():
        if symbol.endswith(yahoo_suffix):
            return symbol[:-len(yahoo_suffix)].lower() + stooq_suffix

    if "." not in symbol:
        return symbol.lower() + ".us"

    return symbol.lower()


@st.cache_data(ttl=3600, show_spinner=False)
def get_yahoo_history(symbol):
    try:
        hist = yf.Ticker(symbol).history(
            period="1y",
            auto_adjust=True
        )
        if hist is None or hist.empty:
            return None
        return hist
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_eodhd_history(symbol):
    if not EODHD_API_TOKEN:
        return None

    try:
        eod_symbol = yahoo_to_eodhd(symbol)
        end_date = date.today()
        start_date = end_date - timedelta(days=370)

        response = requests.get(
            f"https://eodhd.com/api/eod/{eod_symbol}",
            params={
                "api_token": EODHD_API_TOKEN,
                "fmt": "json",
                "period": "d",
                "from": start_date.isoformat(),
                "to": end_date.isoformat(),
            },
            timeout=12,
        )
        if response.status_code != 200:
            return None

        rows = response.json()
        if not isinstance(rows, list) or not rows:
            return None

        df = pd.DataFrame(rows)
        price_col = (
            "adjusted_close"
            if "adjusted_close" in df.columns
            else "close"
        )
        if price_col not in df.columns:
            return None

        df["Date"] = pd.to_datetime(df["date"])
        df["Close"] = pd.to_numeric(
            df[price_col],
            errors="coerce"
        )
        df = (
            df[["Date", "Close"]]
            .dropna()
            .set_index("Date")
            .sort_index()
        )
        return df if not df.empty else None
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_stooq_history(symbol):
    try:
        stooq_symbol = yahoo_to_stooq(symbol)
        end_date = date.today()
        start_date = end_date - timedelta(days=370)

        response = requests.get(
            "https://stooq.com/q/d/l/",
            params={
                "s": stooq_symbol,
                "d1": start_date.strftime("%Y%m%d"),
                "d2": end_date.strftime("%Y%m%d"),
                "i": "d",
            },
            timeout=12,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        if response.status_code != 200:
            return None

        body = response.text.strip()
        if not body or "No data" in body:
            return None

        df = pd.read_csv(StringIO(body))
        if "Date" not in df.columns or "Close" not in df.columns:
            return None

        df["Date"] = pd.to_datetime(df["Date"])
        df["Close"] = pd.to_numeric(
            df["Close"],
            errors="coerce"
        )
        df = (
            df[["Date", "Close"]]
            .dropna()
            .set_index("Date")
            .sort_index()
        )
        return df if not df.empty else None
    except Exception:
        return None


def get_redundant_history(symbol):
    """
    Priorität:
    1. Yahoo Finance
    2. EODHD (wenn API-Key vorhanden)
    3. Stooq

    Sekundärquellen werden nur aufgerufen, wenn die vorherige Quelle
    keine verwertbare Historie liefert. Dadurch wird das EODHD-
    Freikontingent geschont.
    """
    hist = get_yahoo_history(symbol)
    if hist is not None and not hist.empty:
        return hist, "Yahoo Finance"

    hist = get_eodhd_history(symbol)
    if hist is not None and not hist.empty:
        return hist, "EODHD"

    hist = get_stooq_history(symbol)
    if hist is not None and not hist.empty:
        return hist, "Stooq"

    return None, "keine"


@st.cache_data(ttl=21600, show_spinner=False)
def get_yahoo_fundamentals(symbol):
    try:
        ticker = yf.Ticker(symbol)
        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        if not info:
            return {}

        return {
            "ROE %": pct(info.get("returnOnEquity")),
            "Operative Marge %": pct(info.get("operatingMargins")),
            "Debt/Equity": safe_float(info.get("debtToEquity")),
            "KGV": safe_float(info.get("trailingPE")),
            "Forward-KGV": safe_float(info.get("forwardPE")),
            "Gewinnwachstum %": pct(info.get("earningsGrowth")),
            "Umsatzwachstum %": pct(info.get("revenueGrowth")),
            "Dividendenrendite %": pct(info.get("dividendYield")),
            "KBV": safe_float(info.get("priceToBook")),
            "Sektor": str(info.get("sector") or ""),
            "Industrie": str(info.get("industry") or ""),
        }
    except Exception:
        return {}


@st.cache_data(ttl=21600, show_spinner=False)
def get_eodhd_fundamentals(symbol):
    """
    Ergänzende Fundamentaldatenquelle.
    Im kostenlosen EODHD-Paket ist der Fundamentals-Endpunkt meist
    nicht freigeschaltet; dann liefert die Funktion einfach {}.
    Sobald ein passender Tarif aktiv ist, werden fehlende Yahoo-Werte
    automatisch ergänzt.
    """
    if not EODHD_API_TOKEN:
        return {}

    try:
        eod_symbol = yahoo_to_eodhd(symbol)
        response = requests.get(
            f"https://eodhd.com/api/fundamentals/{eod_symbol}",
            params={
                "api_token": EODHD_API_TOKEN,
                "fmt": "json",
            },
            timeout=15,
        )

        if response.status_code != 200:
            return {}

        raw = response.json()
        if not isinstance(raw, dict):
            return {}

        general = raw.get("General") or {}
        highlights = raw.get("Highlights") or {}
        valuation = raw.get("Valuation") or {}

        return {
            "ROE %": pct(highlights.get("ReturnOnEquityTTM")),
            "Operative Marge %": pct(
                highlights.get("OperatingMarginTTM")
                or highlights.get("ProfitMargin")
            ),
            "KGV": safe_float(
                valuation.get("TrailingPE")
                or highlights.get("PERatio")
            ),
            "Forward-KGV": safe_float(
                valuation.get("ForwardPE")
            ),
            "Gewinnwachstum %": pct(
                highlights.get("QuarterlyEarningsGrowthYOY")
            ),
            "Umsatzwachstum %": pct(
                highlights.get("QuarterlyRevenueGrowthYOY")
            ),
            "Dividendenrendite %": pct(
                highlights.get("DividendYield")
            ),
            "KBV": safe_float(
                valuation.get("PriceBookMRQ")
                or valuation.get("PriceBook")
            ),
            "Sektor": str(general.get("Sector") or ""),
            "Industrie": str(general.get("Industry") or ""),
        }
    except Exception:
        return {}


def merge_fundamentals(primary, secondary):
    merged = dict(primary or {})
    used_secondary = False

    for key, value in (secondary or {}).items():
        current = merged.get(key)
        missing = (
            current is None
            or current == ""
            or (
                isinstance(current, float)
                and math.isnan(current)
            )
        )
        if missing and value not in (None, ""):
            merged[key] = value
            used_secondary = True

    if primary and used_secondary:
        source = "Yahoo + EODHD"
    elif primary:
        source = "Yahoo Finance"
    elif secondary:
        source = "EODHD"
    else:
        source = "keine"

    return merged, source


@st.cache_data(ttl=3600, show_spinner=False)
def get_stock_data(symbol):
    try:
        hist, price_source = get_redundant_history(symbol)

        if hist is None or hist.empty:
            return None

        close = pd.to_numeric(
            hist["Close"],
            errors="coerce"
        ).dropna()

        if len(close) < 60:
            return None

        current = float(close.iloc[-1])

        p6m = (
            (current / float(close.iloc[-126]) - 1) * 100
            if len(close) >= 126 else None
        )

        p12m = (
            (current / float(close.iloc[0]) - 1) * 100
            if len(close) >= 240 else None
        )

        sma200 = (
            float(close.tail(200).mean())
            if len(close) >= 200 else None
        )

        distance_200 = (
            (current / sma200 - 1) * 100
            if sma200 else None
        )

        high52 = float(close.max())

        distance_high = (
            (current / high52 - 1) * 100
            if high52 else None
        )

        daily_returns = close.pct_change().dropna()

        volatility = (
            float(daily_returns.std())
            * math.sqrt(252)
            * 100
        )

        running_max = close.cummax()
        drawdown = (close / running_max - 1) * 100
        max_drawdown = float(drawdown.min())

        yahoo_f = get_yahoo_fundamentals(symbol)
        eod_f = get_eodhd_fundamentals(symbol)
        fundamentals, fundamental_source = merge_fundamentals(
            yahoo_f,
            eod_f
        )

        return {
            "Kurs": current,
            "6M %": p6m,
            "12M %": p12m,
            "200T %": distance_200,
            "52W-Hoch %": distance_high,
            "Volatilität %": volatility,
            "Max Drawdown %": max_drawdown,
            "ROE %": fundamentals.get("ROE %"),
            "Operative Marge %": fundamentals.get("Operative Marge %"),
            "Debt/Equity": fundamentals.get("Debt/Equity"),
            "KGV": fundamentals.get("KGV"),
            "Forward-KGV": fundamentals.get("Forward-KGV"),
            "Gewinnwachstum %": fundamentals.get("Gewinnwachstum %"),
            "Umsatzwachstum %": fundamentals.get("Umsatzwachstum %"),
            "Dividendenrendite %": fundamentals.get("Dividendenrendite %"),
            "KBV": fundamentals.get("KBV"),
            "Sektor": fundamentals.get("Sektor", ""),
            "Industrie": fundamentals.get("Industrie", ""),
            "Kursquelle": price_source,
            "Fundamentalquelle": fundamental_source,
        }

    except Exception:
        return None


# ============================================================
# SEKTORERKENNUNG
# ============================================================

def sector_type(d):
    sector = (d.get("Sektor") or "").lower()
    industry = (d.get("Industrie") or "").lower()

    if (
        "financial" in sector
        or "bank" in industry
        or "credit services" in industry
    ):
        if "insurance" in industry:
            return "Versicherung"
        return "Bank/Finanz"

    if "insurance" in industry:
        return "Versicherung"

    return "Standard"


# ============================================================
# QUALITÄT
# ============================================================

def quality_score(d):
    typ = sector_type(d)

    roe = bounded(d.get("ROE %"), -100, 100)
    margin = bounded(d.get("Operative Marge %"), -100, 100)
    growth = bounded(d.get("Gewinnwachstum %"), -100, 100)
    revenue_growth = bounded(d.get("Umsatzwachstum %"), -100, 100)
    debt = bounded(d.get("Debt/Equity"), 0, 1000)

    points = 0
    maximum = 0

    if typ in ["Bank/Finanz", "Versicherung"]:
        if roe is not None:
            maximum += 45
            if roe >= 18:
                points += 45
            elif roe >= 14:
                points += 38
            elif roe >= 10:
                points += 30
            elif roe >= 7:
                points += 18
            elif roe >= 4:
                points += 8

        if growth is not None:
            maximum += 30
            if growth >= 15:
                points += 30
            elif growth >= 8:
                points += 24
            elif growth >= 3:
                points += 16
            elif growth >= 0:
                points += 8

        if revenue_growth is not None:
            maximum += 25
            if revenue_growth >= 10:
                points += 25
            elif revenue_growth >= 5:
                points += 19
            elif revenue_growth >= 0:
                points += 11

    else:
        if roe is not None:
            maximum += 30
            if roe >= 25:
                points += 30
            elif roe >= 18:
                points += 26
            elif roe >= 12:
                points += 20
            elif roe >= 7:
                points += 12

        if margin is not None:
            maximum += 30
            if margin >= 25:
                points += 30
            elif margin >= 15:
                points += 25
            elif margin >= 8:
                points += 18
            elif margin >= 4:
                points += 10

        if growth is not None:
            maximum += 20
            if growth >= 20:
                points += 20
            elif growth >= 10:
                points += 16
            elif growth >= 5:
                points += 11
            elif growth >= 0:
                points += 5

        if debt is not None:
            maximum += 20
            if debt <= 40:
                points += 20
            elif debt <= 80:
                points += 16
            elif debt <= 120:
                points += 11
            elif debt <= 200:
                points += 6

    if maximum == 0:
        return None

    return clamp(points / maximum * 100)


# ============================================================
# BEWERTUNG
# ============================================================

def valuation_score(d):
    typ = sector_type(d)

    pe = bounded(d.get("KGV"), 0, 150)
    forward_pe = bounded(d.get("Forward-KGV"), 0, 150)
    dividend = bounded(d.get("Dividendenrendite %"), 0, 20)
    pb = bounded(d.get("KBV"), 0, 20)

    points = 0
    maximum = 0

    if pe is not None and pe > 0:
        maximum += 40

        if pe <= 8:
            points += 40
        elif pe <= 12:
            points += 34
        elif pe <= 16:
            points += 28
        elif pe <= 22:
            points += 20
        elif pe <= 30:
            points += 12
        elif pe <= 40:
            points += 6

    if forward_pe is not None and forward_pe > 0:
        maximum += 30

        if forward_pe <= 8:
            points += 30
        elif forward_pe <= 12:
            points += 26
        elif forward_pe <= 16:
            points += 21
        elif forward_pe <= 22:
            points += 15
        elif forward_pe <= 30:
            points += 8
        elif forward_pe <= 40:
            points += 4

    if dividend is not None:
        maximum += 15

        if dividend >= 5:
            points += 15
        elif dividend >= 3:
            points += 12
        elif dividend >= 2:
            points += 8
        elif dividend >= 1:
            points += 4

    if typ in ["Bank/Finanz", "Versicherung"] and pb is not None:
        maximum += 15

        if pb <= 0.8:
            points += 15
        elif pb <= 1.2:
            points += 12
        elif pb <= 1.8:
            points += 8
        elif pb <= 2.5:
            points += 4

    if maximum == 0:
        return None

    return clamp(points / maximum * 100)


# ============================================================
# MOMENTUM
# ============================================================

def momentum_score(d):
    points = 0

    p6 = d.get("6M %")
    p12 = d.get("12M %")
    ma = d.get("200T %")
    high = d.get("52W-Hoch %")

    if p6 is not None:
        if p6 >= 20:
            points += 30
        elif p6 >= 10:
            points += 25
        elif p6 >= 5:
            points += 18
        elif p6 >= 0:
            points += 10

    if p12 is not None:
        if p12 >= 30:
            points += 35
        elif p12 >= 20:
            points += 30
        elif p12 >= 10:
            points += 22
        elif p12 >= 0:
            points += 12

    if ma is not None:
        if ma >= 15:
            points += 20
        elif ma >= 5:
            points += 17
        elif ma >= 0:
            points += 12
        elif ma >= -5:
            points += 5

    if high is not None:
        if high >= -5:
            points += 15
        elif high >= -10:
            points += 12
        elif high >= -20:
            points += 7
        elif high >= -30:
            points += 3

    return clamp(points)


# ============================================================
# RISIKO
# ============================================================

def risk_score(d):
    score = 100

    vol = d.get("Volatilität %")
    dd = d.get("Max Drawdown %")

    if vol is not None:
        if vol > 60:
            score -= 45
        elif vol > 45:
            score -= 35
        elif vol > 35:
            score -= 25
        elif vol > 25:
            score -= 15
        elif vol > 20:
            score -= 7

    if dd is not None:
        if dd < -60:
            score -= 45
        elif dd < -45:
            score -= 35
        elif dd < -35:
            score -= 25
        elif dd < -25:
            score -= 15
        elif dd < -15:
            score -= 7

    return clamp(score)


# ============================================================
# LEVERMANN-TEILSCORE
# ============================================================

def levermann_score(d):
    score = 0
    available = 0

    roe = d.get("ROE %")
    margin = d.get("Operative Marge %")
    pe = d.get("KGV")
    forward_pe = d.get("Forward-KGV")
    p6 = d.get("6M %")
    p12 = d.get("12M %")

    typ = sector_type(d)

    if roe is not None:
        available += 1
        if roe > 20:
            score += 1
        elif roe < 10:
            score -= 1

    if typ == "Standard" and margin is not None:
        available += 1
        if margin > 12:
            score += 1
        elif margin < 6:
            score -= 1

    if pe is not None and pe > 0:
        available += 1
        if pe < 12:
            score += 1
        elif pe > 16:
            score -= 1

    if forward_pe is not None and forward_pe > 0:
        available += 1
        if forward_pe < 12:
            score += 1
        elif forward_pe > 16:
            score -= 1

    if p6 is not None:
        available += 1
        if p6 > 5:
            score += 1
        elif p6 < -5:
            score -= 1

    if p12 is not None:
        available += 1
        if p12 > 5:
            score += 1
        elif p12 < -5:
            score -= 1

    return score, available


# ============================================================
# GESAMTSCORE
# ============================================================

def total_score(quality, valuation, momentum, risk):
    components = [
        (quality, 0.30),
        (valuation, 0.25),
        (momentum, 0.25),
        (risk, 0.20),
    ]

    available = [
        (score, weight)
        for score, weight in components
        if score is not None
    ]

    if not available:
        return None, 0

    weight_sum = sum(weight for _, weight in available)

    total = sum(
        score * weight
        for score, weight in available
    ) / weight_sum

    return total, weight_sum * 100


# ============================================================
# OBERFLÄCHE
# ============================================================

index_name = st.selectbox(
    "Index auswählen",
    list(INDEX_DATA.keys())
)

stocks = INDEX_DATA[index_name]

st.info(f"**{index_name}: {len(stocks)} Aktien**")

st.caption(
    "Datenredundanz: Kursreihen werden zuerst über Yahoo Finance geladen; "
    "bei Ausfall folgt EODHD und danach Stooq. Fundamentaldaten kommen "
    "primär von Yahoo Finance und werden – sofern der EODHD-Tarif den "
    "Fundamentals-Endpunkt erlaubt – automatisch durch EODHD ergänzt."
)

if index_name == "EURO STOXX 50":
    if len(stocks) != 50:
        st.warning(
            f"⚠️ Das EURO-STOXX-50-Universum enthält {len(stocks)} statt 50 Aktien."
        )
    else:
        st.success("✅ EURO-STOXX-50-Universum vollständig: 50 Aktien.")

min_coverage = st.slider(
    "Mindest-Datenabdeckung",
    min_value=0,
    max_value=100,
    value=40,
    step=10
)

st.caption(
    "Empfehlung: 40 %. Wenn Fundamentaldaten einer Quelle vorübergehend fehlen, "
    "können Momentum (25 %) und Risiko (20 %) zusammen bereits 45 % Abdeckung liefern. "
    "Bei 50 % würden solche Aktien vollständig ausgeblendet."
)

if st.button(
    f"🔎 {index_name} analysieren",
    type="primary"
):
    progress = st.progress(0)
    status = st.empty()

    results = []
    omitted = []
    total = len(stocks)

    for i, (name, symbol) in enumerate(stocks.items()):
        status.write(
            f"Analysiere {i + 1}/{total}: **{name}**"
        )

        data = get_stock_data(symbol)

        if data is not None:
            quality = quality_score(data)
            valuation = valuation_score(data)
            momentum = momentum_score(data)
            risk = risk_score(data)

            levermann, levermann_n = levermann_score(data)

            overall, coverage = total_score(
                quality,
                valuation,
                momentum,
                risk
            )

            if (
                overall is not None
                and coverage >= min_coverage
            ):
                if overall >= 75:
                    ampel = "🟢"
                elif overall >= 55:
                    ampel = "🟡"
                else:
                    ampel = "🔴"

                results.append({
                    "Ampel": ampel,
                    "Aktie": name,
                    "Symbol": symbol,
                    "Sektor": sector_type(data),
                    "Gesamtscore": overall,
                    "Qualität": quality,
                    "Bewertung": valuation,
                    "Momentum": momentum,
                    "Risiko": risk,
                    "Levermann": levermann,
                    "Lev.-Daten": f"{levermann_n}/13",
                    "Daten %": coverage,
                    "KGV": data.get("KGV"),
                    "Forward-KGV": data.get("Forward-KGV"),
                    "KBV": data.get("KBV"),
                    "ROE %": data.get("ROE %"),
                    "Marge %": data.get("Operative Marge %"),
                    "Gewinnwachstum %": data.get("Gewinnwachstum %"),
                    "6M %": data.get("6M %"),
                    "12M %": data.get("12M %"),
                    "Volatilität %": data.get("Volatilität %"),
                    "Drawdown %": data.get("Max Drawdown %"),
                    "Kursquelle": data.get("Kursquelle"),
                    "Fundamentalquelle": data.get("Fundamentalquelle"),
                })
            else:
                omitted.append({
                    "Aktie": name,
                    "Symbol": symbol,
                    "Grund": (
                        f"Datenabdeckung {coverage:.0f} % "
                        f"< Mindestwert {min_coverage} %"
                        if overall is not None
                        else "Gesamtscore nicht berechenbar"
                    ),
                    "Kursquelle": data.get("Kursquelle"),
                    "Fundamentalquelle": data.get("Fundamentalquelle"),
                })
        else:
            omitted.append({
                "Aktie": name,
                "Symbol": symbol,
                "Grund": "Keine ausreichende Kursreihe aus Yahoo, EODHD oder Stooq",
                "Kursquelle": "keine",
                "Fundamentalquelle": "keine",
            })

        progress.progress((i + 1) / total)

    progress.empty()
    status.empty()

    if not results:
        st.error(
            "Keine Aktien mit der gewählten Mindest-Datenabdeckung gefunden. "
            "Bitte zunächst 40 % wählen; fehlende Fundamentaldaten werden unten separat angezeigt."
        )
    else:
        df = pd.DataFrame(results)

        df = df.sort_values(
            "Gesamtscore",
            ascending=False
        ).reset_index(drop=True)

        df.insert(
            0,
            "Rang",
            range(1, len(df) + 1)
        )

        numeric_columns = [
            "Gesamtscore",
            "Qualität",
            "Bewertung",
            "Momentum",
            "Risiko",
            "Daten %",
            "KGV",
            "Forward-KGV",
            "KBV",
            "ROE %",
            "Marge %",
            "Gewinnwachstum %",
            "6M %",
            "12M %",
            "Volatilität %",
            "Drawdown %",
        ]

        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).round(1)

        st.subheader(
            f"🏆 Ranking – {index_name}"
        )

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        st.subheader("🥇 Top 10")

        st.dataframe(
            df.head(10),
            hide_index=True,
            use_container_width=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ Gesamtes Ranking als CSV",
            csv,
            file_name=(
                index_name
                .replace(" ", "_")
                .replace("-", "_")
                + "_Screener.csv"
            ),
            mime="text/csv"
        )

    if omitted:
        with st.expander(
            f"⚠️ Nicht ausgewertete Aktien ({len(omitted)})",
            expanded=False
        ):
            st.write(
                "Diese Aktien werden nicht mehr stillschweigend entfernt. "
                "Hier siehst du, ob Kursdaten fehlen oder die eingestellte "
                "Mindest-Datenabdeckung nicht erreicht wurde."
            )
            st.dataframe(
                pd.DataFrame(omitted),
                hide_index=True,
                use_container_width=True
            )

st.divider()

st.subheader("🧮 Zusammensetzung des Gesamtscores")

st.markdown(
    """
Der **Gesamtscore** besteht aus vier Teilwerten:

- **30 % Qualität**
- **25 % Bewertung**
- **25 % Momentum**
- **20 % Risiko**

Fehlen einzelne Teilwerte, werden nur die verfügbaren Teilwerte verwendet
und auf 100 % der tatsächlich verfügbaren Gewichtung normiert. Die Spalte
**Daten %** zeigt deshalb, wie viel der vorgesehenen Gesamtgewichtung
tatsächlich mit Daten belegt ist.
"""
)

with st.expander("⭐ Qualität – 30 % des Gesamtscores"):
    st.markdown(
        """
**Standardunternehmen**

- **ROE / Eigenkapitalrendite: 30 % des Qualitätsscores**
- **Operative Marge: 30 %**
- **Gewinnwachstum: 20 %**
- **Debt/Equity: 20 %**

**Banken und Versicherungen**

- **ROE / Eigenkapitalrendite: 45 %**
- **Gewinnwachstum: 30 %**
- **Umsatzwachstum: 25 %**

Die jeweils verfügbaren Kriterien werden innerhalb des Qualitätsscores
auf 100 Punkte normiert.
"""
    )

with st.expander("💶 Bewertung – 25 % des Gesamtscores"):
    st.markdown(
        """
- **KGV: bis zu 40 Punkte**
- **Forward-KGV: bis zu 30 Punkte**
- **Dividendenrendite: bis zu 15 Punkte**
- **KBV: bis zu 15 Punkte bei Banken und Versicherungen**

Je niedriger KGV bzw. Forward-KGV, desto höher die Punktzahl.
Eine höhere Dividendenrendite verbessert den Bewertungsscore.
Bei Banken und Versicherungen wird zusätzlich ein niedriges KBV
positiv berücksichtigt. Verfügbare Kriterien werden auf 100 Punkte
normiert.
"""
    )

with st.expander("🚀 Momentum – 25 % des Gesamtscores"):
    st.markdown(
        """
Der Momentumswert hat maximal 100 Punkte:

- **6-Monats-Performance: 30 Punkte**
- **12-Monats-Performance: 35 Punkte**
- **Abstand zum 200-Tage-Durchschnitt: 20 Punkte**
- **Nähe zum 52-Wochen-Hoch: 15 Punkte**

Damit werden sowohl mittelfristige Kursstärke als auch der längerfristige
Trend und die Nähe zu neuen Hochs berücksichtigt.
"""
    )

with st.expander("🛡️ Risiko – 20 % des Gesamtscores"):
    st.markdown(
        """
Der Risikoscore startet bei **100 Punkten**. Anschließend gibt es
Abzüge für:

- **annualisierte Volatilität:** bis zu **−45 Punkte**
- **maximalen Drawdown der letzten 12 Monate:** bis zu **−45 Punkte**

Je ruhiger die Kursentwicklung und je kleiner der zwischenzeitliche
Kursverlust, desto höher der Risikoscore. Ein hoher Risikoscore bedeutet
also **geringeres historisches Kursrisiko**.
"""
    )

with st.expander("🗄️ Datenquellen und Redundanz"):
    st.markdown(
        """
**Kursdaten**

1. Yahoo Finance
2. EODHD als Fallback
3. Stooq als weiterer Fallback

EODHD wird für Kursdaten nur dann abgefragt, wenn Yahoo keine brauchbare
Historie liefert. Das schont insbesondere das kostenlose EODHD-Kontingent.

**Fundamentaldaten**

1. Yahoo Finance als Primärquelle
2. EODHD als Ergänzung für fehlende Werte, sofern der verwendete
   EODHD-Tarif Fundamentals freigeschaltet hat

Die Ergebnistabelle zeigt mit **Kursquelle** und **Fundamentalquelle**,
welche Quelle tatsächlich verwendet wurde.
"""
    )

st.caption(
    "Banken und Versicherungen werden sektorspezifisch behandelt. "
    "Der Levermann-Wert ist ein Teilscore aus den verfügbaren Kriterien. "
    "Das Screening ist ein quantitatives Hilfsmittel und keine Anlageberatung."
)
