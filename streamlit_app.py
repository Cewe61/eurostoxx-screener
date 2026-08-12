import streamlit as st
import pandas as pd
import requests
import math
from datetime import date, timedelta

st.set_page_config(
    page_title="Europa Aktien-Screener",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Europa Aktien-Screener")
st.caption(
    "Qualität • Bewertung • Momentum • Risiko – "
    "systematisches Ranking europäischer Aktien"
)

try:
    API_TOKEN = st.secrets["EODHD_API_TOKEN"]
except Exception:
    API_TOKEN = ""

try:
    AV_API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]
except Exception:
    AV_API_KEY = ""

st.subheader("🧪 Alpha-Vantage-Test")

if AV_API_KEY:
    st.success("Alpha-Vantage-Key wird von Streamlit erkannt.")
else:
    st.error("Alpha-Vantage-Key wird NICHT erkannt.")

try:
    av_response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "OVERVIEW",
            "symbol": "SAP.DEX",
            "apikey": AV_API_KEY
        },
        timeout=30
    )

    st.write("Alpha Vantage HTTP-Status:", av_response.status_code)

    av_data = av_response.json()

    if "Symbol" in av_data:
        st.success("Fundamentaldaten für SAP wurden gefunden.")
        st.write("Symbol:", av_data.get("Symbol"))
        st.write("Name:", av_data.get("Name"))
        st.write("KGV:", av_data.get("PERatio"))
        st.write("Eigenkapitalrendite:", av_data.get("ReturnOnEquityTTM"))
        st.write("Operative Marge:", av_data.get("OperatingMarginTTM"))
    else:
        st.warning("Keine regulären Fundamentaldaten erhalten.")
        st.json(av_data)

except Exception as e:
    st.error(f"Alpha-Vantage-Fehler: {e}")
    

    st.subheader("🔧 EODHD-Diagnose")

if API_TOKEN:
    st.success("API-Key wird von Streamlit erkannt.")
else:
    st.error("API-Key wird NICHT erkannt.")

try:
    test_url = "https://eodhd.com/api/v1.1/fundamentals/SAP.XETRA"
    test_response = requests.get(
        test_url,
        params={
            "api_token": API_TOKEN,
            "fmt": "json"
        },
        timeout=30
    )

    st.write("Fundamentals HTTP-Status:", test_response.status_code)
    st.code(test_response.text[:500])

except Exception as e:
    st.error(f"Fundamentals-Fehler: {e}")

try:
    test_url2 = "https://eodhd.com/api/eod/SAP.XETRA"
    test_response2 = requests.get(
        test_url2,
        params={
            "api_token": API_TOKEN,
            "fmt": "json",
            "period": "d"
        },
        timeout=30
    )

    st.write("Kursdaten HTTP-Status:", test_response2.status_code)
    st.code(test_response2.text[:500])

except Exception as e:
    st.error(f"Kursdaten-Fehler: {e}")

# ---------------------------------------------------------
# TEST-UNIVERSUM
# Danach erweitern wir auf ca. 600 europäische Aktien.
# ---------------------------------------------------------

STOCKS = {
    "SAP": "SAP.XETRA",
    "Siemens": "SIE.XETRA",
    "Allianz": "ALV.XETRA",
    "Deutsche Telekom": "DTE.XETRA",
    "Munich Re": "MUV2.XETRA",
    "BASF": "BAS.XETRA",
    "Mercedes-Benz": "MBG.XETRA",
    "BMW": "BMW.XETRA",
    "Adidas": "ADS.XETRA",
    "Infineon": "IFX.XETRA",
}

# ---------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------

def safe_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def clamp(x, low=0, high=100):
    return max(low, min(high, x))


@st.cache_data(ttl=3600)
def get_fundamentals(ticker):
    url = f"https://eodhd.com/api/v1.1/fundamentals/{ticker}"
    params = {
        "api_token": API_TOKEN,
        "fmt": "json"
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


@st.cache_data(ttl=3600)
def get_prices(ticker):
    start = date.today() - timedelta(days=420)

    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        "api_token": API_TOKEN,
        "fmt": "json",
        "period": "d",
        "order": "a",
        "from": start.isoformat()
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()

        if not isinstance(data, list) or len(data) < 50:
            return None

        return pd.DataFrame(data)

    except Exception:
        return None


def nested(data, *keys):
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)

    return current


# ---------------------------------------------------------
# Scores
# ---------------------------------------------------------

