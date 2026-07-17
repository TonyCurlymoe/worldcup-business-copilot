import plotly.express as px
import streamlit as st

from .analytics import generate_business_summary, identify_strengths
from .config import settings
from .data import (
    get_team_profile, 
    load_historical_world_cup_data,
    load_team_data,
)
from .llm import (
    answer_business_question_with_ai, 
    generate_ai_report,
)

from src.worldcup_business_copilot.src.worldcup_api import fetch_worldcup_matches


def main() -> None:
    st.set_page_config(page_title="World Cup Business Intelligence Copilot", layout="wide")

    st.title("World Cup Business Intelligence Copilot")
    st.write("A real-time-style dashboard for World Cup team performance and business value.")

    df = load_team_data(settings.data_path)
    matches_df = fetch_worldcup_matches()
    historical_df = load_historical_world_cup_data(
        settings.historical_data_path
    )

    st.sidebar.header("Dashboard Filters")

    region_options = sorted(df["region"].unique().tolist())

    selected_regions = st.sidebar.multiselect(
        "Region",
        options=region_options,
        default=region_options,
    )

    minimum_business_value = st.sidebar.slider(
        "Minimum Business Value",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
    )

    filtered_df = df[
        (df["region"].isin(selected_regions))
        & (df["business_value_score"] >= minimum_business_value)
    ].copy()

    ranked_df = filtered_df.sort_values(
        "business_value_score",
        ascending=False,
    )

    if ranked_df.empty:
        st.warning("No teams match the selected filters.")
        st.stop()

    filtered_team_names = set(ranked_df["team"].tolist())

    filtered_matches_df = matches_df[
        matches_df["team_a"].isin(filtered_team_names)
        | matches_df["team_b"].isin(filtered_team_names)
    ].copy()

    total_teams = len(ranked_df)
    total_matches = len(filtered_matches_df)
    average_business_value = ranked_df["business_value_score"].mean()
    average_advancement = ranked_df["advancement_probability"].mean()

    st.subheader("Executive Overview")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Teams", total_teams)
    kpi2.metric("Matches", total_matches)
    kpi3.metric("Avg. Business Value", f"{average_business_value:.1f}")
    kpi4.metric("Avg. Advancement Probability", f"{average_advancement:.1f}%")

    st.subheader("Business Opportunities")

    top_sponsor_team = ranked_df.loc[
        ranked_df["sponsor_exposure"].idxmax()
    ]

    top_star_team = ranked_df.loc[
        ranked_df["star_power"].idxmax()
    ]

    top_social_team = ranked_df.loc[
        ranked_df["social_media_heat"].idxmax()
    ]

    opportunity_col1, opportunity_col2, opportunity_col3 = st.columns(3)

    with opportunity_col1:
        st.metric(
            "Highest Sponsor Exposure",
            top_sponsor_team["team"],
            f"{top_sponsor_team['sponsor_exposure']}",
        )

    with opportunity_col2:
        st.metric(
            "Highest Star Power",
            top_star_team["team"],
            f"{top_star_team['star_power']}",
        )

    with opportunity_col3:
        st.metric(
            "Highest Social Media Heat",
            top_social_team["team"],
            f"{top_social_team['social_media_heat']}",
        )

    st.subheader("Historical World Cup Analytics")

    historical_years = sorted(
        historical_df["year"].unique().tolist(),
        reverse=True,
    )

    selected_history_year = st.selectbox(
        "Select Tournament Year",
        options=historical_years,
        key="historical_year",
    )

    selected_final = historical_df[
        historical_df["year"] == selected_history_year
    ].iloc[0]

    history_col1, history_col2, history_col3 = st.columns(3)

    history_col1.metric(
        "Champion",
        selected_final["winner"],
    )

    history_col2.metric(
        "Final Match",
        f"{selected_final['team_a']} vs {selected_final['team_b']}",
    )

    history_col3.metric(
        "Final Score",
        f"{selected_final['score_a']}-{selected_final['score_b']}",
    )

    if selected_final["score_a"] == selected_final["score_b"]:
        st.caption(
            "The final finished level, and the champion was decided "
            "by a penalty shootout."
        )

    st.markdown("#### Champion History")

    historical_df["winner_normalized"] = historical_df["winner"].replace(
        {
            "West Germany": "Germany",
        }
    )

    champion_counts = (
        historical_df["winner_normalized"]
        .value_counts()
        .rename_axis("team")
        .reset_index(name="championships")
    )

    champion_chart = px.bar(
        champion_counts,
        x="team",
        y="championships",
        text="championships",
        title="World Cup Titles in Loaded Historical Data",
        labels={
            "team": "National Team",
            "championships": "Championships",
        },
    )

    champion_chart.update_traces(textposition="outside")

    champion_chart.update_layout(
        yaxis=dict(
            tickmode="linear",
            dtick=1,
        )
    )

    st.plotly_chart(
        champion_chart,
        width="stretch",
    )

    st.markdown("#### Tournament Timeline")

    timeline_df = historical_df.copy()

    timeline_df["champion"] = timeline_df["winner"].replace(
        {
            "West Germany": "Germany",
        }
    )

    timeline_df = timeline_df.sort_values("year")

    timeline_chart = px.scatter(
        timeline_df,
        x="year",
        y="champion",
        text="champion",
        title="World Cup Champions by Tournament Year",
        labels={
            "year": "Tournament Year",
            "champion": "Champion",
        },
    )

    timeline_chart.update_traces(
        textposition="top center",
        marker=dict(size=12),
    )

    timeline_chart.update_layout(
        xaxis=dict(
            tickmode="linear",
            dtick=4,
        ),
        showlegend=False,
    )

    st.plotly_chart(
        timeline_chart,
        width="stretch",
    )

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

    if filtered_matches_df.empty:
        st.warning("No match data available for the selected teams.")
    else:
        st.dataframe(
            filtered_matches_df, 
            use_container_width=True, 
            hide_index=True
        )

        st.markdown("### Match Center")

        groups = ["All Groups"] + sorted(
            filtered_matches_df["stage"].unique().tolist()
        )
        selected_group = st.selectbox("Filter by group", groups)

        if selected_group == "All Groups":
            filtered_matches = filtered_matches_df
        else:
            filtered_matches = filtered_matches_df[
                filtered_matches_df["stage"] == selected_group
            ]


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

    st.subheader("Team Comparison")

    team_names = ranked_df["team"].tolist()

    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        team_a_name = st.selectbox(
            "Select Team A",
            team_names,
            index=0,
            key="compare_team_a",
        )

    with compare_col2:
        default_b_index = 1 if len(team_names) > 1 else 0
        team_b_name = st.selectbox(
            "Select Team B",
            team_names,
            index=default_b_index,
            key="compare_team_b",
        )

    team_a_data = get_team_profile(df, team_a_name)
    team_b_data = get_team_profile(df, team_b_name)

    comparison_metrics = [
        "business_value_score",
        "market_size",
        "star_power",
        "social_media_heat",
        "sponsor_exposure",
        "performance_score",
        "advancement_probability",
    ]

    comparison_df = ranked_df[
        ranked_df["team"].isin([team_a_name, team_b_name])
    ][["team"] + comparison_metrics]

    comparison_long = comparison_df.melt(
        id_vars="team",
        value_vars=comparison_metrics,
        var_name="metric",
        value_name="score",
    )

    comparison_chart = px.bar(
        comparison_long,
        x="metric",
        y="score",
        color="team",
        barmode="group",
        title=f"{team_a_name} vs {team_b_name}",
    )

    st.plotly_chart(comparison_chart, use_container_width=True)

    if team_a_data["business_value_score"] > team_b_data["business_value_score"]:
        stronger_team = team_a_name
    elif team_b_data["business_value_score"] > team_a_data["business_value_score"]:
        stronger_team = team_b_name
    else:
        stronger_team = "Both teams"

    st.info(
        f"{stronger_team} currently has the stronger overall business value "
        f"based on the selected metrics."
    )

    selected_team = st.selectbox("Select a team", ranked_df["team"].tolist())
    team = get_team_profile(df, selected_team)

    st.subheader(f"{selected_team} Business Profile")
    col1, col2, col3 = st.columns(3)
    col1.metric("Business Value Score", f"{team['business_value_score']:.1f}")
    col2.metric("Sponsor Exposure", f"{team['sponsor_exposure']}")
    col3.metric("Advancement Probability", f"{team['advancement_probability']}%")

    st.write(generate_business_summary(team))
    st.write("**Top strengths:** " + ", ".join(identify_strengths(team)))

    st.subheader("Business Insights")

    insight_items = []

    if team["star_power"] >= 90:
        insight_items.append(
            f"{selected_team} has elite star power and strong global endorsement potential."
        )
    elif team["star_power"] >= 80:
        insight_items.append(
            f"{selected_team} has solid star power with regional marketing potential."
        )
    else:
        insight_items.append(
            f"{selected_team} may need stronger player branding to improve global visibility."
        )

    if team["sponsor_exposure"] >= 90:
        insight_items.append(
            "The team is highly attractive to major sponsors and international brands."
        )
    elif team["sponsor_exposure"] >= 80:
        insight_items.append(
            "The team offers moderate-to-strong sponsorship opportunities."
        )
    else:
        insight_items.append(
            "Sponsorship exposure is currently below the leading teams."
        )

    if team["social_media_heat"] >= 90:
        insight_items.append(
            "Strong social media interest creates opportunities for digital campaigns."
        )
    elif team["social_media_heat"] >= 80:
        insight_items.append(
            "Social media engagement is healthy but still has room to grow."
        )
    else:
        insight_items.append(
            "Digital engagement should be a priority for future marketing activity."
        )

    if team["advancement_probability"] >= 80:
        risk_level = "Low"
    elif team["advancement_probability"] >= 65:
        risk_level = "Medium"
    else:
        risk_level = "High"

    if team["market_size"] >= 90:
        recommended_sectors = [
            "Global consumer brands",
            "Financial services",
            "Airlines and travel",
        ]
    elif team["social_media_heat"] >= 90:
        recommended_sectors = [
            "Technology",
            "Gaming",
            "Digital media",
        ]
    else:
        recommended_sectors = [
            "Regional retail",
            "Sportswear",
            "Local media",
        ]

    for item in insight_items:
        st.markdown(f"- {item}")

    st.markdown(
        "**Recommended sponsorship sectors:** "
        + ", ".join(recommended_sectors)
    )

    st.markdown(f"**Commercial risk level:** {risk_level}")

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

    report_button = st.button(
        "Generate Business Report (Offline)",
        width="stretch",
        key="generate_business_report",
    )

    if report_button:
        st.session_state["business_report"] = generate_ai_report(team)
        st.session_state["business_report_team"] = selected_team

    report_is_current = (
        st.session_state.get("business_report_team") == selected_team
        and "business_report" in st.session_state
    )

    if report_is_current:
        report = st.session_state["business_report"]

        st.divider()
        st.markdown(report)

        st.download_button(
            label="Download Report as Markdown",
            data=report,
            file_name=(
                f"{selected_team.lower().replace(' ', '_')}"
                "_business_report.md"
            ),
            mime="text/markdown",
            width="stretch",
            key=f"download_{selected_team}",
            on_click="ignore",
        )


    st.divider()
    st.subheader("Ask Business Copilot")

    chat_state_key = f"copilot_messages_{selected_team}"

    _, chat_header_col2 = st.columns([4, 1])

    with chat_header_col2:
        clear_chat = st.button(
            "Clear Chat",
            key=f"clear_chat_{selected_team}",
            width="stretch",
        )

    if clear_chat:
        st.session_state[chat_state_key] = []
        st.rerun()

    st.caption(
        "Offline mode: answers are generated from the selected team's "
        "dashboard metrics and predefined business rules."
    )

    st.markdown("#### Suggested Questions")

    suggested_questions = [
        f"Should Adidas sponsor {selected_team}?",
        f"What are {selected_team}'s biggest commercial risks?",
        f"How valuable is {selected_team}?",
        f"What are {selected_team}'s strongest advantages?",
        f"How should {selected_team} improve fan engagement?",
    ]

    suggestion_cols = st.columns(2)

    for index, suggestion in enumerate(suggested_questions):
        column = suggestion_cols[index % 2]

        with column:
            if st.button(
                suggestion,
                key=f"suggestion_{selected_team}_{index}",
                width="stretch",
            ):
                st.session_state[
                    f"pending_question_{selected_team}"
                ] = suggestion

    if chat_state_key not in st.session_state:
        st.session_state[chat_state_key] = []

    for message in st.session_state[chat_state_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed_question = st.chat_input(
        f"Ask a business question about {selected_team}",
        key=f"chat_input_{selected_team}",
    )

    pending_question_key = f"pending_question_{selected_team}"

    suggested_question = st.session_state.pop(
        pending_question_key,
        None,
    )

    user_question = typed_question or suggested_question

    if user_question:
        st.session_state[chat_state_key].append(
            {
                "role": "user",
                "content": user_question,
            }
        )

        answer, answer_mode = answer_business_question_with_ai(
            team,
            user_question
        )

        st.session_state[chat_state_key].append(
            {
                "role": "assistant",
                "content": answer,
                "mode": answer_mode,
            }
        )

        st.rerun()

if __name__ == "__main__":
    main()