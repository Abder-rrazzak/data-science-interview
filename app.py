import streamlit as st
from decision_intelligence.data import generate_events
from decision_intelligence.analysis import compare_regions
from decision_intelligence.model import score_anomalies
import plotly.express as px

st.set_page_config(page_title="Decision Intelligence | Synthetic Lab", layout="wide")
st.title("Decision Intelligence — Synthetic Research Lab")
st.caption("All data are simulated. No real-world security assessment is implied.")
rows = st.sidebar.slider("Synthetic observations", 100, 10000, 1000, step=100)
mode = st.sidebar.radio("Presentation mode", ["Executive", "Technical"])
df = generate_events(rows)
summary = compare_regions(df)
scored = score_anomalies(df)
a, b, c = st.columns(3)
a.metric("Observations", f"{len(df):,}")
b.metric("Regions", df.region.nunique())
c.metric("Statistical anomalies", int(scored.is_anomaly.sum()))
st.plotly_chart(px.box(df, x="region", y="measurement", title="Measurements by synthetic region"), use_container_width=True)
if mode == "Technical":
    st.subheader("Welch t-test: North vs South")
    st.json(summary)
    st.dataframe(scored.head(25), use_container_width=True)
else:
    st.info("Synthetic North–South comparison. Association is not causation; validate design and sampling before decisions.")
    st.write(f"Estimated mean difference: {summary['mean_difference']:.2f} (95% CI: {summary['ci95_lower']:.2f}, {summary['ci95_upper']:.2f}).")
st.download_button("Export synthetic observations", df.to_csv(index=False), "synthetic_events.csv", "text/csv")
