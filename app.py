import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st

# ---------- Data Collection Example: Fed Interest Rate (FRED) ----------
def get_fed_rate():
    url = "https://fred.stlouisfed.org/series/FEDFUNDS"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        rate_tag = soup.find('div', class_='series-meta-observation-value')
        rate = float(rate_tag.text.strip().replace('%',''))
        return rate
    except:
        return None

# ---------- Data Collection Example: Local News Headlines ----------
def get_local_headlines():
    url = "https://rapidcityjournal.com/news/local/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    for item in soup.select('h3 a')[:5]:
        headline = item.get_text(strip=True)
        link = item.get('href')
        if link and not link.startswith('http'):
            link = "https://rapidcityjournal.com" + link
        headlines.append((headline, link))

    return headlines

# ---------- Dashboard ----------
st.title("Sentinel FCU Economic Tracker")

# Display Fed Rate
fed_rate = get_fed_rate()
if fed_rate:
    st.metric(label="Federal Funds Rate", value=f"{fed_rate}%")
else:
    st.warning("Unable to retrieve Fed rate.")

# Display Local News
st.subheader("Local News Headlines")
headlines = get_local_headlines()
if headlines:
    for title, link in headlines:
        st.markdown(f"- [{title}]({link})")
else:
    st.warning("Unable to retrieve local news.")

# Sample Visualization (Static Example for Prototype)
st.subheader("Example: Unemployment Rate (Placeholder Data)")
data = {
    'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'Rate': [3.8, 3.9, 3.7, 3.8]
}
df = pd.DataFrame(data)
st.line_chart(df.set_index('Month'))