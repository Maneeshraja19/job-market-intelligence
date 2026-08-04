# Data Dictionary

Describes the columns used across raw and processed job posting datasets.

| Column | Type | Description |
|---|---|---|
| search_keyword | text | The search term used to find this job posting |
| title | text | Job title as posted |
| company | text | Hiring company name |
| location | text | Job location |
| salary_min | number | Minimum estimated/stated salary (missing values = not provided) |
| salary_max | number | Maximum estimated/stated salary (missing values = not provided) |
| category | text | Job category as classified by the source (e.g., "IT Jobs") |
| created | datetime | Date/time the job was posted |
| description | text | Job description snippet (Adzuna only provides partial descriptions, not full text) |
| redirect_url | text | Link to the original job posting |
| extracted_skills | list | Skills detected from title, description, and category text |