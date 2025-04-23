import streamlit as st
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime

# ------------------ Configuration ------------------
FRED_API_KEY = '83709bc9a35d7d11c07bad8630ff8b2c'  # Replace with your own key

# ------------------ FRED API Utility ------------------
FED_FUNDS_RATE_SERIES = "FEDFUNDS"  # Federal Funds Effective Rate
def get_fed_interest_rates():
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": FED_FUNDS_RATE_SERIES,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": "2020-01-01"
    }
    response = requests.get(url, params=params)
    data = response.json()
    observations = data.get("observations", [])
    
    df = pd.DataFrame(observations)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df
    st.subheader("Federal Funds Interest Rate Trend")

try:
    fed_df = get_fed_interest_rates()
    st.line_chart(fed_df.set_index('date')['value'])
    latest = fed_df.iloc[-1]
    st.info(f"Latest Fed Funds Rate: {latest['value']}% on {latest['date'].strftime('%b %d, %Y')}")
except Exception as e:
    st.error("Failed to fetch interest rate data.")
    st.text(str(e))

# ------------------ Market Index Utility ------------------
def get_index_value(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.history(period='1d')['Close'].iloc[-1]

# ------------------ App Layout ------------------
st.title("Sentinel FCU Economic Tracker v2")

# Interest Rates Section
st.header("Interest Rates")
fed_rate = fetch_fred_series("FEDFUNDS")
mortgage_rate = fetch_fred_series("MORTGAGE30US")

if fed_rate is not None:
    st.metric("Federal Funds Rate", f"{fed_rate:.2f}%")
else:
    st.warning("Fed rate unavailable")

if mortgage_rate is not None:
    st.metric("30-Year Mortgage Rate", f"{mortgage_rate:.2f}%")
else:
    st.warning("Mortgage rate unavailable")

# Regional Indicator: SD Unemployment
st.header("Regional Economic Indicators")
sd_unemployment = fetch_fred_series("SDUR")
if sd_unemployment is not None:
    st.metric("South Dakota Unemployment Rate", f"{sd_unemployment:.2f}%")
else:
    st.warning("SD unemployment data unavailable")

# Market Indices
st.header("Market Indices")
sp500 = get_index_value("^GSPC")
nasdaq = get_index_value("^IXIC")
st.metric("S&P 500", f"{sp500:,.2f}")
st.metric("NASDAQ", f"{nasdaq:,.2f}")

# Legislative Alerts
st.header("Legislative Alerts")
import requests
API_KEY = 'ice98ixPmVFcY8WBJbf9qohf0YvQDEdGB7ILqM54'
headers = {'X-API-Key': API_KEY}
params = {'query': 'credit union', 'limit': 5}
response = requests.get('https://api.congress.gov/v3/bill', headers=headers, params=params)
data = response.json()
import streamlit as st
for bill in data['bills']:
    title = bill.get('title', 'No title available')
    summary = bill.get('summary', 'No summary available')
    url = bill.get('url', '#')
    st.subheader(title)
    st.write(summary)
    st.markdown(f"[Read more]({url})")
if 'lending' in summary.lower():
    st.warning("This bill may affect credit union lending practices.")

# Placeholder for Local Business Trends
st.header("Local Business Trends")
st.info("Coming soon: Headlines on openings, closures, and economic impact.")

# Placeholder for NCUA Competitor Trends
st.header("NCUA Competitor Trends")
st.info("Coming soon: Peer comparison from NCUA research.")

# Placeholder for CUNA Data
st.header("CUNA Insights")
st.info("Coming soon: Reports and advocacy updates from CUNA.")

# Alerts
st.header("Automated Alerts")
if fed_rate and fed_rate > 5.0:
    st.error("Alert: Fed rate exceeds 5%! Monetary tightening likely.")
if mortgage_rate and mortgage_rate > 7.0:
    st.warning("Alert: Mortgage rates above 7% may impact lending.")