def quality_score(roe, operating_margin, debt_equity):

    score = 0

    # ROE: 0–40 Punkte
    if roe is not None:
        if roe >= 20:
            score += 40
        elif roe >= 15:
            score += 32
        elif roe >= 10:
            score += 24
        elif roe >= 5:
            score += 12

    # operative Marge: 0–35
    if operating_margin is not None:
        if operating_margin >= 20:
            score += 35
        elif operating_margin >= 15:
            score += 28
        elif operating_margin >= 10:
            score += 20
        elif operating_margin >= 5:
            score += 10

    # Verschuldung: 0–25
    if debt_equity is not None:
        if debt_equity <= 50:
            score += 25
        elif debt_equity <= 100:
            score += 18
        elif debt_equity <= 150:
            score += 10
        elif debt_equity <= 250:
            score += 4

    return clamp(score)


def valuation_score(pe, dividend_yield):

    score = 0

    # KGV: 0–70
    if pe is not None and pe > 0:
        if pe <= 10:
            score += 70
        elif pe <= 15:
            score += 60
        elif pe <= 20:
            score += 48
        elif pe <= 25:
            score += 35
        elif pe <= 35:
            score += 20
        elif pe <= 50:
            score += 8

    # Dividende: 0–30
    if dividend_yield is not None:
        if dividend_yield >= 4:
            score += 30
        elif dividend_yield >= 3:
            score += 24
        elif dividend_yield >= 2:
            score += 18
        elif dividend_yield >= 1:
            score += 10

    return clamp(score)


def momentum_score(prices):

    if prices is None or len(prices) < 200:
        return None, None, None, None

    close_col = "adjusted_close" if "adjusted_close" in prices.columns else "close"

    close = pd.to_numeric(prices[close_col], errors="coerce").dropna()

    if len(close) < 200:
        return None, None, None, None

    current = close.iloc[-1]

    p6 = close.iloc[-126] if len(close) >= 126 else close.iloc[0]
    p12 = close.iloc[-252] if len(close) >= 252 else close.iloc[0]

    ret6 = (current / p6 - 1) * 100
    ret12 = (current / p12 - 1) * 100

    ma200 = close.tail(200).mean()
    above_ma200 = (current / ma200 - 1) * 100

    score = 0

    # 6 Monate – 35 Punkte
    if ret6 >= 20:
        score += 35
    elif ret6 >= 10:
        score += 28
    elif ret6 >= 5:
        score += 20
    elif ret6 >= 0:
        score += 10

    # 12 Monate – 40 Punkte
    if ret12 >= 30:
        score += 40
    elif ret12 >= 20:
        score += 34
    elif ret12 >= 10:
        score += 26
    elif ret12 >= 0:
        score += 12

    # 200-Tage-Linie – 25 Punkte
    if above_ma200 >= 15:
        score += 25
    elif above_ma200 >= 5:
        score += 20
    elif above_ma200 >= 0:
        score += 15
    elif above_ma200 >= -5:
        score += 5

    return clamp(score), ret6, ret12, above_ma200


def risk_score(prices):

    if prices is None or len(prices) < 60:
        return None, None, None

    close_col = "adjusted_close" if "adjusted_close" in prices.columns else "close"

    close = pd.to_numeric(prices[close_col], errors="coerce").dropna()

    returns = close.pct_change().dropna()

    if len(returns) < 30:
        return None, None, None

    volatility = returns.std() * math.sqrt(252) * 100

    running_max = close.cummax()
    drawdown = ((close / running_max) - 1) * 100
    max_drawdown = drawdown.min()

    score = 100

    # Volatilität
    if volatility > 50:
        score -= 45
    elif volatility > 40:
        score -= 35
    elif volatility > 30:
        score -= 25
    elif volatility > 20:
        score -= 12

    # Drawdown
    if max_drawdown < -50:
        score -= 45
    elif max_drawdown < -40:
        score -= 35
    elif max_drawdown < -30:
        score -= 25
    elif max_drawdown < -20:
        score -= 12

    return clamp(score), volatility, max_drawdown


# ---------------------------------------------------------
# Einzelaktie analysieren
# ---------------------------------------------------------

