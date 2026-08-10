# Job Market Intelligence Dashboard

An AI-powered tool that analyzes real data analyst and data scientist job postings to uncover in-demand skills, salary trends, and personalized career insights.

🔗 **[Live Dashboard](https://job-market-intelligence-data-maneeshraja.streamlit.app/)**

## Data Freshness
This dashboard's data is automatically refreshed daily via a scheduled GitHub Actions workflow, 
which pulls fresh postings from Adzuna and RemoteOK, cleans them, and updates the dataset that powers the live dashboard.
**Quick finding:** Postings mentioning Machine Learning show an $18,475 average salary premium over those that don't (based on analysis of 740 real job postings). [See full insights ↓](#key-insights-from-740-analyzed-job-postings)

## Why this project?
While job hunting, I found it hard to know exactly which skills to prioritize and what salary to expect. So I built this tool to pull real job postings, analyze them with NLP and machine learning, and turn them into clear, actionable insights — for myself and anyone else navigating the job market.

**Progress so far:**
- ✅ Project structure set up
- ✅ Adzuna API connected and returning live job posting data
- Data cleaning
- NLP skill extraction
- Salary prediction model
- Dashboard

## Current Features

- Automated daily job posting collection using Adzuna API
- NLP-based skill extraction from job descriptions
- Salary prediction model
- Semantic skill clustering
- Interactive Streamlit dashboard
- AI-generated job market insights
- Automated data pipeline using GitHub Actions

## Future Improvements

- Expand job data sources beyond Adzuna
- Improve NLP-based skill extraction with advanced language models
- Enhance salary prediction accuracy with additional features
- Add historical job-market trend analysis
- Add advanced job recommendation and skill-gap analysis
- Improve real-time monitoring and alerting capabilities

## Tech Stack
Python, pandas, scikit-learn, spaCy, sentence-transformers, Streamlit

## Data Sources
- **Adzuna API** — real-time job postings (title, company, location, salary, description)
- **RemoteOK API** *(coming soon)* — remote-specific job postings

## Sample Data
The first batch of collected job postings (300 real listings for Data Analyst and Data Scientist roles) is available in `data/raw/adzuna_jobs_raw.csv`.

## How to Run This Project (so far)
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your own Adzuna API credentials:
4. Data collection notebook: see `notebooks/01_data_collection.ipynb` *(coming soon — will be added from Colab)*

## Methodology & Known Limitations
- Skills are extracted via keyword matching against a curated list of 43 common data-role skills, searched across job title, description snippet, and category.
- Adzuna's API provides only partial job description text (not full postings), which may undercount skills that appear later in the full listing.
- Some companies post near-identical job descriptions across multiple locations; these are kept as separate rows (since location/salary differ) but can inflate specific skill counts for those employers.
- Skill counts should be read as directional signal (what's mentioned across available text), not a precise measure of true market-wide demand.

## Key Insights (from 740 analyzed job postings)

- **Machine Learning** shows the strongest salary association: postings mentioning it average **$18,475 higher** salary_min than those that don't (based on 96 postings).
- **Python** also shows a positive association (**+$15,977**), though based on a smaller sample (16 postings).
- **SQL**, despite being widely required (42 postings), shows a slight **negative** association (-$10,154) — likely because it's a near-universal baseline skill across both junior and senior roles rather than a differentiator for higher pay.
- **Business Analyst** postings emphasize Agile and Communication over technical tools, while **Data Analyst** postings lean heavily on SQL, Python, and Power BI — reflecting a more technical vs. process-oriented role split.
- Smaller sample sizes (Tableau, Power BI, AWS — each under 15 postings) mean their salary associations should be treated as directional, not conclusive.

*See `data/processed/salary_by_skill.csv` and `data/processed/skills_by_role.csv` for full data.*