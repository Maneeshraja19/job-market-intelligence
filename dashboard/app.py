import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, timezone, timedelta

# ── Page config ──
st.set_page_config(
    page_title="Job Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Load data ──
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/job_postings_with_skills.csv')
    return df

@st.cache_data
def load_skills_by_role():
    return pd.read_csv('data/processed/skills_by_role.csv')

@st.cache_data
def load_salary_by_skill():
    return pd.read_csv('data/processed/salary_by_skill.csv')

@st.cache_resource
def load_model():
    return joblib.load('models/salary_model.pkl')

df = load_data()
skills_by_role_df = load_skills_by_role()
salary_by_skill_df = load_salary_by_skill()
model = load_model()

# ── Sidebar navigation ──
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to:", ["Overview", "Skill Insights", "Salary Predictor", "Browse Jobs"])

st.sidebar.markdown("---")
st.sidebar.markdown("**About this project**")
st.sidebar.markdown(
    "Built from real job postings (Adzuna + RemoteOK APIs). "
    "Skills extracted via NLP keyword matching. "
    "Salary predictions powered by a Random Forest model."
)

# ══════════════════════════════════════
# PAGE 1: OVERVIEW
# ══════════════════════════════════════
if page == "Overview":
    st.title("📊 Job Market Intelligence Dashboard")
    st.markdown("Real-time insights into Data Analyst and Data Scientist job postings")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Postings", len(df))
    with col2:
        st.metric("Avg Salary (Min)", f"${df['salary_min'].mean():,.0f}")
    with col3:
        st.metric("Companies", df['company'].nunique())
    with col4:
        st.metric("Role Types", df['search_keyword'].nunique())

    st.markdown("---")

    # Recent postings (last 24 hours)
    st.subheader("🔥 Posted in the Last 24 Hours")
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)
    recent_jobs = df[df['created'] >= cutoff].sort_values('created', ascending=False)

    if len(recent_jobs) > 0:
        st.success(f"{len(recent_jobs)} job(s) posted in the last 24 hours — apply early for less competition!")
        st.dataframe(
            recent_jobs[['title', 'company', 'location', 'salary_min', 'created', 'redirect_url']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No postings found in the last 24 hours in the current dataset. Check back after the next data refresh.")

# ══════════════════════════════════════
# PAGE 2: SKILL INSIGHTS
# ══════════════════════════════════════
elif page == "Skill Insights":
    st.title("📈 Skill Insights")

    st.subheader("Skill Demand by Role")
    selected_role = st.selectbox("Select a role:", skills_by_role_df['role'].unique())
    filtered_skills = skills_by_role_df[skills_by_role_df['role'] == selected_role].sort_values('count', ascending=True)
    st.bar_chart(filtered_skills.set_index('skill')['count'])

    st.markdown("---")

    st.subheader("💰 Salary Impact by Skill")
    st.bar_chart(salary_by_skill_df.set_index('skill')['difference'])
    st.caption("Positive values indicate postings mentioning this skill had higher average salary_min than those that didn't.")

    st.markdown("---")
    st.subheader("📋 Methodology & Limitations")
    st.markdown("""
    - Skills are detected via keyword matching against a curated list of 43 skills, searched across job title, description snippet, and category.
    - Adzuna's API provides only partial description text, which may undercount some skills.
    - Some employers post near-identical listings across multiple locations; these are kept as separate rows since salary/location differ.
    - Skill counts should be read as directional signal, not a precise measure of true market-wide demand.
    """)

# ══════════════════════════════════════
# PAGE 3: SALARY PREDICTOR
# ══════════════════════════════════════
elif page == "Salary Predictor":
    st.title("🔮 Salary Predictor")
    st.markdown("Select a role and skills to get an estimated salary based on our trained Random Forest model.")

    model_features = model.feature_names_in_

    col1, col2 = st.columns(2)
    with col1:
        predict_role = st.selectbox(
            "Job Role:",
            ['data analyst', 'data scientist', 'business analyst', 'data engineer', 'junior data analyst']
        )
    with col2:
        all_skills = sorted([c for c in model_features if not c.startswith('role_')])
        predict_skills = st.multiselect("Skills mentioned in the job:", all_skills)

    if st.button("Predict Salary", type="primary"):
        input_data = pd.DataFrame(0, index=[0], columns=model_features)

        for skill in predict_skills:
            if skill in input_data.columns:
                input_data[skill] = 1

        role_col = f'role_{predict_role}'
        if role_col in input_data.columns:
            input_data[role_col] = 1

        prediction = model.predict(input_data)[0]
        st.success(f"Estimated Salary: **${prediction:,.0f}**")
        st.caption(f"Model performance: R² = 0.407, MAE ≈ $22,816 (Random Forest, trained on {len(df)} postings)")

# ══════════════════════════════════════
# PAGE 4: BROWSE JOBS
# ══════════════════════════════════════
elif page == "Browse Jobs":
    st.title("🔍 Browse Job Postings")

    col1, col2, col3 = st.columns(3)
    with col1:
        role_filter = st.multiselect("Filter by role:", df['search_keyword'].unique())
    with col2:
        min_salary = st.number_input("Minimum salary:", min_value=0, value=0, step=10000)
    with col3:
        search_term = st.text_input("Search title/company:")

    filtered_df = df.copy()

    if role_filter:
        filtered_df = filtered_df[filtered_df['search_keyword'].isin(role_filter)]

    if min_salary > 0:
        filtered_df = filtered_df[filtered_df['salary_min'] >= min_salary]

    if search_term:
        mask = (
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['company'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    st.markdown(f"**{len(filtered_df)} postings match your filters**")
    st.dataframe(
        filtered_df[['title', 'company', 'location', 'salary_min', 'search_keyword', 'redirect_url']],
        use_container_width=True,
        hide_index=True
    )