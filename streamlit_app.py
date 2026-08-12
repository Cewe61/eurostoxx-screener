import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# ============================================================
# GRUNDEINSTELLUNGEN
# ============================================================

st.set_page_config(
    page_title="4-Index Aktien-Screener",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Aktien-Screener")
st.caption(
    "EURO STOXX 50 • TecDAX • Dow Jones • Nasdaq-100"
)

# ============================================================
# AKTIENLISTEN
# ============================================================

# ------------------------------------------------------------
# DOW JONES
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# NASDAQ-100
# ------------------------------------------------------------

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
    "AstraZeneca": "AZN",
    "Atlassian": "TEAM",
    "Autodesk": "ADSK",
    "Automatic Data Processing": "ADP",
    "Axon Enterprise": "AXON",
    "Baker Hughes": "BKR",
    "Booking Holdings": "BKNG",
    "Broadcom": "AVGO",
    "Cadence Design Systems": "CDNS",
    "CDW": "CDW",
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
    "MongoDB": "MDB",
    "Monster Beverage": "MNST",
    "Netflix": "NFLX",
    "Nvidia": "NVDA",
    "NXP Semiconductors": "NXPI",
    "Old Dominion Freight Line": "ODFL",
    "ON Semiconductor": "ON",
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
    "The Trade Desk": "TTD",
    "Verisk Analytics": "VRSK",
    "Vertex Pharmaceuticals": "VRTX",
    "Warner Bros. Discovery": "WBD",
    "Workday": "WDAY",
    "Xcel Energy": "XEL",
    "Zscaler": "ZS",
}

# ------------------------------------------------------------
# EURO STOXX 50
# Yahoo-Symbole mit jeweiligem Börsenplatz
# ------------------------------------------------------------

EUROSTOXX50 = {
    "Adidas": "ADS.DE",
    "Air Liquide": "AI.PA",
    "Airbus": "AIR.PA",
    "Allianz": "ALV.DE",
    "Anheuser-Busch InBev": "ABI.BR",
    "ASML": "ASML.AS",
    "AXA": "CS.PA",
    "BASF": "BAS.DE",
    "Bayer": "BAYN.DE",
    "BBVA": "BBVA.MC",
    "BMW": "BMW.DE",
    "BNP Paribas": "BNP.PA",
    "Danone": "BN.PA",
    "Deutsche Bank": "DBK.DE",
    "Deutsche Post / DHL": "DHL.DE",
    "Deutsche Telekom": "DTE.DE",
    "Enel": "ENEL.MI",
    "Eni": "ENI.MI",
    "EssilorLuxottica": "EL.PA",
    "Ferrari": "RACE.MI",
    "Hermès": "RMS.PA",
    "Iberdrola": "IBE.MC",
    "Inditex": "ITX.MC",
    "ING": "INGA.AS",
    "Intesa Sanpaolo": "ISP.MI",
    "Kering": "KER.PA",
    "L'Oréal": "OR.PA",
    "LVMH": "MC.PA",
    "Mercedes-Benz": "MBG.DE",
    "Münchener Rück": "MUV2.DE",
    "Nokia": "NOKIA.HE",
    "Prosus": "PRX.AS",
    "Safran": "SAF.PA",
    "Sanofi": "SAN.PA",
    "Santander": "SAN.MC",
    "SAP": "SAP.DE",
    "Schneider Electric": "SU.PA",
    "Siemens": "SIE.DE",
    "Stellantis": "STLAM.MI",
    "TotalEnergies": "TTE.PA",
    "UniCredit": "UCG.MI",
    "Vinci": "DG.PA",
    "Volkswagen Vz.": "VOW3.DE",
}

# ------------------------------------------------------------
# TECDAX
# ------------------------------------------------------------

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
# AUSWAHL
# ============================================================

index_name = st.selectbox(
    "Index auswählen",
    list(INDEX_DATA.keys())
)

stocks = INDEX_DATA[index_name]

st.info(
    f"{index_name}: {len(stocks)} Aktien in der aktuellen Screener-Liste."
)

