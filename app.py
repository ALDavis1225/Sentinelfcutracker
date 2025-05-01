import streamlit as st
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime

# ------------------ Configuration ------------------
FRED_API_KEY = '83709bc9a35d7d11c07bad8630ff8b2c'  # Replace with your own key

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
    
# Fetch historical Fed Funds Rate trend from 1/1/2020
def fetch_fed_funds_trend():
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': 'FEDFUNDS',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': '2020-01-01'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['observations'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df[['date', 'value']]
    return None

def fetch_mortgage_rate_trend():
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': 'MORTGAGE30US',
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': '2020-01-01'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['observations'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.set_index('date').resample('M').last().dropna().reset_index()  # Monthly rate trend
        df['rate_change'] = df['value'].diff()
        return df
    return None

def fetch_sd_unemployment_trend():
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': 'SDUR',  # South Dakota Unemployment Rate
        'api_key': FRED_API_KEY,
        'file_type': 'json',
        'observation_start': '2020-01-01'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['observations'])
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df[['date', 'value']]
    return None
    
# ------------------ Market Index Utility ------------------
def get_index_value(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.history(period='5d')['Close'].iloc[-1]

# ------------------ App Layout ------------------
st.title("Sentinel FCU Economic Tracker")

# Interest Rates Section
st.header("Interest Rates")
fed_rate = fetch_fred_series("FEDFUNDS")
mortgage_rate = fetch_fred_series("MORTGAGE30US")

if fed_rate is not None:
    st.metric("Federal Funds Rate", f"{fed_rate:.2f}%")
else:
    st.warning("Fed rate unavailable")

st.subheader("Federal Funds Rate Trend (Since 2020)")
fed_trend_df = fetch_fed_funds_trend()

if fed_trend_df is not None:
    st.line_chart(fed_trend_df.set_index('date')['value'])
else:
    st.warning("Unable to fetch Fed Funds historical data.")
    
if mortgage_rate is not None:
    st.metric("30-Year Mortgage Rate", f"{mortgage_rate:.2f}%")
else:
    st.warning("Mortgage rate unavailable")

st.subheader("30-Year Mortgage Rate Trend (Since 2020)")
mortgage_trend_df = fetch_mortgage_rate_trend()

if mortgage_trend_df is not None:
    st.line_chart(mortgage_trend_df.set_index('date')['value'])

    # Check for significant jumps
    recent_jump = mortgage_trend_df['rate_change'].iloc[-1]
    if recent_jump > 0.5:
        st.error(f"Alert: Mortgage rate jumped by {recent_jump:.2f}% last month!")
    elif recent_jump > 0.25:
        st.warning(f"Notice: Mortgage rate rose by {recent_jump:.2f}% last month.")
else:
    st.warning("Unable to fetch mortgage rate trend data.")
    
# Regional Indicator: SD Unemployment
st.header("Regional Economic Indicators")
sd_unemployment = fetch_fred_series("SDUR")

if sd_unemployment is not None:
    st.metric("South Dakota Unemployment Rate", f"{sd_unemployment:.2f}%")
else:
    st.warning("SD unemployment data unavailable")

st.subheader("South Dakota Unemployment Rate Trend (Since 2020)")
sd_trend_df = fetch_sd_unemployment_trend()

if sd_trend_df is not None:
    st.line_chart(sd_trend_df.set_index('date')['value'])
else:
    st.warning("Unable to fetch SD unemployment trend data.")
    
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
