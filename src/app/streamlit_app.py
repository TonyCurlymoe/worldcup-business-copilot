import os

import httpx
import pandas as pd
import plotly.express as px
import streamlit as st

API_BASE_URL = os.getenv("FRONTEND_API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="World Cup BI Copilot", page_icon="⚽", layout="wide")
st.title("⚽ World Cup Business Intelligence Copilot")
st.caption("AI-assisted football, sponsorship, and market intelligence for World Cup decision makers.")


@st.cache_data(ttl=60)
def get_dashboard() -> dict:
    with httpx.Client(timeout=10) as client:
        response = client.get(f"{API_BASE_URL}/dashboard")
        response.raise_for_status()
        return response.json()


try:
    dashboard = get_dashboard()
except Exception as exc:  # Streamlit UI boundary
    st.error(f"Unable to load API dashboard data: {exc}")
    st.stop()

teams = pd.DataFrame(dashboard["teams"])
matches = pd.DataFrame(dashboard["matches"])

score_col, reach_col, sponsor_col = st.columns(3)
score_col.metric("Top Business Value Score", f"{teams['business_value_score'].max():.1f}")
reach_col.metric("Total Social Reach", f"{teams['social_reach_millions'].sum():.0f}M")
sponsor_col.metric("Sponsor Portfolio", f"${teams['sponsor_portfolio_value_musd'].sum():.0f}M")

left, right = st.columns([2, 1])
with left:
    st.subheader("Team Business Value Score")
    st.plotly_chart(px.bar(teams.sort_values("business_value_score"), x="business_value_score", y="team", orientation="h", color="marketability_index", labels={"business_value_score": "Score", "team": "Team"}), use_container_width=True)
with right:
    st.subheader("Upcoming Commercial Moments")
    st.dataframe(matches, use_container_width=True, hide_index=True)

st.subheader("Marketability vs Sponsor Portfolio")
st.plotly_chart(px.scatter(teams, x="marketability_index", y="sponsor_portfolio_value_musd", size="social_reach_millions", color="team", hover_name="team"), use_container_width=True)

analysis_tab, sponsor_tab, news_tab = st.tabs(["AI Match Analysis", "Sponsor Impact", "News RAG"])
with analysis_tab:
    home = st.selectbox("Home team", teams["team"], key="home")
    away = st.selectbox("Away team", teams["team"], index=1, key="away")
    context = st.text_area("Business context", "Assess broadcast demand, sponsor exposure, and fan engagement.")
    if st.button("Analyze match"):
        result = httpx.post(f"{API_BASE_URL}/analysis/match", json={"home_team": home, "away_team": away, "context": context}, timeout=30).json()
        st.write(result["summary"])
        st.write("Risks", result["risks"])
        st.write("Opportunities", result["opportunities"])
with sponsor_tab:
    sponsor = st.text_input("Sponsor", "Global Sportswear Co")
    team = st.selectbox("Team", teams["team"], key="sponsor_team")
    budget = st.number_input("Campaign budget ($M)", min_value=0.1, value=25.0)
    if st.button("Analyze sponsor impact"):
        result = httpx.post(f"{API_BASE_URL}/analysis/sponsor", json={"sponsor": sponsor, "team": team, "campaign_budget_musd": budget}, timeout=30).json()
        st.write(result["summary"])
        st.write("Risks", result["risks"])
        st.write("Opportunities", result["opportunities"])
with news_tab:
    query = st.text_input("News query", "World Cup sponsors business")
    if st.button("Retrieve news"):
        articles = httpx.get(f"{API_BASE_URL}/news", params={"query": query}, timeout=20).json()
        for article in articles:
            st.markdown(f"**[{article['title']}]({article['url']})** — {article['source']}")
            st.write(article["summary"])
