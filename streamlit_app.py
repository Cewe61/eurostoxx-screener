import streamlit as st
import pandas as pd
import requests
import math
from io import StringIO
from datetime import date, timedelta

st.set_page_config(
    page_title="4-Index Aktien-Screener",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Aktien-Screener")
st.caption(
    "EURO STOXX 50 • TecDAX • Dow Jones • Nasdaq-100"
)

# ---------------------------------------------------------
# API-Schlüssel
# ---------------------------------------------------------

try:
    EODHD_KEY = st.secrets["EODHD_API_TOKEN"]
except Exception:
    EODHD_KEY = ""

try:
    AV_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]
except Exception:
    AV_KEY = ""


# ---------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------

def flatten_columns(df):
    cols = []
    for c in df.columns:
        if isinstance(c, tuple):
            c = " ".join(
                str(x) for x in c
                if str(x) != "nan"
            )
        cols.append(str(c).strip())
    df.columns = cols
    return df


def find_column(df, possibilities):
    for wanted in possibilities:
        for col in df.columns:
            if wanted.lower() == col.lower():
                return col

    for wanted in possibilities:
        for col in df.columns:
            if wanted.lower() in col.lower():
                return col

    return None


@st.cache_data(ttl=86400)
def read_tables(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(
        url,
        headers=headers,
        timeout=30
    )
    r.raise_for_status()

    return pd.read_html(
        StringIO(r.text)
    )


# ---------------------------------------------------------
# Index-Zusammensetzungen
# ---------------------------------------------------------

@st.cache_data(ttl=86400)
def load_nasdaq100():

    @st.cache_data(ttl=86400)
def load_nasdaq100():

    symbols = [
        "AAPL","ABNB","ADBE","ADI","ADP","ADSK","AEP","ALNY",
        "AMAT","AMD","AMGN","AMZN","APP","ARM","ASML","AVGO",
        "AXON","BKNG","BKR","CCEP","CDNS","CEG","CHTR","CMCSA",
        "COST","CPRT","CRWD","CSCO","CSGP","CSX","CTAS","CTSH",
        "DASH","DDOG","DXCM","EA","EXC","FANG","FAST","FER",
        "FTNT","GEHC","GILD","GOOG","GOOGL","HON","IDXX","INSM",
        "INTC","INTU","ISRG","KDP","KHC","KLAC","LIN","LRCX",
        "MAR","MCHP","MDLZ","MELI","META","MNST","MPWR","MRVL",
        "MSFT","MSTR","MU","NFLX","NVDA","NXPI","ODFL","ORLY",
        "PANW","PAYX","PCAR","PDD","PEP","PLTR","PYPL","QCOM",
        "REGN","ROP","ROST","SBUX","SHOP","SNPS","STX","TEAM",
        "TMUS","TRI","TSLA","TTWO","TXN","VRSK","VRTX","WBD",
        "WDAY","WDC","WMT","XEL","ZS"
    ]

    out = pd.DataFrame({
        "Aktie": symbols,
        "Symbol": symbols
    })

    out["Index"] = "Nasdaq-100"
    out["Markt"] = "USA"

    return out

@st.cache_data(ttl=86400)
def load_dow():

    tables = read_tables(
        "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
    )

    for df in tables:
        df = flatten_columns(df)

        ticker_col = find_column(
            df,
            ["Symbol", "Ticker"]
        )

        name_col = find_column(
            df,
            ["Company", "Name"]
        )

        if ticker_col and name_col and 25 <= len(df) <= 40:

            out = pd.DataFrame({
                "Aktie": df[name_col].astype(str),
                "Symbol": df[ticker_col].astype(str)
            })

            out["Index"] = "Dow Jones"
            out["Markt"] = "USA"

            return out.drop_duplicates("Symbol")

    raise ValueError(
        "Dow-Jones-Komponenten konnten nicht gelesen werden."
    )


@st.cache_data(ttl=86400)
def load_tecdax():

    tables = read_tables(
        "https://de.wikipedia.org/wiki/TecDAX"
    )

    for df in tables:
        df = flatten_columns(df)

        ticker_col = find_column(
            df,
            ["Symbol"]
        )

        name_col = find_column(
            df,
            ["Name"]
        )

        if ticker_col and name_col and 25 <= len(df) <= 40:

            out = pd.DataFrame({
                "Aktie": df[name_col].astype(str),
                "Symbol": df[ticker_col].astype(str)
            })

            out["Index"] = "TecDAX"
            out["Markt"] = "Deutschland"

            return out.drop_duplicates("Symbol")

    raise ValueError(
        "TecDAX-Komponenten konnten nicht gelesen werden."
    )


@st.cache_data(ttl=86400)
def load_eurostoxx50():

    tables = read_tables(
        "https://en.wikipedia.org/wiki/EURO_STOXX_50"
    )

    for df in tables:
        df = flatten_columns(df)

        ticker_col = find_column(
            df,
            ["Ticker"]
        )

        name_col = find_column(
            df,
            ["Name"]
        )

        if ticker_col and name_col and 45 <= len(df) <= 55:

            out = pd.DataFrame({
                "Aktie": df[name_col].astype(str),
                "Symbol": df[ticker_col].astype(str)
            })

            out["Index"] = "EURO STOXX 50"
            out["Markt"] = "Eurozone"

            return out.drop_duplicates("Symbol")

    raise ValueError(
        "EURO-STOXX-50-Komponenten konnten nicht gelesen werden."
    )


def get_universe(index_name):

    if index_name == "Nasdaq-100":
        return load_nasdaq100()

    if index_name == "Dow Jones":
        return load_dow()

    if index_name == "TecDAX":
        return load_tecdax()

    if index_name == "EURO STOXX 50":
        return load_eurostoxx50()

    frames = [
        load_eurostoxx50(),
        load_tecdax(),
        load_dow(),
        load_nasdaq100()
    ]

    all_stocks = pd.concat(
        frames,
        ignore_index=True
    )

    return all_stocks.drop_duplicates(
        ["Aktie", "Symbol"]
    )


# ---------------------------------------------------------
# Ticker für EODHD erzeugen
# ---------------------------------------------------------

def eodhd_symbol(symbol, market):

    symbol = str(symbol).strip()

    if market == "USA":
        return f"{symbol}.US"

    if market == "Deutschland":

        if symbol.endswith(".DE"):
            symbol = symbol[:-3]

        return f"{symbol}.XETRA"

    # EURO STOXX 50 nutzt auf Wikipedia Yahoo-artige
    # Börsen-Suffixe.

    suffix_map = {
        ".DE": "XETRA",
        ".PA": "PA",
        ".AS": "AS",
        ".BR": "BR",
        ".MC": "MC",
        ".MI": "MI",
        ".HE": "HE",
        ".IR": "IR"
    }

    for suffix, exchange in suffix_map.items():

        if symbol.endswith(suffix):

            code = symbol[:-len(suffix)]

            return f"{code}.{exchange}"

    return None


# ---------------------------------------------------------
# Kursdaten EODHD
# ---------------------------------------------------------

@st.cache_data(ttl=86400)
def get_prices(ticker):

    if not ticker or not EODHD_KEY:
        return None

    start = date.today() - timedelta(days=370)

    url = f"https://eodhd.com/api/eod/{ticker}"

    params = {
        "api_token": EODHD_KEY,
        "fmt": "json",
        "period": "d",
        "order": "a",
        "from": start.isoformat()
    }

    try:

        r = requests.get(
            url,
            params=params,
            timeout=30
        )

        if r.status_code != 200:
            return None

        data = r.json()

        if not isinstance(data, list):
            return None

        if len(data) < 60:
            return None

        return pd.DataFrame(data)

    except Exception:
        return None


# ---------------------------------------------------------
# Alpha Vantage – USA Fundamentaldaten
# ---------------------------------------------------------

@st.cache_data(ttl=86400)
def get_us_fundamentals(symbol):

    if not AV_KEY:
        return None

    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": AV_KEY
    }

    try:

        r = requests.get(
            "https://www.alphavantage.co/query",
            params=params,
            timeout=30
        )

        if r.status_code != 200:
            return None

        data = r.json()

        if not data.get("Symbol"):
            return None

        return data

    except Exception:
        return None


