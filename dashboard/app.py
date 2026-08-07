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