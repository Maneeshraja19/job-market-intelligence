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
st.markdown("---")
st.subheader("🔮 Salary Predictor")
st.markdown("Select a role and skills to get an estimated salary based on our trained model.")

import joblib

# Load the trained model
model = joblib.load('models/salary_model.pkl')

# Get the exact feature columns the model expects
model_features = model.feature_names_in_

col1, col2 = st.columns(2)

with col1:
    predict_role = st.selectbox("Job Role:", ['data analyst', 'data scientist', 'business analyst', 'data engineer', 'junior data analyst'], key='predict_role')

with col2:
    all_skills = ['python', 'sql', 'excel', 'tableau', 'power bi', 'machine learning', 'aws', 'azure', 'r', 'java']
    predict_skills = st.multiselect("Skills mentioned in the job:", all_skills)

if st.button("Predict Salary"):
    # Build a feature row matching the model's expected columns
    input_data = pd.DataFrame(0, index=[0], columns=model_features)
    
    for skill in predict_skills:
        if skill in input_data.columns:
            input_data[skill] = 1
    
    role_col = f'role_{predict_role}'
    if role_col in input_data.columns:
        input_data[role_col] = 1
    
    prediction = model.predict(input_data)[0]
    st.success(f"Estimated Salary: **${prediction:,.0f}**")