# ---------------------------------------------------------
# Zahlen sicher umwandeln
# ---------------------------------------------------------

def number(value):

    try:

        if value in [
            None,
            "",
            "None",
            "null",
            "-"
        ]:
            return None

        return float(value)

    except Exception:
        return None


def percentage(value):

    value = number(value)

    if value is None:
        return None

    # Alpha Vantage liefert viele Prozentwerte
    # als Dezimalzahl, z. B. 0.25 = 25 %
    if abs(value) <= 2:
        value *= 100

    return value


# ---------------------------------------------------------
# Technische Kennzahlen
# ---------------------------------------------------------

def price_metrics(prices):

    if prices is None:
        return None

    col = (
        "adjusted_close"
        if "adjusted_close" in prices.columns
        else "close"
    )

    close = pd.to_numeric(
        prices[col],
        errors="coerce"
    ).dropna()

    if len(close) < 130:
        return None

    current = close.iloc[-1]

    p6 = (
        close.iloc[-126]
        if len(close) >= 126
        else close.iloc[0]
    )

    p12 = (
        close.iloc[-252]
        if len(close) >= 252
        else close.iloc[0]
    )

    ret6 = (
        current / p6 - 1
    ) * 100

    ret12 = (
        current / p12 - 1
    ) * 100

    if len(close) >= 200:
        ma200 = close.tail(200).mean()
        ma200_distance = (
            current / ma200 - 1
        ) * 100
    else:
        ma200_distance = None

    daily_returns = close.pct_change().dropna()

    volatility = (
        daily_returns.std()
        * math.sqrt(252)
        * 100
    )

    running_max = close.cummax()

    drawdown = (
        close / running_max - 1
    ) * 100

    max_drawdown = drawdown.min()

    return {
        "6M %": ret6,
        "12M %": ret12,
        "200T %": ma200_distance,
        "Volatilität %": volatility,
        "Max Drawdown %": max_drawdown
    }


