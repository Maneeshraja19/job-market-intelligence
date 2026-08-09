"""
Automated data refresh script.
Pulls job postings from Adzuna + RemoteOK, cleans them, extracts skills,
and saves updated CSVs to data/raw/ and data/processed/.
Designed to run locally or via GitHub Actions on a schedule.
"""

import os
import re
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone

# ── Credentials (from environment variables, not hardcoded) ──
APP_ID = os.environ.get("ADZUNA_APP_ID")
APP_KEY = os.environ.get("ADZUNA_APP_KEY")

if not APP_ID or not APP_KEY:
    raise ValueError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY environment variables.")

SKILLS_LIST = [
    'python', 'sql', 'r', 'java', 'scala', 'c++',
    'excel', 'tableau', 'power bi', 'looker', 'qlik',
    'mysql', 'postgresql', 'mongodb', 'snowflake', 'redshift', 'bigquery',
    'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
    'spark', 'hadoop', 'kafka', 'airflow',
    'aws', 'azure', 'gcp', 'google cloud',
    'machine learning', 'deep learning', 'statistics', 'a/b testing',
    'data visualization', 'etl', 'data warehousing', 'nlp',
    'stakeholder management', 'communication', 'agile', 'scrum'
]

KEYWORDS = ["data analyst", "data scientist", "junior data analyst", "business analyst", "data engineer"]


def fetch_adzuna_jobs(keyword, num_pages=3):
    all_jobs = []
    for page in range(1, num_pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"
        params = {
            "app_id": APP_ID, "app_key": APP_KEY,
            "what": keyword, "results_per_page": 50
        }
        response = requests.get(url, params=params, timeout=30)
        if response.status_code != 200:
            print(f"Adzuna error on page {page} for '{keyword}': {response.status_code}")
            break
        data = response.json()
        for job in data.get('results', []):
            all_jobs.append({
                'search_keyword': keyword,
                'title': job.get('title'),
                'company': job.get('company', {}).get('display_name'),
                'location': job.get('location', {}).get('display_name'),
                'salary_min': job.get('salary_min'),
                'salary_max': job.get('salary_max'),
                'category': job.get('category', {}).get('label'),
                'created': job.get('created'),
                'description': job.get('description'),
                'redirect_url': job.get('redirect_url')
            })
    return all_jobs


def fetch_remoteok_jobs():
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"RemoteOK error: {response.status_code}")
        return []
    remote_data = response.json()
    jobs = []
    for job in remote_data[1:]:
        jobs.append({
            'search_keyword': 'remote',
            'title': job.get('position'),
            'company': job.get('company'),
            'location': job.get('location', 'Remote'),
            'salary_min': job.get('salary_min'),
            'salary_max': job.get('salary_max'),
            'category': ', '.join(job.get('tags', [])),
            'created': job.get('date'),
            'description': job.get('description'),
            'redirect_url': job.get('url')
        })
    df = pd.DataFrame(jobs)
    if len(df) == 0:
        return []
    keywords = ['data analyst', 'data scientist', 'data science', 'analytics']
    mask = df['title'].str.lower().str.contains('|'.join(keywords), na=False)
    return df[mask].to_dict('records')


def extract_skills(text, skills_list):
    if pd.isna(text):
        return []
    text_lower = str(text).lower()
    found = []
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return found


def main():
    print(f"Refresh started at {datetime.now(timezone.utc).isoformat()}")

    # ── Collect ──
    all_jobs = []
    for kw in KEYWORDS:
        jobs = fetch_adzuna_jobs(kw, num_pages=3)
        all_jobs.extend(jobs)
        print(f"  {kw}: {len(jobs)} jobs")

    remote_jobs = fetch_remoteok_jobs()
    all_jobs.extend(remote_jobs)
    print(f"  remote: {len(remote_jobs)} jobs")

    df = pd.DataFrame(all_jobs)
    print(f"Total collected: {len(df)}")

    # ── Clean ──
    df = df.drop_duplicates(subset=['title', 'company', 'location', 'description', 'salary_min'], keep='first').copy()
    df['created'] = pd.to_datetime(df['created'], format='mixed', errors='coerce')
    df['salary_min'] = df['salary_min'].replace(0, np.nan)
    df['salary_max'] = df['salary_max'].replace(0, np.nan)
    print(f"After cleaning: {len(df)}")

    # ── Extract skills ──
    df['combined_text'] = (
        df['title'].fillna('') + ' ' + df['description'].fillna('') + ' ' + df['category'].fillna('')
    )
    df['extracted_skills'] = df['combined_text'].apply(lambda t: extract_skills(t, SKILLS_LIST))

    # ── Save ──
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/job_postings_with_skills.csv', index=False)
    print("Saved data/processed/job_postings_with_skills.csv")

    # ── Skill counts summary ──
    from collections import Counter
    all_skills_flat = [s for skills in df['extracted_skills'] for s in skills]
    skill_counts_df = pd.DataFrame(Counter(all_skills_flat).items(), columns=['skill', 'count']).sort_values('count', ascending=False)
    skill_counts_df.to_csv('data/processed/skill_counts.csv', index=False)
    print("Saved data/processed/skill_counts.csv")

    print(f"Refresh completed at {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()