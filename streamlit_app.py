import streamlit as st
import pandas as pd
import yfinance as yf
import math

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
    "DHL Group": "DHL.DE",
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
# DATEN
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)

        hist = ticker.history(
            period="1y",
            auto_adjust=True
        )

        if hist is None or hist.empty:
            return None

        close = hist["Close"].dropna()

        if len(close) < 60:
            return None

        try:
            info = ticker.info or {}
        except Exception:
            info = {}

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

        drawdown = (
            close / running_max - 1
        ) * 100

        max_drawdown = float(drawdown.min())

        sector = str(info.get("sector") or "")
        industry = str(info.get("industry") or "")

        roe = pct(info.get("returnOnEquity"))
        margin = pct(info.get("operatingMargins"))
        debt_equity = safe_float(info.get("debtToEquity"))
        pe = safe_float(info.get("trailingPE"))
        forward_pe = safe_float(info.get("forwardPE"))
        earnings_growth = pct(info.get("earningsGrowth"))
        revenue_growth = pct(info.get("revenueGrowth"))
        dividend_yield = pct(info.get("dividendYield"))
        price_to_book = safe_float(info.get("priceToBook"))

        return {
            "Kurs": current,
            "6M %": p6m,
            "12M %": p12m,
            "200T %": distance_200,
            "52W-Hoch %": distance_high,
            "Volatilität %": volatility,
            "Max Drawdown %": max_drawdown,
            "ROE %": roe,
            "Operative Marge %": margin,
            "Debt/Equity": debt_equity,
            "KGV": pe,
            "Forward-KGV": forward_pe,
            "Gewinnwachstum %": earnings_growth,
            "Umsatzwachstum %": revenue_growth,
            "Dividendenrendite %": dividend_yield,
            "KBV": price_to_book,
            "Sektor": sector,
            "Industrie": industry,
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

min_coverage = st.slider(
    "Mindest-Datenabdeckung",
    min_value=0,
    max_value=100,
    value=50,
    step=10
)

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
                })

        progress.progress((i + 1) / total)

    progress.empty()
    status.empty()

    if not results:
        st.error(
            "Keine Aktien mit ausreichender Datenabdeckung gefunden."
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

st.divider()

st.caption(
    "Gesamtscore: Qualität 30 %, Bewertung 25 %, "
    "Momentum 25 %, Risiko 20 %. "
    "Banken und Versicherungen werden sektorspezifisch behandelt. "
    "Der Levermann-Wert ist ein Teilscore aus den verfügbaren Kriterien. "
    "Keine Anlageberatung."
)