# ============================================================
# KURSDATEN
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_price_data(symbol):
    try:
        ticker = yf.Ticker(symbol)

        hist = ticker.history(
            period="1y",
            auto_adjust=True
        )

        if hist is None or hist.empty:
            return None

        close = hist["Close"].dropna()

        if len(close) < 20:
            return None

        current = float(close.iloc[-1])

        # Performance
        perf_1m = None
        perf_3m = None
        perf_6m = None
        perf_12m = None

        if len(close) >= 22:
            perf_1m = (current / close.iloc[-22] - 1) * 100

        if len(close) >= 66:
            perf_3m = (current / close.iloc[-66] - 1) * 100

        if len(close) >= 132:
            perf_6m = (current / close.iloc[-132] - 1) * 100

        if len(close) >= 240:
            perf_12m = (current / close.iloc[0] - 1) * 100

        # gleitende Durchschnitte
        sma50 = None
        sma200 = None

        if len(close) >= 50:
            sma50 = float(close.tail(50).mean())

        if len(close) >= 200:
            sma200 = float(close.tail(200).mean())

        # Abstand zum 52-Wochen-Hoch
        high_52 = float(close.max())

        distance_high = (
            (current / high_52 - 1) * 100
            if high_52 else None
        )

        return {
            "Kurs": current,
            "1M %": perf_1m,
            "3M %": perf_3m,
            "6M %": perf_6m,
            "12M %": perf_12m,
            "SMA50": sma50,
            "SMA200": sma200,
            "Abstand 52W-Hoch %": distance_high,
        }

    except Exception:
        return None


# ============================================================
# MOMENTUM-SCORE
# ============================================================

def momentum_score(data):
    if data is None:
        return None

    score = 0

    # 6-Monats-Momentum
    p6 = data.get("6M %")

    if p6 is not None:
        if p6 > 20:
            score += 3
        elif p6 > 10:
            score += 2
        elif p6 > 0:
            score += 1
        elif p6 < -20:
            score -= 3
        elif p6 < -10:
            score -= 2
        else:
            score -= 1

    # 12-Monats-Momentum
    p12 = data.get("12M %")

    if p12 is not None:
        if p12 > 25:
            score += 3
        elif p12 > 10:
            score += 2
        elif p12 > 0:
            score += 1
        elif p12 < -25:
            score -= 3
        elif p12 < -10:
            score -= 2
        else:
            score -= 1

    # Trend
    kurs = data.get("Kurs")
    sma50 = data.get("SMA50")
    sma200 = data.get("SMA200")

    if kurs is not None and sma50 is not None:
        score += 1 if kurs > sma50 else -1

    if kurs is not None and sma200 is not None:
        score += 2 if kurs > sma200 else -2

    # Nähe zum Jahreshoch
    high_dist = data.get("Abstand 52W-Hoch %")

    if high_dist is not None:
        if high_dist > -5:
            score += 2
        elif high_dist > -10:
            score += 1
        elif high_dist < -30:
            score -= 2
        elif high_dist < -20:
            score -= 1

    return score


# ============================================================
# SCREENING
# ============================================================

if st.button(
    f"🔎 {index_name} analysieren",
    type="primary"
):

    progress = st.progress(0)

    status = st.empty()

    results = []

    total = len(stocks)

    for i, (name, symbol) in enumerate(stocks.items()):

        status.write(
            f"Analysiere {i + 1}/{total}: **{name}**"
        )

        data = get_price_data(symbol)

        if data is not None:

            score = momentum_score(data)

            results.append({
                "Aktie": name,
                "Symbol": symbol,
                "Index": index_name,
                "Score": score,
                **data
            })

        progress.progress((i + 1) / total)

    status.empty()
    progress.empty()

    if not results:
        st.error(
            "Es konnten keine Kursdaten geladen werden."
        )

    else:
        df = pd.DataFrame(results)

        df = df.sort_values(
            "Score",
            ascending=False
        ).reset_index(drop=True)

        df.insert(
            0,
            "Rang",
            range(1, len(df) + 1)
        )

        st.subheader(
            f"🏆 Ranking – {index_name}"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🥇 Top 10")

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )

        csv = df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ Ergebnis als CSV herunterladen",
            csv,
            file_name=(
                index_name
                .replace(" ", "_")
                .replace("-", "_")
                + "_ranking.csv"
            ),
            mime="text/csv"
        )

# ============================================================
# INFORMATION
# ============================================================

st.divider()

st.caption(
    "Version 1: stabiles Kurs- und Momentum-Screening. "
    "Im nächsten Schritt werden Qualitäts-, Bewertungs- "
    "und Levermann-Kriterien ergänzt."
)
