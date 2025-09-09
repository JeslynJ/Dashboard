import os
from datetime import datetime
import pandas as pd
import streamlit as st

from classify import classify
from preprocess import clean_text, extract_domains
from storage import save_to_csv, save_to_db
from report import generate_report

st.set_page_config(page_title="HarmWatch Live — Social Harm Analyzer", layout="wide")

st.title("HarmWatch Live — Adverse Societal Impact of Social Media")
st.caption("Demo • Rule-based detection • Privacy-aware")

with st.expander("📘 How to use"):
    st.markdown("""
**Steps**
1. Prepare a CSV with at least a **text** column (use the sample in `data/sample_posts.csv`).
2. (Optional) Include **platform, date, author_id, url**.
3. Upload the file or classify live URLs/streams.
    """)

mode = st.sidebar.radio("Choose Mode", ["CSV Upload", "Reports"])

# In-memory store
data = []

def to_df():
    return pd.DataFrame(data)

if mode == "CSV Upload":
    uploaded = st.file_uploader("Upload CSV (min column: text)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        if "text" not in df.columns:
            st.error("CSV must contain a 'text' column.")
            st.stop()

        for col in ["platform","date","author_id","url"]:
            if col not in df.columns:
                df[col] = ""

        # Processing
        df["clean_text"] = df["text"].apply(clean_text)
        df["domains"] = df["text"].apply(extract_domains)

        cats, risks = [], []
        for t, dlist in zip(df["clean_text"], df["domains"]):
            c, r = classify(t, dlist)
            cats.append(c); risks.append(r)
        df["category"], df["risk_level"] = cats, risks

        # Dates
        try:
            df["date_parsed"] = pd.to_datetime(df["date"], errors="coerce")
        except Exception:
            df["date_parsed"] = pd.NaT

        # --- Preview ---
        st.subheader("Preview")
        st.dataframe(df[["text", "category", "risk_level"]].head(30))

        # --- Category Distribution ---
        st.subheader("Category distribution")
        st.bar_chart(df["category"].value_counts())

        # --- Trend over Time ---
        if df["date_parsed"].notna().any():
            st.subheader("Trend over time (by category)")
            temp = df.dropna(subset=["date_parsed"]).copy()
            temp["day"] = temp["date_parsed"].dt.date
            pivot = temp.pivot_table(index="day", columns="category", values="text", aggfunc="count").fillna(0)
            st.line_chart(pivot)

        # --- Flagged Examples ---
        st.subheader("Flagged examples (High & Medium risk)")
        flagged = df[df["risk_level"].isin(["High","Medium"])]
        st.dataframe(flagged[["text", "category", "risk_level"]].head(50))

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Export CSV"):
                os.makedirs("outputs", exist_ok=True)
                path = f"outputs/classified_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(path, index=False)
                st.success(f"Saved to {path}")
        with col2:
            if st.button("🗃️ Save to DB"):
                save_to_db(df)
                st.success("Saved to database")
        with col3:
            if st.button("📄 Generate HTML report"):
                generate_report(df)
                st.success("Report generated as report.html")

elif mode == "Reports":
    st.subheader("Classified Data")
    df = to_df()
    if not df.empty:
        # --- Preview ---
        st.subheader("Preview")
        st.dataframe(df[["text", "category", "risk_level"]].head(30))

        # --- Category Distribution ---
        st.subheader("Category distribution")
        st.bar_chart(df["category"].value_counts())

        # --- Trend over Time ---
        if "date" in df.columns and df["date"].notna().any():
            st.subheader("Trend over time (by category)")
            temp = df.dropna(subset=["date"]).copy()
            temp["day"] = pd.to_datetime(temp["date"], errors="coerce").dt.date
            pivot = temp.pivot_table(index="day", columns="category", values="text", aggfunc="count").fillna(0)
            st.line_chart(pivot)

        # --- Flagged Examples ---
        st.subheader("Flagged examples (High & Medium risk)")
        flagged = df[df["risk_level"].isin(["High","Medium"])]
        st.dataframe(flagged[["text", "category", "risk_level"]].head(50))
    else:
        st.info("No data classified yet.")

st.markdown("---")
st.caption("For research/education • Always respect platform policies & user privacy.")