# Job Market Intelligence Dashboard

An AI-powered tool that analyzes real data analyst and data scientist job postings to uncover in-demand skills, salary trends, and personalized career insights.

## Why this project?
While job hunting, I found it hard to know exactly which skills to prioritize and what salary to expect. So I built this tool to pull real job postings, analyze them with NLP and machine learning, and turn them into clear, actionable insights — for myself and anyone else navigating the job market.

## Status
## Status
🚧 Work in progress — actively being built.

**Progress so far:**
- ✅ Project structure set up
- ✅ Adzuna API connected and returning live job posting data
- Data cleaning
- NLP skill extraction
- Salary prediction model
- Dashboard

## Planned Features
- Real-time job posting collection (Adzuna + RemoteOK APIs)
- NLP-based skill extraction from job descriptions
- Salary prediction model
- Semantic skill clustering
- Interactive dashboard (Streamlit)
- AI-generated market insights

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