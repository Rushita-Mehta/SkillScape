import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px

from recommendation_engine import load_data, calculate_skill_gaps

# A simple catalog of real courses for each skill
TRAINING_CATALOG = {
    "Python": [
        "Python for Everybody (Coursera)",
        "The Complete Python Bootcamp (Udemy)"
    ],
    "Market Analysis": [
        "Market Research and Consumer Behavior (Coursera)",
        "Business Analytics Specialization (Coursera)"
    ],
    "Data Visualization": [
        "Data Visualization with Tableau (Udacity)",
        "Interactive Data Visualization with Python (Udemy)"
    ],
    "Statistics": [
        "Statistics with R (Coursera)",
        "Intro to Statistical Learning (edX)"
    ],
    # … add more mappings as needed …
}

@st.cache_data
def load_all_data():
    # Load base data
    employees, role_reqs = load_data()
    # Compute skill gaps
    recs = calculate_skill_gaps(employees, role_reqs)
    # Map each skill to real learning resources
    def lookup(skill):
        return TRAINING_CATALOG.get(skill, [f"Search LinkedIn Learning for {skill}"])
    recs["LearningResources"] = recs["Skill"].map(
        lambda s: "\n".join(f"- {c}" for c in lookup(s))
    )
    return employees, role_reqs, recs

def safe_avg(df: pd.DataFrame, skill: str) -> float:
    """Return a valid average (0.0 if missing or NaN) for df[skill]."""
    if df.empty or skill not in df.columns:
        return 0.0
    vals = df[skill].fillna(0)
    m = vals.mean()
    return 0.0 if (not isinstance(m, (int, float)) or math.isnan(m)) else m

def safe_max_req(role_reqs: pd.DataFrame, skill: str) -> int:
    """Return required proficiency or 0 if undefined."""
    sub = role_reqs[role_reqs["Skill"] == skill]
    if sub.empty:
        return 0
    m = sub["RequiredProficiency"].max()
    return int(m) if not math.isnan(m) else 0

