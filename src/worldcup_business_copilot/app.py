import plotly.express as px
import streamlit as st

from .analytics import generate_business_summary, identify_strengths
from .config import settings
from .data import get_team_profile, load_team_data
from .llm import generate_ai_report
from src.worldcup_business_copilot.src.worldcup_api import fetch_worldcup_matches


def main() -> None:
    st.set_page_config(page_title="World Cup Business Intelligence Copilot", layout="wide")

    st.title("World Cup Business Intelligence Copilot")
    st.write("A real-time-style dashboard for World Cup team performance and business value.")

    df = load_team_data(settings.data_path)
    ranked_df = df.sort_values("business_value_score", ascending=False)

    st.subheader("Team Business Value Ranking")
    st.dataframe(ranked_df, use_container_width=True, hide_index=True)

    fig = px.bar(
        ranked_df,
        x="team",
        y="business_value_score",
        hover_data=["region", "recent_result"],
        title="World Cup Team Business Value Score",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent World Cup Match Results")
    matches_df = fetch_worldcup_matches()

    if matches_df.empty:
        st.warning("No match data available.")
    else:
        st.dataframe(matches_df, use_container_width=True, hide_index=True)

        st.markdown("### Match Center")

        groups = ["All Groups"] + sorted(matches_df["stage"].unique().tolist())
        selected_group = st.selectbox("Filter by group", groups)

        if selected_group == "All Groups":
            filtered_matches = matches_df
        else:
            filtered_matches = matches_df[matches_df["stage"] == selected_group]


        for _, match in filtered_matches.iterrows():
            team_a = match["team_a"]
            team_b = match["team_b"]
            winner = match["winner"]

            if team_a == winner:
                team_a_display = f"🏆 {team_a}"
                team_b_display = team_b
            elif team_b == winner:
                team_a_display = team_a
                team_b_display = f"🏆 {team_b}"
            else:
                team_a_display = team_a
                team_b_display = team_b

            col1, col2, col3 = st.columns([2, 1, 2])

            with col1:
                st.markdown(f"**{team_a_display}**")

            with col2:
                st.markdown(
                    f"<h3 style='text-align:center;'>{match['score']}</h3>",
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(f"**{team_b_display}**")

            st.caption(f"{match['stage']} · Winner: {match['winner']} · Date: {match['date']}")
            st.divider()

    selected_team = st.selectbox("Select a team", ranked_df["team"].tolist())
    team = get_team_profile(df, selected_team)

    st.subheader(f"{selected_team} Business Profile")
    col1, col2, col3 = st.columns(3)
    col1.metric("Business Value Score", f"{team['business_value_score']:.1f}")
    col2.metric("Sponsor Exposure", f"{team['sponsor_exposure']}")
    col3.metric("Advancement Probability", f"{team['advancement_probability']}%")

    st.write(generate_business_summary(team))
    st.write("**Top strengths:** " + ", ".join(identify_strengths(team)))

    radar_df = ranked_df[ranked_df["team"] == selected_team].melt(
        id_vars="team",
        value_vars=[
            "market_size",
            "star_power",
            "social_media_heat",
            "sponsor_exposure",
            "performance_score",
            "advancement_probability",
        ],
        var_name="metric",
        value_name="score",
    )

    radar = px.line_polar(
        radar_df,
        r="score",
        theta="metric",
        line_close=True,
        title=f"{selected_team} Value Drivers",
    )
    st.plotly_chart(radar, use_container_width=True)

    if st.button("Generate AI Business Report"):
        with st.spinner("Generating report..."):
            st.markdown(generate_ai_report(team))


if __name__ == "__main__":
    main()