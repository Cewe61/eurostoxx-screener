import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="Europa Aktien-Screener",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Europa Aktien-Screener")
st.caption("Fundamental-, Qualitäts-, Momentum- und Risiko-Screening europäischer Aktien")

# API-Key sicher aus Streamlit Secrets lesen
try:
    API_TOKEN = st.secrets["EODHD_API_TOKEN"]
except Exception:
    API_TOKEN = ""

st.sidebar.header("Einstellungen")

min_score = st.sidebar.slider(
    "Mindest-Gesamtscore",
    min_value=0,
    max_value=100,
    value=60
)

st.sidebar.markdown("""
### Bewertungsmodell

**Qualität – 30 Punkte**
- Eigenkapitalrendite
- operative Marge
- Verschuldung
- Gewinnstabilität

**Bewertung – 25 Punkte**
- KGV
- Kurs/Cashflow
- Dividendenrendite

**Momentum – 25 Punkte**
- 6-Monats-Trend
- 12-Monats-Trend
- Abstand zur 200-Tage-Linie

**Risiko – 20 Punkte**
- Volatilität
- Drawdown
- Verschuldungsrisiko
""")

def eodhd_get(endpoint, params=None):
    if not API_TOKEN:
        return None

    url = f"https://eodhd.com/api/{endpoint}"

    p = {
        "api_token": API_TOKEN,
        "fmt": "json"
    }

    if params:
        p.update(params)

    try:
        r = requests.get(url, params=p, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def score_value(value, good, bad, reverse=False):
    if value is None:
        return 0

    try:
        value = float(value)
    except Exception:
        return 0

    if reverse:
        if value <= good:
            return 100
        if value >= bad:
            return 0
        return 100 * (bad - value) / (bad - good)

    if value >= good:
        return 100
    if value <= bad:
        return 0

    return 100 * (value - bad) / (good - bad)


st.subheader("Screener")

st.info(
    "Der Screener wird nach Verbindung mit EODHD automatisch "
    "Markt- und Fundamentaldaten europäischer Aktien auswerten."
)

if not API_TOKEN:
    st.warning(
        "Noch kein EODHD API-Key hinterlegt. "
        "Wir richten diesen anschließend sicher über Streamlit Secrets ein."
    )

# Beispielstruktur für die spätere Ergebnisanzeige
columns = [
    "Rang",
    "Aktie",
    "Ticker",
    "Qualität",
    "Bewertung",
    "Momentum",
    "Risiko",
    "Gesamtscore"
]

df = pd.DataFrame(columns=columns)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.caption(
    "Hinweis: Der Score dient als systematische Entscheidungshilfe "
    "und stellt keine Anlageberatung dar."
)