# ---------------------------------------------------------
# Scores
# ---------------------------------------------------------

def momentum_score(m):

    if not m:
        return None

    score = 0

    r6 = m["6M %"]
    r12 = m["12M %"]
    ma = m["200T %"]

    if r6 >= 20:
        score += 35
    elif r6 >= 10:
        score += 28
    elif r6 >= 5:
        score += 20
    elif r6 >= 0:
        score += 10

    if r12 >= 30:
        score += 40
    elif r12 >= 20:
        score += 34
    elif r12 >= 10:
        score += 26
    elif r12 >= 0:
        score += 12

    if ma is not None:

        if ma >= 15:
            score += 25
        elif ma >= 5:
            score += 20
        elif ma >= 0:
            score += 15
        elif ma >= -5:
            score += 5

    return min(score, 100)


def risk_score(m):

    if not m:
        return None

    vol = m["Volatilität %"]
    dd = m["Max Drawdown %"]

    score = 100

    if vol > 50:
        score -= 45
    elif vol > 40:
        score -= 35
    elif vol > 30:
        score -= 25
    elif vol > 20:
        score -= 12

    if dd < -50:
        score -= 45
    elif dd < -40:
        score -= 35
    elif dd < -30:
        score -= 25
    elif dd < -20:
        score -= 12

    return max(0, score)


def quality_score(f):

    if not f:
        return None

    roe = percentage(
        f.get("ReturnOnEquityTTM")
    )

    margin = percentage(
        f.get("OperatingMarginTTM")
    )

    if roe is None and margin is None:
        return None

    points = 0
    maximum = 0

    if roe is not None:

        maximum += 50

        if roe >= 20:
            points += 50
        elif roe >= 15:
            points += 40
        elif roe >= 10:
            points += 28
        elif roe >= 5:
            points += 15

    if margin is not None:

        maximum += 50

        if margin >= 20:
            points += 50
        elif margin >= 12:
            points += 40
        elif margin >= 6:
            points += 25
        elif margin >= 3:
            points += 12

    return (
        points / maximum * 100
        if maximum
        else None
    )


