import streamlit as st
import pandas as pd
import os
import glob
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from scoring.ci_score import score_title

st.set_page_config(page_title="Second-Hand Price Intelligence", layout="centered")
st.title("Second-Hand Price Intelligence")
st.write("Enter a listing title to get a condition score and price estimate.")

@st.cache_data
def load_latest_csv():
    data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
    csv_files = glob.glob(os.path.join(data_folder, "*.csv"))
    
    if csv_files:
        latest = max(csv_files, key=os.path.getmtime)
        return pd.read_csv(latest)
    
    fallback = os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_listings.csv")
    if os.path.exists(fallback):
        return pd.read_csv(fallback)
    
    return None

df = load_latest_csv()

user_input = st.text_input("Listing title", placeholder="e.g. Sony WH-1000XM4 like new, all accessories")

analyse_clicked = st.button("Analyse")


if analyse_clicked and user_input.strip():
    result = score_title(user_input)

    st.subheader(f"CI Score: {result['score']} / 100 — Grade {result['grade']}")

    if result['matched']:
        st.write("**Signals detected:**")
        for keyword, delta in result['matched']:
            sign = "+" if delta > 0 else ""
            st.write(f"  {'✓' if delta > 0 else '✗'}  {keyword}  ({sign}{delta})")
    else:
        st.write("No condition signals detected in title. Defaulting to Grade C.")

    if df is not None:
        grade = result['grade']
        filtered = df[df['title'].apply(lambda t: score_title(str(t))['grade'] == grade)]

        if len(filtered) < 10:
            filtered = df

        low = filtered['price_usd'].quantile(0.25)
        mid = filtered['price_usd'].quantile(0.50)
        high = filtered['price_usd'].quantile(0.75)

        st.subheader("Price Range")
        st.write(f"Based on **{len(filtered)} listings** with similar condition (Grade {grade})")
        st.write(f"- Low end:  ${low:.2f}")
        st.write(f"- Median:   ${mid:.2f}")
        st.write(f"- High end: ${high:.2f}")
    else:
        st.warning("No CSV data found. Run the scraper first.")

elif analyse_clicked and not user_input.strip():
    st.warning("Please enter a listing title first.")