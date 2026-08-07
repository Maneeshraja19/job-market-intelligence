import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Job Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/job_postings_with_skills.csv')
    return df

df = load_data()

# Title
st.title("📊 Job Market Intelligence Dashboard")
st.markdown("Real-time insights into Data Analyst and Data Scientist job postings")

# Key stats row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Postings", len(df))

with col2:
    avg_salary = df['salary_min'].mean()
    st.metric("Avg Salary (Min)", f"${avg_salary:,.0f}")

with col3:
    num_companies = df['company'].nunique()
    st.metric("Companies", num_companies)

with col4:
    num_roles = df['search_keyword'].nunique()
    st.metric("Role Types", num_roles)

st.markdown("---")
st.subheader("Sample of Job Postings")
st.dataframe(df[['title', 'company', 'location', 'salary_min', 'search_keyword']].head(20))
st.markdown("---")
st.subheader("📈 Skill Demand by Role")

# Load skill-by-role data
skills_by_role_df = pd.read_csv('data/processed/skills_by_role.csv')

# Dropdown to select a role
selected_role = st.selectbox("Select a role to see top skills:", skills_by_role_df['role'].unique())

# Filter and display as a bar chart
filtered_skills = skills_by_role_df[skills_by_role_df['role'] == selected_role].sort_values('count', ascending=True)
st.bar_chart(filtered_skills.set_index('skill')['count'])

st.markdown("---")
st.subheader("💰 Salary Impact by Skill")

# Load salary-by-skill data
salary_by_skill_df = pd.read_csv('data/processed/salary_by_skill.csv')
st.bar_chart(salary_by_skill_df.set_index('skill')['difference'])
st.caption("Positive values indicate postings mentioning this skill had higher average salary_min than those that didn't.")