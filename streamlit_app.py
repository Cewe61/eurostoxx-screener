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
    'Adobe': 'ADBE',
    'Advanced Micro Devices': 'AMD',
    'Airbnb': 'ABNB',
    'Alnylam Pharmaceuticals': 'ALNY',
    'Alphabet A': 'GOOGL',
    'Alphabet C': 'GOOG',
    'Amazon': 'AMZN',
    'American Electric Power': 'AEP',
    'Amgen': 'AMGN',
    'Analog Devices': 'ADI',
    'Apple': 'AAPL',
    'Applied Materials': 'AMAT',
    'AppLovin': 'APP',
    'Arm Holdings': 'ARM',
    'ASML': 'ASML',
    'Astera Labs': 'ALAB',
    'Autodesk': 'ADSK',
    'Automatic Data Processing': 'ADP',
    'Axon Enterprise': 'AXON',
    'Baker Hughes': 'BKR',
    'Booking Holdings': 'BKNG',
    'Broadcom': 'AVGO',
    'Cadence Design Systems': 'CDNS',
    'Cintas': 'CTAS',
    'Cisco': 'CSCO',
    'Coca-Cola Europacific': 'CCEP',
    'Comcast': 'CMCSA',
    'Constellation Energy': 'CEG',
    'Copart': 'CPRT',
    'CoreWeave': 'CRWV',
    'Costco': 'COST',
    'CrowdStrike': 'CRWD',
    'CSX': 'CSX',
    'Datadog': 'DDOG',
    'DexCom': 'DXCM',
    'Diamondback Energy': 'FANG',
    'DoorDash': 'DASH',
    'Exelon': 'EXC',
    'Fastenal': 'FAST',
    'Ferrovial': 'FER',
    'Fortinet': 'FTNT',
    'GE HealthCare': 'GEHC',
    'Gilead Sciences': 'GILD',
    'Honeywell Aerospace': 'HONA',
    'Honeywell Technologies': 'HON',
    'IDEXX Laboratories': 'IDXX',
    'Intel': 'INTC',
    'Intuit': 'INTU',
    'Intuitive Surgical': 'ISRG',
    'Keurig Dr Pepper': 'KDP',
    'KLA': 'KLAC',
    'Kraft Heinz': 'KHC',
    'Lam Research': 'LRCX',
    'Linde': 'LIN',
    'Lumentum': 'LITE',
    'Marriott': 'MAR',
    'Marvell Technology': 'MRVL',
    'MercadoLibre': 'MELI',
    'Meta Platforms': 'META',
    'Microchip Technology': 'MCHP',
    'Micron Technology': 'MU',
    'Microsoft': 'MSFT',
    'MicroStrategy': 'MSTR',
    'Mondelez': 'MDLZ',
    'Monolithic Power Systems': 'MPWR',
    'Monster Beverage': 'MNST',
    'Nebius Group': 'NBIS',
    'Netflix': 'NFLX',
    'Nvidia': 'NVDA',
    'NXP Semiconductors': 'NXPI',
    "O'Reilly Automotive": 'ORLY',
    'Old Dominion Freight Line': 'ODFL',
    'PACCAR': 'PCAR',
    'Palantir': 'PLTR',
    'Palo Alto Networks': 'PANW',
    'Paychex': 'PAYX',
    'PayPal': 'PYPL',
    'PDD Holdings': 'PDD',
    'PepsiCo': 'PEP',
    'Qualcomm': 'QCOM',
    'Regeneron': 'REGN',
    'Rocket Lab': 'RKLB',
    'Roper Technologies': 'ROP',
    'Ross Stores': 'ROST',
    'Sandisk': 'SNDK',
    'Seagate Technology': 'STX',
    'Shopify': 'SHOP',
    'SpaceX': 'SPCX',
    'Starbucks': 'SBUX',
    'Synopsys': 'SNPS',
    'T-Mobile US': 'TMUS',
    'Take-Two Interactive': 'TTWO',
    'Teradyne': 'TER',
    'Tesla': 'TSLA',
    'Texas Instruments': 'TXN',
    'Thomson Reuters': 'TRI',
    'Vertex Pharmaceuticals': 'VRTX',
    'Walmart': 'WMT',
    'Warner Bros. Discovery': 'WBD',
    'Western Digital': 'WDC',
    'Workday': 'WDAY',
    'Xcel Energy': 'XEL',
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
    'Aixtron': 'AIXA.DE',
    'ATOSS Software': 'AOF.DE',
    'Bechtle': 'BC8.DE',
    'CANCOM': 'COK.DE',
    'Carl Zeiss Meditec': 'AFX.DE',
    'Drägerwerk Vz.': 'DRW3.DE',
    'Deutsche Telekom': 'DTE.DE',
    'Eckert & Ziegler': 'EUZ.DE',
    'Elmos Semiconductor': 'ELG.DE',
    'Evotec': 'EVT.DE',
    'Freenet': 'FNTN.DE',
    'Hensoldt': 'HAG.DE',
    'Infineon': 'IFX.DE',
    'IONOS': 'IOS.DE',
    'Jenoptik': 'JEN.DE',
    'Kontron': 'KTN.DE',
    'Nemetschek': 'NEM.DE',
    'Nordex': 'NDX1.DE',
    'Ottobock': 'OBCK.DE',
    'PVA TePla': 'TPE.DE',
    'Qiagen': 'QIA.DE',
    'SAP': 'SAP.DE',
    'Sartorius Vz.': 'SRT3.DE',
    'Siemens Healthineers': 'SHL.DE',
    'Siltronic': 'WAF.DE',
    'SMA Solar': 'S92.DE',
    'SUSS MicroTec': 'SMHN.DE',
    'TeamViewer': 'TMV.DE',
    'United Internet': 'UTDI.DE',
    'Verbio': 'VBK.DE',
}


