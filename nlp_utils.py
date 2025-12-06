import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
# Remove subprocess and sys imports

# Load spaCy model immediately
nlp = spacy.load("en_core_web_sm")
# ... (rest of your functions) ...


def extract_skills_nlp(text):
    """
    Extract skills from text using NLP techniques.
    This is a basic implementation that can be enhanced with better skill detection.
    """
    doc = nlp(text.lower())
    
    # Common technical skills and keywords to look for
    skill_keywords = {
        'python', 'java', 'javascript', 'react', 'node', 'sql', 'mysql', 'postgresql',
        'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'linux',
        'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas',
        'numpy', 'scikit-learn', 'html', 'css', 'bootstrap', 'angular', 'vue',
        'express', 'django', 'flask', 'spring', 'hibernate', 'rest', 'api',
        'microservices', 'devops', 'ci/cd', 'jenkins', 'terraform', 'ansible',
        'scrum', 'agile', 'project management', 'leadership', 'communication',
        'problem solving', 'analytical', 'teamwork', 'excel', 'powerpoint',
        'tableau', 'power bi', 'spark', 'hadoop', 'kafka', 'redis', 'elasticsearch'
    }
    
    # Extract nouns and noun phrases as potential skills
    skills = set()
    
    # Extract single token skills
    for token in doc:
        if (token.pos_ in ["NOUN", "PROPN"] and 
            len(token.text) > 2 and 
            not token.is_stop and 
            not token.is_punct):
            skills.add(token.text.lower())
    
    # Extract multi-word skills (noun phrases)
    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) <= 3:  # Limit to reasonable phrase length
            skills.add(chunk.text.lower().strip())
    
    # Add known skill keywords found in text
    text_lower = text.lower()
    for skill in skill_keywords:
        if skill in text_lower:
            skills.add(skill)
    
    # Filter out common non-skill words
    non_skills = {
        'experience', 'work', 'job', 'company', 'team', 'project', 'role',
        'position', 'responsibility', 'task', 'duty', 'requirement', 'skill',
        'ability', 'knowledge', 'education', 'degree', 'university', 'college',
        'year', 'month', 'time', 'day', 'week', 'people', 'person', 'client',
        'customer', 'business', 'industry', 'field', 'area', 'part', 'way',
        'thing', 'information', 'data', 'system', 'process', 'service',
        'product', 'solution', 'application', 'software', 'technology'
    }
    
    # Remove non-skills and very short/long terms
    filtered_skills = {
        skill for skill in skills 
        if skill not in non_skills and 2 < len(skill) < 25
    }
    
    return list(filtered_skills)

def get_vector(text):
    """
    Get document vector using spaCy's pre-trained word vectors.
    """
    doc = nlp(text)
    # Use the document vector (average of token vectors)
    return doc.vector

def calculate_fit_score(resume_text, job_desc_text):
    """
    Calculate how well a resume matches a job description using cosine similarity.
    """
    try:
        # Get vectors for both texts
        resume_vector = get_vector(resume_text)
        job_vector = get_vector(job_desc_text)
        
        # Check if vectors are valid (not all zeros)
        if np.allclose(resume_vector, 0) or np.allclose(job_vector, 0):
            # Fallback to keyword matching if vectors are not available
            return calculate_keyword_similarity(resume_text, job_desc_text)
        
        # Calculate cosine similarity
        # Cosine similarity formula: $\frac{A \cdot B}{\|A\| \|B\|}$
        similarity = cosine_similarity([resume_vector], [job_vector])[0][0]
        
        # Convert to percentage and ensure it's reasonable
        score = max(0, min(100, round(similarity * 100, 2)))
        
        return score
        
    except Exception as e:
        print(f"Error calculating fit score: {e}")
        # Fallback to keyword matching
        return calculate_keyword_similarity(resume_text, job_desc_text)

def calculate_keyword_similarity(resume_text, job_desc_text):
    """
    Fallback method to calculate similarity based on keyword overlap.
    """
    resume_skills = set(extract_skills_nlp(resume_text))
    job_skills = set(extract_skills_nlp(job_desc_text))
    
    if not job_skills:
        return 0
    
    matched_skills = resume_skills & job_skills
    similarity_ratio = len(matched_skills) / len(job_skills)
    
    return round(similarity_ratio * 100, 2)

def clean_text(text):
    """
    Clean text for better processing.
    """
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text