def main():
    st.title("Strategic Talent Advisory Dashboard")

    # 1) Load all data
    employees, role_reqs, recommendations = load_all_data()

    # 2) Employee Overview
    st.header("1. Employee Overview")
    st.write(
        "This table shows each employee’s role and current skill levels. "
        "Verify your source data before diving into gaps."
    )
    st.dataframe(employees)

    # 3) Skill Gaps & Learning Resources
    st.header("2. Skill Gaps & Learning Resources")
    st.write(
        "**What you see:** Each row is a skill gap (Current vs Required) for an employee.\n\n"
        "**Why it helps:** Direct links to real courses make it easy to assign targeted upskilling."
    )
    st.dataframe(
        recommendations[
            ["EmployeeID", "Name", "Role", "Skill", "Gap", "LearningResources"]
        ],
        use_container_width=True
    )

    # Sidebar: choose a role
    st.sidebar.header("Role-Specific Deep Dive")
    roles = sorted(employees["Role"].unique())
    selected_role = st.sidebar.selectbox("Select a Role", roles)

    # Filter for that role
    df_emp = employees[employees["Role"] == selected_role]
    reqs = role_reqs[role_reqs["Role"] == selected_role]

    # 4) Skill Tower
    st.header("3. Skill Tower")
    st.write(
        "**Question answered:** Which skills have the largest team-wide gaps?\n\n"
        "- **Blue blocks** = team’s average proficiency\n"
        "- **Gray blocks** = points missing to hit the required level\n\n"
        "Target the tallest gray bars first for greatest impact."
    )
    if not reqs.empty:
        tower_rows = []
        for _, r in reqs.iterrows():
            skill = r["Skill"]
            required = r["RequiredProficiency"]
            avg = safe_avg(df_emp, skill)
            filled = int(round(avg))
            missing = max(required - filled, 0)
            tower_rows.append({"Skill": skill, "Filled": filled, "Missing": missing})
        tower_df = pd.DataFrame(tower_rows)

        fig1 = px.bar(
            tower_df,
            x="Skill", y=["Filled", "Missing"],
            title=f"Skill Tower: {selected_role}",
            labels={"value":"Blocks (1 pt)", "variable":""},
            color_discrete_map={"Filled":"#1f77b4","Missing":"#d3d3d3"}
        )
        fig1.update_yaxes(dtick=1, gridcolor="white")
        fig1.update_layout(plot_bgcolor="#eaeff2", legend_title_text="")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No skill requirements defined for this role.")
        tower_df = pd.DataFrame(columns=["Skill","Filled","Missing"])

    # 5) Build Your Dream Team
    st.header("4. Build Your Dream Team")
    st.write(
        "**Which skills should we focus on first?**\n\n"
        "- We’ve pre-selected the **top 5 skills** where gaps are largest.\n"
        "- You can add or remove skills; the chart will update current vs. needed blocks.\n\n"
        "- **Green bars** = current average proficiency\n"
        "- **Orange bars** = additional blocks needed to reach target"
    )

    all_skills = sorted(reqs["Skill"].unique())
    # Determine top5 by descending gap
    top5 = tower_df.sort_values("Missing", ascending=False)["Skill"].tolist()[:5]
    # Pre-select top5 (only those that exist in reqs)
    defaults = [s for s in top5 if s in all_skills]

    chosen = st.multiselect(
        "Skills to include in your Dream Team:",
        options=all_skills,
        default=defaults
    )

    # Persist target settings
    if "targets" not in st.session_state:
        st.session_state.targets = {}
    for sk in chosen:
        st.session_state.targets.setdefault(sk, safe_max_req(reqs, sk))

    # Interactive Build Mode
    if st.checkbox("Enable Interactive Build Mode") and chosen:
        st.write("Click ➖/➕ to fine-tune each skill’s target blocks:")
        for sk in chosen:
            max_req = safe_max_req(reqs, sk)
            c1, c2, c3 = st.columns([2,1,2])
            with c1:
                st.write(sk)
            with c2:
                if st.button("➖", key=f"minus_{sk}"):
                    st.session_state.targets[sk] = max(0, st.session_state.targets[sk] - 1)
                if st.button("➕", key=f"plus_{sk}"):
                    st.session_state.targets[sk] = min(max_req, st.session_state.targets[sk] + 1)
            with c3:
                st.write(f"Target: {st.session_state.targets[sk]}")

    # Render the Dream Team chart
    if chosen:
        dream_rows = []
        for sk in chosen:
            target = st.session_state.targets[sk]
            curr = int(round(safe_avg(df_emp, sk)))
            gap = max(target - curr, 0)
            dream_rows.append({"Skill": sk, "Current": curr, "Build Gap": gap})
        dream_df = pd.DataFrame(dream_rows)

        fig2 = px.bar(
            dream_df,
            x="Skill", y=["Current", "Build Gap"],
            title="Dream Team Blocks",
            labels={"value":"Blocks", "variable":""},
            color_discrete_map={"Current":"#4CAF50","Build Gap":"#FF9800"}
        )
        fig2.update_yaxes(dtick=1, gridcolor="white")
        fig2.update_layout(plot_bgcolor="#eaeff2", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

        total_needed = int(dream_df["Build Gap"].sum())
        st.write(f"**Total additional blocks needed:** {total_needed}")
    else:
        st.info("Select at least one skill to start planning your Dream Team.")

    # 6) Dynamic Consultative Insights
    st.header("5. Dynamic Consultative Insights")
    st.write(
        "**Next steps based on your gap and target analyses:**\n\n"
        "- Which skills to tackle first\n"
        "- Whether to train internally or hire externally\n"
        "- Suggested timeline and milestones"
    )
    if tower_df.empty:
        st.info("No data available to generate insights.")
    else:
        avg_gap = tower_df["Missing"].mean()
        st.subheader("Overall Gap Snapshot")
        st.write(f"- **Average gap**: **{avg_gap:.2f}** points across all skills.")

        st.subheader("Top Priority Skills")
        top3 = tower_df.sort_values("Missing", ascending=False).head(3)
        for _, r in top3.iterrows():
            sk, miss = r["Skill"], r["Missing"]
            advice = (
                "Run a short internal training sprint." if miss <= 2
                else "Launch external hiring alongside training."
            )
            st.write(f"- **{sk}**: missing {miss} pt(s). {advice}")

        st.subheader("Action Plan")
        st.write(
            "1. Kick off training for skills with gaps ≤2 points; assign mentors.\n"
            "2. Open hiring for skills with gaps >2 points to speed up capacity build.\n"
            "3. Reassess in 3 months and adjust targets as needed."
        )

if __name__ == "__main__":
    main()