def valuation_score(f):

    if not f:
        return None

    pe = number(
        f.get("PERatio")
    )

    if pe is None or pe <= 0:
        return None

    if pe <= 10:
        return 100

    if pe <= 12:
        return 90

    if pe <= 16:
        return 75

    if pe <= 20:
        return 60

    if pe <= 25:
        return 45

    if pe <= 35:
        return 25

    if pe <= 50:
        return 10

    return 0


# ---------------------------------------------------------
# Levermann-Teilscore
# Nur Kriterien mit tatsächlich vorhandenen Daten.
# ---------------------------------------------------------

def levermann_partial(f, m):

    points = 0
    available = 0

    # Eigenkapitalrendite
    if f:

        roe = percentage(
            f.get("ReturnOnEquityTTM")
        )

        if roe is not None:

            available += 1

            if roe > 20:
                points += 1
            elif roe < 10:
                points -= 1

        # EBIT-/operative Marge
        margin = percentage(
            f.get("OperatingMarginTTM")
        )

        if margin is not None:

            available += 1

            if margin > 12:
                points += 1
            elif margin < 6:
                points -= 1

        # aktuelles KGV
        pe = number(
            f.get("PERatio")
        )

        if pe is not None and pe > 0:

            available += 1

            if pe < 12:
                points += 1
            elif pe > 16:
                points -= 1

    if m:

        # 6-Monats-Momentum
        available += 1

        if m["6M %"] > 5:
            points += 1
        elif m["6M %"] < -5:
            points -= 1

        # 12-Monats-Momentum
        available += 1

        if m["12M %"] > 5:
            points += 1
        elif m["12M %"] < -5:
            points -= 1

    return points, available


# ---------------------------------------------------------
# Gesamtscore mit transparenter Datenabdeckung
# ---------------------------------------------------------

def combined_score(
    quality,
    valuation,
    momentum,
    risk
):

    components = [
        (quality, 0.30),
        (valuation, 0.20),
        (momentum, 0.30),
        (risk, 0.20)
    ]

    available = [
        (value, weight)
        for value, weight in components
        if value is not None
    ]

    if not available:
        return None, 0

    used_weight = sum(
        weight
        for _, weight in available
    )

    score = sum(
        value * weight
        for value, weight in available
    ) / used_weight

    coverage = used_weight * 100

    return score, coverage


# ---------------------------------------------------------
# Einzelaktie analysieren
# ---------------------------------------------------------

def analyse(row):

    name = row["Aktie"]
    symbol = row["Symbol"]
    market = row["Markt"]
    index_name = row["Index"]

    eod_symbol = eodhd_symbol(
        symbol,
        market
    )

    prices = get_prices(
        eod_symbol
    )

    metrics = price_metrics(
        prices
    )

    fundamentals = None

    # Alpha Vantage zunächst nur für US-Werte
    if market == "USA":

        fundamentals = get_us_fundamentals(
            symbol
        )

    mom = momentum_score(
        metrics
    )

    risk = risk_score(
        metrics
    )

    qual = quality_score(
        fundamentals
    )

    val = valuation_score(
        fundamentals
    )

    levermann, levermann_n = levermann_partial(
        fundamentals,
        metrics
    )

    total, coverage = combined_score(
        qual,
        val,
        mom,
        risk
    )

    pe = (
        number(fundamentals.get("PERatio"))
        if fundamentals
        else None
    )

    roe = (
        percentage(
            fundamentals.get(
                "ReturnOnEquityTTM"
            )
        )
        if fundamentals
        else None
    )

    margin = (
        percentage(
            fundamentals.get(
                "OperatingMarginTTM"
            )
        )
        if fundamentals
        else None
    )

    return {
        "Aktie": name,
        "Symbol": symbol,
        "Index": index_name,
        "Levermann": levermann,
        "Levermann Daten": f"{levermann_n}/13",
        "Qualität": qual,
        "Bewertung": val,
        "Momentum": mom,
        "Risiko": risk,
        "Gesamtscore": total,
        "Datenabdeckung %": coverage,
        "KGV": pe,
        "ROE %": roe,
        "Marge %": margin,
        "6M %": (
            metrics["6M %"]
            if metrics
            else None
        ),
        "12M %": (
            metrics["12M %"]
            if metrics
            else None
        ),
        "200T %": (
            metrics["200T %"]
            if metrics
            else None
        )
    }