def analyse_stock(name, ticker):

    fundamentals = get_fundamentals(ticker)
    prices = get_prices(ticker)

    if not fundamentals or prices is None:
        return None

    highlights = fundamentals.get("Highlights", {})
    valuation = fundamentals.get("Valuation", {})
    technicals = fundamentals.get("Technicals", {})

    roe = safe_float(highlights.get("ReturnOnEquityTTM"))
    operating_margin = safe_float(highlights.get("OperatingMarginTTM"))

    pe = safe_float(highlights.get("PERatio"))
    if pe is None:
        pe = safe_float(valuation.get("TrailingPE"))

    dividend_yield = safe_float(highlights.get("DividendYield"))

    if dividend_yield is not None and dividend_yield < 1:
        dividend_yield *= 100

    debt_equity = safe_float(technicals.get("DebtToEquity"))

    q_score = quality_score(
        roe,
        operating_margin,
        debt_equity
    )

    v_score = valuation_score(
        pe,
        dividend_yield
    )

    m_score, ret6, ret12, above_ma200 = momentum_score(prices)

    r_score, volatility, max_drawdown = risk_score(prices)

    if m_score is None:
        m_score = 0

    if r_score is None:
        r_score = 0

    # -----------------------------------------------------
    # Gesamtscore:
    # Qualität 30 %
    # Bewertung 25 %
    # Momentum 25 %
    # Risiko 20 %
    # -----------------------------------------------------

    total = (
        0.30 * q_score
        + 0.25 * v_score
        + 0.25 * m_score
        + 0.20 * r_score
    )

    return {
        "Aktie": name,
        "Ticker": ticker,
        "Qualität": round(q_score, 1),
        "Bewertung": round(v_score, 1),
        "Momentum": round(m_score, 1),
        "Risiko": round(r_score, 1),
        "Gesamtscore": round(total, 1),

        "KGV": round(pe, 1) if pe is not None else None,
        "Div.-Rendite %": round(dividend_yield, 2)
        if dividend_yield is not None else None,

        "6 Monate %": round(ret6, 1)
        if ret6 is not None else None,

        "12 Monate %": round(ret12, 1)
        if ret12 is not None else None,

        "ggü. 200-Tage-Linie %": round(above_ma200, 1)
        if above_ma200 is not None else None,

        "Volatilität %": round(volatility, 1)
        if volatility is not None else None,

        "Max. Drawdown %": round(max_drawdown, 1)
        if max_drawdown is not None else None,
    }


# ---------------------------------------------------------
# Oberfläche
# ---------------------------------------------------------

st.sidebar.header("Einstellungen")

min_score = st.sidebar.slider(
    "Mindest-Gesamtscore",
    min_value=0,
    max_value=100,
    value=0
)

st.sidebar.markdown(
    """
### Gewichtung

- **Qualität:** 30 %
- **Bewertung:** 25 %
- **Momentum:** 25 %
- **Risiko:** 20 %
"""
)

if not API_TOKEN:
    st.error(
        "EODHD API-Key fehlt. Bitte unter "
        "Streamlit → Settings → Secrets hinterlegen."
    )
    st.stop()

st.subheader("Aktien-Ranking")

if st.button("🔄 Screener starten", type="primary"):

    rows = []

    progress = st.progress(0)

    status = st.empty()

    count = len(STOCKS)

    for i, (name, ticker) in enumerate(STOCKS.items()):

        status.write(f"Analysiere {name} …")

        result = analyse_stock(name, ticker)

        if result:
            rows.append(result)

        progress.progress((i + 1) / count)

    progress.empty()
    status.empty()

    if not rows:

        st.error(
            "Es konnten keine Aktien ausgewertet werden. "
            "Bitte EODHD-Zugang bzw. Tarif prüfen."
        )

    else:

        df = pd.DataFrame(rows)

        df = df.sort_values(
            "Gesamtscore",
            ascending=False
        ).reset_index(drop=True)

        df.insert(
            0,
            "Rang",
            range(1, len(df) + 1)
        )

        df = df[
            df["Gesamtscore"] >= min_score
        ]

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        st.subheader("🏆 Top 3")

        top = df.head(3)

        cols = st.columns(3)

        for col, (_, row) in zip(cols, top.iterrows()):

            with col:

                st.metric(
                    row["Aktie"],
                    f'{row["Gesamtscore"]:.1f} Punkte'
                )

                st.caption(
                    f'Qualität {row["Qualität"]:.0f} | '
                    f'Bewertung {row["Bewertung"]:.0f} | '
                    f'Momentum {row["Momentum"]:.0f} | '
                    f'Risiko {row["Risiko"]:.0f}'
                )

else:

    st.info(
        "Tippen Sie auf „Screener starten“, "
        "um die Aktien mit aktuellen EODHD-Daten auszuwerten."
    )

st.markdown("---")

st.caption(
    "Der Score ist eine systematische Entscheidungshilfe "
    "und keine Anlageberatung."
        )
