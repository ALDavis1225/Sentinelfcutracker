import streamlit as st
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime

# ------------------ Configuration ------------------
FRED_API_KEY = 'https://fred.stlouisfed.org/docs/api/api_key.html'  # Replace with your own key

# ------------------ FRED API Utility ------------------
def fetch_fred_series(series_id, observation_count=1):
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': observation_count
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['observations']:
            return float(data['observations'][0]['value'])
    return None

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

# Placeholder for Legislative Alerts
st.header("Legislative Alerts")
st.info("Coming soon: Summarized bills affecting credit unions.")

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