# ---------------------------------------------------------
# Oberfläche
# ---------------------------------------------------------

st.sidebar.header("Screener")

index_choice = st.sidebar.selectbox(
    "Aktienuniversum",
    [
        "Alle",
        "EURO STOXX 50",
        "TecDAX",
        "Dow Jones",
        "Nasdaq-100"
    ]
)

batch_size = st.sidebar.slider(
    "Aktien pro Durchlauf",
    min_value=1,
    max_value=10,
    value=5
)

try:

    universe = get_universe(
        index_choice
    )

except Exception as e:

    st.error(
        f"Indexliste konnte nicht geladen werden: {e}"
    )

    st.stop()


st.write(
    f"**{len(universe)} Indexpositionen gefunden.**"
)

max_start = max(
    0,
    len(universe) - batch_size
)

start = st.sidebar.number_input(
    "Startposition",
    min_value=0,
    max_value=max_start,
    value=0,
    step=batch_size
)

end = min(
    start + batch_size,
    len(universe)
)

batch = universe.iloc[
    start:end
].copy()


st.subheader("Aktien dieses Durchlaufs")

st.dataframe(
    batch[
        [
            "Aktie",
            "Symbol",
            "Index"
        ]
    ],
    hide_index=True,
    use_container_width=True
)


st.info(
    "Wegen der kostenlosen API-Limits werden "
    "höchstens 10 Aktien pro Durchlauf analysiert. "
    "Danach kann die Startposition erhöht werden."
)


if st.button(
    "🔄 Diese Aktien analysieren",
    type="primary"
):

    rows = []

    progress = st.progress(0)

    status = st.empty()

    for i, (_, row) in enumerate(
        batch.iterrows()
    ):

        status.write(
            f'Analysiere {row["Aktie"]} …'
        )

        try:

            result = analyse(row)

            rows.append(result)

        except Exception as e:

            rows.append({
                "Aktie": row["Aktie"],
                "Symbol": row["Symbol"],
                "Index": row["Index"],
                "Fehler": str(e)
            })

        progress.progress(
            (i + 1) / len(batch)
        )

    progress.empty()
    status.empty()

    df = pd.DataFrame(rows)

    if "Gesamtscore" in df.columns:

        df = df.sort_values(
            "Gesamtscore",
            ascending=False,
            na_position="last"
        )

        df.insert(
            0,
            "Rang",
            range(1, len(df) + 1)
        )

    # Zahlen schöner darstellen
    numeric_cols = [
        "Qualität",
        "Bewertung",
        "Momentum",
        "Risiko",
        "Gesamtscore",
        "Datenabdeckung %",
        "KGV",
        "ROE %",
        "Marge %",
        "6M %",
        "12M %",
        "200T %"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).round(1)

    st.subheader("📊 Ergebnis")

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )

    if (
        "Gesamtscore" in df.columns
        and df["Gesamtscore"].notna().any()
    ):

        top = df[
            df["Gesamtscore"].notna()
        ].head(3)

        st.subheader("🏆 Top 3 dieses Durchlaufs")

        cols = st.columns(
            min(3, len(top))
        )

        for col, (_, row) in zip(
            cols,
            top.iterrows()
        ):

            with col:

                st.metric(
                    row["Aktie"],
                    f'{row["Gesamtscore"]:.1f}'
                )

                st.caption(
                    f'Levermann {row["Levermann"]:+.0f} '
                    f'({row["Levermann Daten"]})'
                )


st.markdown("---")

st.caption(
    "Levermann = Teilscore aus den tatsächlich "
    "verfügbaren Kriterien. Fehlende Kriterien "
    "werden nicht als Null bewertet. "
    "Der Screener ist eine Entscheidungshilfe "
    "und keine Anlageberatung."
)
