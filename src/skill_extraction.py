import re
import pandas as pd

def extract_skills(text, skills_list):
    """
    Find which skills from a given list appear in a text field (job title,
    description, or category), matching whole words only to avoid false
    matches like 'r' inside 'requirements'.
    """
    if pd.isna(text):
        return []
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    return found_skills