# ============================================================
# FESTE SEKTOR-TYPEN
# Fallback, falls Yahoo/EODHD keine Sektordaten liefern.
# Besonders wichtig für Banken und Versicherungen, weil sie
# sektorspezifisch bewertet werden.
# ============================================================

SECTOR_TYPE_BY_SYMBOL = {
    # EURO STOXX 50 – Banken / Finanz
    "SAN.MC": "Bank/Finanz",
    "BBVA.MC": "Bank/Finanz",
    "BNP.PA": "Bank/Finanz",
    "DBK.DE": "Bank/Finanz",
    "DB1.DE": "Bank/Finanz",
    "INGA.AS": "Bank/Finanz",
    "ISP.MI": "Bank/Finanz",
    "UCG.MI": "Bank/Finanz",
    "NDA-FI.HE": "Bank/Finanz",
    "ADYEN.AS": "Bank/Finanz",

    # EURO STOXX 50 – Versicherungen
    "ALV.DE": "Versicherung",
    "CS.PA": "Versicherung",
    "MUV2.DE": "Versicherung",

    # Dow Jones / Nasdaq – Finanz
    "AXP": "Bank/Finanz",
    "GS": "Bank/Finanz",
    "JPM": "Bank/Finanz",
    "V": "Bank/Finanz",
    "PYPL": "Bank/Finanz",
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
# MOMENTUM-HILFSFUNKTIONEN
# ============================================================

def segment_monthly_return(close, start_pos, end_pos):
    """
    Berechnet die Performance eines historischen Zeitsegments und
    normiert sie auf eine durchschnittliche 21-Handelstage-Monatsrate.

    start_pos / end_pos sind iloc-Positionen relativ zum Serienende,
    z. B. -63 bis -21 für ungefähr Monate 2–3.

    Dadurch sind unterschiedlich lange Segmente miteinander vergleichbar.
    """
    try:
        n = len(close)

        start_idx = start_pos if start_pos >= 0 else n + start_pos
        end_idx = end_pos if end_pos >= 0 else n + end_pos

        start_idx = max(0, start_idx)
        end_idx = min(n - 1, end_idx)

        if start_idx < 0 or end_idx <= start_idx or start_idx >= n:
            return None

        start_price = float(close.iloc[start_idx])
        end_price = float(close.iloc[end_idx])

        if start_price <= 0 or end_price <= 0:
            return None

        trading_days = end_idx - start_idx
        if trading_days <= 0:
            return None

        total_factor = end_price / start_price

        monthly_factor = total_factor ** (21.0 / trading_days)
        return (monthly_factor - 1.0) * 100.0

    except Exception:
        return None


def acceleration_score_from_segments(r1, r23, r46, r712):
    """
    Beschleunigungskomponente mit maximal 22 Punkten.

    Verwendet vier NICHT überlappende Zeitfenster:
    - letzter Monat
    - Monate 2–3
    - Monate 4–6
    - Monate 7–12

    Alle Segmente sind bereits auf eine durchschnittliche Monatsrate
    normiert.

    Idealfall:
        1M > 2–3M > 4–6M > 7–12M
    und der jüngste Monat ist positiv.

    Bewertung über vier Bedingungen:
    0 Abweichungen -> 22,0 Punkte
    1 Abweichung   -> 16,5 Punkte (75 %)
    2 Abweichungen -> 11,0 Punkte (50 %)
    3 Abweichungen ->  5,5 Punkte (25 %)
    4 Abweichungen ->  0,0 Punkte
    """
    values = [r1, r23, r46, r712]

    # Für die gewünschte 4-Stufen-Bewertung müssen alle vier Segmente
    # verfügbar sein.
    if any(v is None for v in values):
        return None

    conditions = [
        r1 > r23,
        r23 > r46,
        r46 > r712,
        r1 > 0,
    ]

    deviations = sum(1 for ok in conditions if not ok)

    factor_by_deviations = {
        0: 1.00,
        1: 0.75,
        2: 0.50,
        3: 0.25,
        4: 0.00,
    }

    return 22.0 * factor_by_deviations[deviations]


def acceleration_label(r1, r23, r46, r712):
    values = [r1, r23, r46, r712]

    if any(v is None for v in values):
        return "zu wenig Daten"

    conditions = [
        r1 > r23,
        r23 > r46,
        r46 > r712,
        r1 > 0,
    ]
    deviations = sum(1 for ok in conditions if not ok)

    if deviations == 0:
        return "🚀 ideal beschleunigt"
    if deviations == 1:
        return "↗ fast ideal"
    if deviations == 2:
        return "↗ teilweise beschleunigt"
    if deviations == 3:
        return "↘ überwiegend nicht beschleunigt"
    return "⛔ keine Beschleunigung"


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
def get_yahoo_histories_batch(symbols_tuple):
    """
    Lädt die Kursreihen eines kompletten Index in EINEM Yahoo-Aufruf.
    Das reduziert Rate-Limits insbesondere beim Nasdaq-100 erheblich.

    Rückgabe:
        dict[symbol] -> DataFrame mit mindestens Close
    """
    symbols = list(symbols_tuple)
    result = {}

    if not symbols:
        return result

    try:
        raw = yf.download(
            tickers=symbols,
            period="2y",
            interval="1d",
            auto_adjust=True,
            group_by="ticker",
            threads=True,
            progress=False,
        )

        if raw is None or raw.empty:
            return result

        # Mehrere Ticker -> MultiIndex-Spalten
        if isinstance(raw.columns, pd.MultiIndex):
            level0 = set(raw.columns.get_level_values(0))
            level1 = set(raw.columns.get_level_values(1))

            for symbol in symbols:
                try:
                    if symbol in level0:
                        sub = raw[symbol].copy()
                    elif symbol in level1:
                        sub = raw.xs(symbol, axis=1, level=1).copy()
                    else:
                        continue

                    if "Close" not in sub.columns:
                        continue

                    sub = sub.dropna(subset=["Close"])
                    if not sub.empty:
                        result[symbol] = sub
                except Exception:
                    continue

        # Ein Ticker -> normale Spalten
        elif len(symbols) == 1 and "Close" in raw.columns:
            sub = raw.dropna(subset=["Close"]).copy()
            if not sub.empty:
                result[symbols[0]] = sub

    except Exception:
        return {}

    return result


@st.cache_data(ttl=3600, show_spinner=False)
def get_yahoo_history(symbol):
    try:
        hist = yf.Ticker(symbol).history(
            period="2y",
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
        start_date = end_date - timedelta(days=740)

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
        start_date = end_date - timedelta(days=740)

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


def _statement_row(df, candidates):
    if df is None or getattr(df, "empty", True):
        return None

    for name in candidates:
        if name in df.index:
            row = pd.to_numeric(df.loc[name], errors="coerce").dropna()
            if len(row) > 0:
                # yfinance liefert die jüngsten Perioden normalerweise zuerst.
                return row
    return None


def _safe_growth(latest, previous):
    latest = safe_float(latest)
    previous = safe_float(previous)
    if latest is None or previous is None or previous == 0:
        return None
    return (latest / previous - 1) * 100


@st.cache_data(ttl=21600, show_spinner=False)
def get_yahoo_fundamentals(symbol):
    """
    Yahoo-Fundamentaldaten in zwei Stufen:
    1. ticker.info
    2. Berechnung aus Income Statement / Balance Sheet / fast_info

    Die zweite Stufe ist wichtig, weil ticker.info bei europäischen Aktien
    gelegentlich leer oder unvollständig zurückkommt.
    """
    result = {}
    used_info = False
    used_statements = False

    try:
        ticker = yf.Ticker(symbol)

        # ---------- 1. Yahoo info ----------
        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        if info:
            used_info = True
            result.update({
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
            })

        # ---------- 2. Yahoo Finanzberichte ----------
        # Nur laden, wenn zentrale Werte fehlen.
        important_keys = [
            "ROE %",
            "Operative Marge %",
            "Debt/Equity",
            "KGV",
            "Gewinnwachstum %",
            "Umsatzwachstum %",
            "KBV",
        ]

        if any(result.get(k) is None for k in important_keys):
            try:
                income = ticker.income_stmt
            except Exception:
                income = pd.DataFrame()

            try:
                balance = ticker.balance_sheet
            except Exception:
                balance = pd.DataFrame()

            try:
                fast = ticker.fast_info
            except Exception:
                fast = {}

            revenue_row = _statement_row(
                income,
                ["Total Revenue", "Operating Revenue"]
            )
            operating_income_row = _statement_row(
                income,
                ["Operating Income"]
            )
            net_income_row = _statement_row(
                income,
                [
                    "Net Income",
                    "Net Income Common Stockholders",
                    "Net Income Including Noncontrolling Interests",
                ]
            )
            equity_row = _statement_row(
                balance,
                [
                    "Stockholders Equity",
                    "Total Stockholder Equity",
                    "Common Stock Equity",
                    "Total Equity Gross Minority Interest",
                ]
            )
            debt_row = _statement_row(
                balance,
                [
                    "Total Debt",
                    "Total Non Current Liabilities Net Minority Interest",
                ]
            )

            revenue_latest = (
                float(revenue_row.iloc[0])
                if revenue_row is not None and len(revenue_row) >= 1
                else None
            )
            revenue_prev = (
                float(revenue_row.iloc[1])
                if revenue_row is not None and len(revenue_row) >= 2
                else None
            )

            op_income_latest = (
                float(operating_income_row.iloc[0])
                if operating_income_row is not None and len(operating_income_row) >= 1
                else None
            )

            net_income_latest = (
                float(net_income_row.iloc[0])
                if net_income_row is not None and len(net_income_row) >= 1
                else None
            )
            net_income_prev = (
                float(net_income_row.iloc[1])
                if net_income_row is not None and len(net_income_row) >= 2
                else None
            )

            equity_latest = (
                float(equity_row.iloc[0])
                if equity_row is not None and len(equity_row) >= 1
                else None
            )

            debt_latest = (
                float(debt_row.iloc[0])
                if debt_row is not None and len(debt_row) >= 1
                else None
            )

            market_cap = None
            try:
                market_cap = safe_float(fast.get("market_cap"))
            except Exception:
                pass

            calculated = {}

            if (
                net_income_latest is not None
                and equity_latest is not None
                and equity_latest != 0
            ):
                calculated["ROE %"] = (
                    net_income_latest / equity_latest * 100
                )

            if (
                op_income_latest is not None
                and revenue_latest is not None
                and revenue_latest != 0
            ):
                calculated["Operative Marge %"] = (
                    op_income_latest / revenue_latest * 100
                )

            if (
                debt_latest is not None
                and equity_latest is not None
                and equity_latest != 0
            ):
                calculated["Debt/Equity"] = (
                    debt_latest / equity_latest * 100
                )

            calculated["Gewinnwachstum %"] = _safe_growth(
                net_income_latest,
                net_income_prev
            )
            calculated["Umsatzwachstum %"] = _safe_growth(
                revenue_latest,
                revenue_prev
            )

            if (
                market_cap is not None
                and net_income_latest is not None
                and net_income_latest > 0
            ):
                calculated["KGV"] = market_cap / net_income_latest

            if (
                market_cap is not None
                and equity_latest is not None
                and equity_latest > 0
            ):
                calculated["KBV"] = market_cap / equity_latest

            for key, value in calculated.items():
                if result.get(key) is None and value is not None:
                    result[key] = value
                    used_statements = True

        if not result:
            return {}

        if used_info and used_statements:
            result["_Quelle"] = "Yahoo info + Finanzberichte"
        elif used_statements:
            result["_Quelle"] = "Yahoo Finanzberichte"
        elif used_info:
            result["_Quelle"] = "Yahoo Finance"
        else:
            result["_Quelle"] = "keine"

        return result

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
    primary = dict(primary or {})
    secondary = dict(secondary or {})

    primary_source = primary.pop("_Quelle", "")
    secondary_source = secondary.pop("_Quelle", "")

    merged = dict(primary)
    used_secondary = False

    for key, value in secondary.items():
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
        source = (
            (primary_source or "Yahoo Finance")
            + " + EODHD"
        )
    elif primary:
        source = primary_source or "Yahoo Finance"
    elif secondary:
        source = secondary_source or "EODHD"
    else:
        source = "keine"

    return merged, source


def get_stock_data(symbol, preloaded_hist=None):
    """
    Robuste Datenfunktion:
    - technische Daten werden zuerst und unabhängig berechnet
    - Fundamentaldaten werden anschließend nur ergänzt
    - Fehler bei Fundamentals dürfen die technischen Daten NICHT verwerfen
    """
    # --------------------------------------------------------
    # A) KURSDATEN / TECHNIK
    # --------------------------------------------------------
    try:
        if preloaded_hist is not None and not preloaded_hist.empty:
            hist = preloaded_hist.copy()
            price_source = "Yahoo Finance (Batch)"
        else:
            hist, price_source = get_redundant_history(symbol)

        if hist is None or hist.empty or "Close" not in hist.columns:
            return None

        close = pd.to_numeric(
            hist["Close"],
            errors="coerce"
        ).dropna()

        # Für alle technischen Kriterien benötigen wir mindestens GD200.
        if len(close) < 200:
            return None

        # Nur die jüngsten ca. 12 Handelsmonate verwenden.
        # Ein kleiner Puffer über 252 Tage hilft bei Feiertagen.
        close = close.tail(260)

        current = float(close.iloc[-1])

        r1m = (
            segment_monthly_return(close, -22, -1)
            if len(close) >= 22 else None
        )

        r2_3m = (
            segment_monthly_return(close, -64, -22)
            if len(close) >= 64 else None
        )

        r4_6m = (
            segment_monthly_return(close, -127, -64)
            if len(close) >= 127 else None
        )

        # Monate 7–12: ausschließlich der ältere Halbjahresblock,
        # ohne Monate 1–6.
        if len(close) >= 240:
            start_7_12 = -min(len(close), 252)
            r7_12m = segment_monthly_return(
                close,
                start_7_12,
                -127
            )
        else:
            r7_12m = None

        acceleration = acceleration_score_from_segments(
            r1m,
            r2_3m,
            r4_6m,
            r7_12m
        )

        acceleration_text = acceleration_label(
            r1m,
            r2_3m,
            r4_6m,
            r7_12m
        )

        p6m = (
            (current / float(close.iloc[-126]) - 1) * 100
            if len(close) >= 126 else None
        )

        p12m = (
            (current / float(close.iloc[-252]) - 1) * 100
            if len(close) >= 252 else
            (current / float(close.iloc[0]) - 1) * 100
            if len(close) >= 240 else None
        )

        sma200 = float(close.tail(200).mean())
        distance_200 = (
            (current / sma200 - 1) * 100
            if sma200 else None
        )

        high52 = float(close.tail(252).max())
        distance_high = (
            (current / high52 - 1) * 100
            if high52 else None
        )

        daily_returns = close.tail(252).pct_change().dropna()

        volatility = (
            float(daily_returns.std())
            * math.sqrt(252)
            * 100
            if len(daily_returns) > 1
            else None
        )

        close_12m = close.tail(252)
        running_max = close_12m.cummax()
        drawdown = (close_12m / running_max - 1) * 100
        max_drawdown = (
            float(drawdown.min())
            if not drawdown.empty
            else None
        )

        data = {
            "Kurs": current,
            "1M Monatsrate %": r1m,
            "2-3M Monatsrate %": r2_3m,
            "4-6M Monatsrate %": r4_6m,
            "7-12M Monatsrate %": r7_12m,
            "Momentum-Beschleunigung": acceleration,
            "Momentum-Muster": acceleration_text,
            "6M %": p6m,
            "12M %": p12m,
            "200T %": distance_200,
            "52W-Hoch %": distance_high,
            "Volatilität %": volatility,
            "Max Drawdown %": max_drawdown,

            # Fundamentals zunächst leer; werden unten ergänzt.
            "ROE %": None,
            "Operative Marge %": None,
            "Debt/Equity": None,
            "KGV": None,
            "Forward-KGV": None,
            "Gewinnwachstum %": None,
            "Umsatzwachstum %": None,
            "Dividendenrendite %": None,
            "KBV": None,
            "Sektor": "",
            "Industrie": "",

            "Kursquelle": price_source,
            "Fundamentalquelle": "keine",
            "Sektor-Typ-Override": SECTOR_TYPE_BY_SYMBOL.get(symbol),
            "Datenfehler": "",
        }

    except Exception as exc:
        # Technische Fehler sollen künftig sichtbar diagnostizierbar sein.
        # Wir geben ein spezielles Fehlerobjekt zurück statt still None.
        return {
            "_TECHNIK_FEHLER": f"{type(exc).__name__}: {exc}",
            "Kursquelle": (
                "Yahoo Finance (Batch)"
                if preloaded_hist is not None and not preloaded_hist.empty
                else "unbekannt"
            ),
        }

    # --------------------------------------------------------
    # B) FUNDAMENTALDATEN – OPTIONAL
    # --------------------------------------------------------
    try:
        yahoo_f = get_yahoo_fundamentals(symbol)

        central_keys = [
            "ROE %",
            "KGV",
            "Forward-KGV",
            "Gewinnwachstum %",
            "Umsatzwachstum %",
        ]

        yahoo_has_gaps = (
            not yahoo_f
            or any(
                yahoo_f.get(k) is None
                for k in central_keys
            )
        )

        eod_f = (
            get_eodhd_fundamentals(symbol)
            if yahoo_has_gaps
            else {}
        )

        fundamentals, fundamental_source = merge_fundamentals(
            yahoo_f,
            eod_f
        )

        for key in [
            "ROE %",
            "Operative Marge %",
            "Debt/Equity",
            "KGV",
            "Forward-KGV",
            "Gewinnwachstum %",
            "Umsatzwachstum %",
            "Dividendenrendite %",
            "KBV",
            "Sektor",
            "Industrie",
        ]:
            if fundamentals.get(key) not in (None, ""):
                data[key] = fundamentals.get(key)

        data["Fundamentalquelle"] = fundamental_source

    except Exception as exc:
        # Technischer Score bleibt erhalten.
        data["Fundamentalquelle"] = "keine"
        data["Datenfehler"] = f"Fundamentals: {type(exc).__name__}"

    return data


# ============================================================
# SEKTORERKENNUNG
# ============================================================

def sector_type(d):
    override = d.get("Sektor-Typ-Override")
    if override:
        return override

    sector = (d.get("Sektor") or "").lower()
    industry = (d.get("Industrie") or "").lower()

    if (
        "insurance" in industry
        or "insurance" in sector
    ):
        return "Versicherung"

    if (
        "financial" in sector
        or "bank" in industry
        or "banks" in industry
        or "credit services" in industry
    ):
        return "Bank/Finanz"

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
    """
    Momentum-Teilscore 0–100.

    Rohpunktesystem:
    - kurzfristige Beschleunigung: maximal 22 Punkte
    - GD200-Trend:               maximal 13 Punkte
    ------------------------------------------------
    - gesamt:                    maximal 35 Punkte

    Der Rohwert wird anschließend auf 0–100 normiert.
    Im Gesamtscore hat Momentum ein Gewicht von 32 %.
    """
    raw_points = 0.0
    raw_maximum = 0.0

    acceleration = d.get("Momentum-Beschleunigung")
    ma = d.get("200T %")

    # A) Beschleunigung – maximal 22 Punkte
    if acceleration is not None:
        raw_points += clamp(acceleration)
        raw_maximum += 22.0

    # B) GD200-Trend – maximal 13 Punkte
    if ma is not None:
        raw_maximum += 13.0

        if ma >= 20:
            raw_points += 13.0
        elif ma >= 15:
            raw_points += 12.0
        elif ma >= 10:
            raw_points += 10.5
        elif ma >= 5:
            raw_points += 9.0
        elif ma >= 0:
            raw_points += 7.0
        elif ma >= -5:
            raw_points += 4.0
        elif ma >= -10:
            raw_points += 2.0
        else:
            raw_points += 0.0

    if raw_maximum == 0:
        return None

    return clamp(raw_points / raw_maximum * 100.0)


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
    """
    Levermann-light: 6 automatisch verfügbare Kriterien.
    Das ist bewusst NICHT der vollständige klassische 13-Punkte-Levermann-Score.

    Kriterien:
    1. ROE
    2. operative Marge (nur Standardunternehmen)
    3. KGV
    4. Forward-KGV
    5. 6-Monats-Performance
    6. 12-Monats-Performance

    Rückgabe:
    score      = Summe aus -1 / 0 / +1
    available  = Zahl der tatsächlich verfügbaren Kriterien
    possible   = Zahl der grundsätzlich anwendbaren Kriterien
                 (6 bei Standard, 5 bei Bank/Versicherung)
    """
    score = 0
    available = 0

    roe = d.get("ROE %")
    margin = d.get("Operative Marge %")
    pe = d.get("KGV")
    forward_pe = d.get("Forward-KGV")
    p6 = d.get("6M %")
    p12 = d.get("12M %")

    typ = sector_type(d)
    possible = 6 if typ == "Standard" else 5

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

    return score, available, possible


# ============================================================
# GESAMTSCORE
# ============================================================

def total_score(quality, valuation, momentum, risk):
    components = [
        (quality, 0.27),
        (valuation, 0.22),
        (momentum, 0.32),
        (risk, 0.19),
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

# Interner Konsistenzcheck
if "SECTOR_TYPE_BY_SYMBOL" not in globals():
    st.error(
        "Interner Konfigurationsfehler: SECTOR_TYPE_BY_SYMBOL fehlt. "
        "Bitte die aktuelle vollständige streamlit_app.py verwenden."
    )
    st.stop()

if index_name == "Nasdaq-100":
    st.info(f"**{index_name}: {len(stocks)} aktuelle Wertpapiere**")
else:
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

elif index_name == "TecDAX":
    if len(stocks) != 30:
        st.warning(
            f"⚠️ Das TecDAX-Universum enthält {len(stocks)} statt 30 Aktien."
        )
    else:
        st.success("✅ TecDAX-Universum vollständig: 30 Aktien.")

elif index_name == "Nasdaq-100":
    if len(stocks) < 100:
        st.warning(
            f"⚠️ Das Nasdaq-100-Universum enthält nur {len(stocks)} Wertpapiere."
        )
    else:
        st.success(
            f"✅ Nasdaq-100-Universum vollständig: {len(stocks)} aktuelle Wertpapiere."
        )

min_coverage = st.slider(
    "Mindest-Datenabdeckung",
    min_value=0,
    max_value=100,
    value=50,
    step=5
)

st.caption(
    "Empfehlung: zunächst 50 %. Momentum (32 %) und Risiko (19 %) ergeben zusammen "
    "51 % Datenabdeckung. Ein technisch berechneter Teilscore bleibt damit sichtbar. "
    "Für einen vollständig fundamental + technisch belegten Vergleich sollte die "
    "Abdeckung möglichst 95–100 % erreichen."
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

    status.write(
        f"Lade Kursdaten für **{index_name}** gesammelt über Yahoo Finance ..."
    )

    batch_histories = get_yahoo_histories_batch(
        tuple(stocks.values())
    )

    st.caption(
        f"Yahoo-Batch: {len(batch_histories)}/{total} Kursreihen (2 Jahre) direkt geladen. "
        "Fehlende Titel werden anschließend einzeln über Yahoo, EODHD und Stooq versucht. "
        "Für Momentum/GD200 werden mindestens 200 Handelstage benötigt."
    )

    for i, (name, symbol) in enumerate(stocks.items()):
        status.write(
            f"Analysiere {i + 1}/{total}: **{name}**"
        )

        data = get_stock_data(
            symbol,
            preloaded_hist=batch_histories.get(symbol)
        )

        if data is not None and data.get("_TECHNIK_FEHLER"):
            omitted.append({
                "Aktie": name,
                "Symbol": symbol,
                "Grund": "Technischer Berechnungsfehler",
                "Kursquelle": data.get("Kursquelle"),
                "Fundamentalquelle": "nicht geprüft",
                "Datenfehler": data.get("_TECHNIK_FEHLER"),
            })

        elif data is not None:
            quality = quality_score(data)
            valuation = valuation_score(data)
            momentum = momentum_score(data)
            risk = risk_score(data)

            levermann, levermann_n, levermann_possible = levermann_score(data)

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
                    "Score-Status": (
                        "Vollscore" if coverage >= 95
                        else "Teilscore"
                    ),
                    "Qualität": quality,
                    "Bewertung": valuation,
                    "Momentum": momentum,
                    "Risiko": risk,
                    "Levermann": levermann,
                    "Lev.-Daten": f"{levermann_n}/{levermann_possible}",
                    "Daten %": coverage,
                    "KGV": data.get("KGV"),
                    "Forward-KGV": data.get("Forward-KGV"),
                    "KBV": data.get("KBV"),
                    "ROE %": data.get("ROE %"),
                    "Marge %": data.get("Operative Marge %"),
                    "Gewinnwachstum %": data.get("Gewinnwachstum %"),
                    "1M mtl. %": data.get("1M Monatsrate %"),
                    "2-3M mtl. %": data.get("2-3M Monatsrate %"),
                    "4-6M mtl. %": data.get("4-6M Monatsrate %"),
                    "7-12M mtl. %": data.get("7-12M Monatsrate %"),
                    "Beschl. Punkte /22": data.get("Momentum-Beschleunigung"),
                    "Momentum-Muster": data.get("Momentum-Muster"),
                    "6M %": data.get("6M %"),
                    "12M %": data.get("12M %"),
                    "Volatilität %": data.get("Volatilität %"),
                    "Drawdown %": data.get("Max Drawdown %"),
                    "Kursquelle": data.get("Kursquelle"),
                    "Fundamentalquelle": data.get("Fundamentalquelle"),
                    "Datenfehler": data.get("Datenfehler"),
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
                    "Momentum": momentum,
                    "Risiko": risk,
                    "Qualität": quality,
                    "Bewertung": valuation,
                    "Datenfehler": data.get("Datenfehler"),
                })
        else:
            omitted.append({
                "Aktie": name,
                "Symbol": symbol,
                "Grund": (
                    "Keine ausreichende Kursreihe verfügbar. "
                    "Yahoo-Batch und die Einzel-Fallbacks lieferten keine "
                    "für GD200/12-Monatsanalyse ausreichenden Daten."
                ),
                "Kursquelle": "keine",
                "Fundamentalquelle": "keine",
            })

        progress.progress((i + 1) / total)

    progress.empty()
    status.empty()

    if not results:
        st.error(
            "Keine Aktien mit der gewählten Mindest-Datenabdeckung gefunden. "
            "Bei fehlenden Fundamentaldaten ergeben Momentum (32 %) und Risiko (19 %) zusammen 51 % Abdeckung. "
            "Öffne unten 'Nicht ausgewertete Aktien', um den konkreten Grund zu sehen."
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
            "1M mtl. %",
            "2-3M mtl. %",
            "4-6M mtl. %",
            "7-12M mtl. %",
            "Beschl. Punkte /22",
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

- **27 % Qualität**
- **22 % Bewertung**
- **32 % Momentum**
- **19 % Risiko**

Fehlen einzelne Teilwerte, werden nur die verfügbaren Teilwerte verwendet
und auf 100 % der tatsächlich verfügbaren Gewichtung normiert. Die Spalte
**Daten %** zeigt deshalb, wie viel der vorgesehenen Gesamtgewichtung
tatsächlich mit Daten belegt ist.
"""
)

with st.expander("⭐ Qualität – 27 % des Gesamtscores"):
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

with st.expander("💶 Bewertung – 22 % des Gesamtscores"):
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

with st.expander("🚀 Momentum – 32 % des Gesamtscores"):
    st.markdown(
        """
Der **Momentum-Teilscore macht 32 % des Gesamtscores** aus.

Intern wird Momentum als **35-Punkte-Modul** berechnet:

- **22 Punkte kurzfristige Beschleunigung**
- **13 Punkte GD200-Trend**

Anschließend werden die erreichten Rohpunkte auf einen Momentum-Score
von **0 bis 100** normiert.

### 1. Kurzfristige Beschleunigung – maximal 22 Punkte

Es werden vier vollständig getrennte Zeitabschnitte betrachtet:

1. **letzter Monat**
2. **Monate 2–3**, also ausdrücklich **ohne Monat 1**
3. **Monate 4–6**, also ausdrücklich **ohne Monate 1–3**
4. **Monate 7–12**, also ausdrücklich **ohne Monate 1–6**

Jedes Segment wird auf eine **durchschnittliche Monatsrate** normiert.
Dadurch sind die unterschiedlich langen Zeitfenster direkt vergleichbar.

Die ideale Beschleunigungsstruktur lautet:

**1M > Ø Monate 2–3 > Ø Monate 4–6 > Ø Monate 7–12**

Beispiel:

- Monate 7–12: **+1 % pro Monat**
- Monate 4–6: **+2 % pro Monat**
- Monate 2–3: **+3 % pro Monat**
- letzter Monat: **+4 %**

→ **volle 22 Punkte**

Bewertung:

- **0 Abweichungen:** 22,0 Punkte = 100 %
- **1 Abweichung:** 16,5 Punkte = 75 %
- **2 Abweichungen:** 11,0 Punkte = 50 %
- **3 Abweichungen:** 5,5 Punkte = 25 %
- **4 Abweichungen:** 0 Punkte

Als vierte Bedingung wird zusätzlich verlangt, dass der jüngste Monat
positiv ist. So bekommt eine bloße relative Verbesserung innerhalb eines
weiterhin fallenden Trends nicht automatisch die volle Punktzahl.

### 2. GD200-Trend – maximal 13 Punkte

Je deutlicher der aktuelle Kurs oberhalb seines 200-Tage-Durchschnitts
liegt, desto höher ist der GD200-Teilscore. Ein Kurs unterhalb des GD200
führt entsprechend zu deutlich weniger Punkten.

Die Tabelle zeigt zusätzlich:

- **1M mtl. %**
- **2–3M mtl. %**
- **4–6M mtl. %**
- **7–12M mtl. %**
- **Beschl. Punkte /22**
- **Momentum-Muster**
"""
    )

with st.expander("🛡️ Risiko – 19 % des Gesamtscores"):
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


with st.expander("📊 Levermann-light – automatische Teilbewertung"):
    st.markdown(
        """
Der angezeigte **Levermann-light-Wert ist kein vollständiger klassischer
13-Kriterien-Levermann-Score**. Die App kann derzeit automatisch maximal
**6 Kriterien** bewerten:

- ROE
- operative Marge (bei Standardunternehmen)
- KGV
- Forward-KGV
- 6-Monats-Performance
- 12-Monats-Performance

Jedes verfügbare Kriterium erhält **−1, 0 oder +1**. Die Spalte
**Lev.-Daten** zeigt die tatsächlich vorhandenen Daten, z. B. **4/6**.
Bei Banken und Versicherungen entfällt die operative Marge als Kriterium;
dort lautet der maximale Nenner deshalb **5**.

Ein Wert wie **2 bei 2/6** bedeutet nicht dasselbe wie **2 bei 6/6**.
Deshalb sollte immer auch die Datenabdeckung betrachtet werden.
"""
    )

with st.expander("🗄️ Datenquellen und Redundanz"):
    st.markdown(
        """
**Kursdaten**

1. Yahoo Finance als **Batch-Abfrage für den gesamten gewählten Index**
2. Yahoo-Einzelabfrage nur für im Batch fehlende Titel
3. EODHD als weiterer Fallback
4. Stooq als letzter Fallback

Die Batch-Abfrage reduziert bei großen Universen wie dem Nasdaq-100
die Zahl der Yahoo-Anfragen drastisch und vermindert Rate-Limits.

EODHD wird für Kursdaten nur dann abgefragt, wenn Yahoo keine brauchbare
Historie liefert. Das schont insbesondere das kostenlose EODHD-Kontingent.

**Fundamentaldaten**

1. Yahoo `ticker.info`
2. Yahoo-Finanzberichte als Berechnungs-Fallback
3. EODHD als unabhängige Ergänzung für noch fehlende Werte, sofern der
   verwendete EODHD-Tarif Fundamentals freigeschaltet hat

Die Ergebnistabelle zeigt mit **Kursquelle** und **Fundamentalquelle**,
welche Quelle tatsächlich verwendet wurde.

**Sektorerkennung**

Für Banken und Versicherungen gibt es zusätzlich eine feste interne
Fallback-Zuordnung. Dadurch werden z. B. Allianz, AXA, Münchener Rück,
ING, Santander, BBVA, BNP Paribas, Intesa und UniCredit auch dann
sektorspezifisch bewertet, wenn Yahoo vorübergehend keine Sektordaten liefert.
"""
    )

st.caption(
    "Banken und Versicherungen werden sektorspezifisch behandelt. "
    "Der Levermann-Wert ist ein Teilscore aus den verfügbaren Kriterien. "
    "Kurzfristige Momentum-Beschleunigung wird über monatlich normierte "
    "Segmente 1M, 2–3M, 4–6M und 7–12M berücksichtigt. "
    "Das Screening ist ein quantitatives Hilfsmittel und keine Anlageberatung."
)


