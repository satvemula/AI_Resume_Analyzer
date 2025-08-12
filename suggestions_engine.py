from openai import OpenAI
import json

def suggest_improvements(resume_text, job_desc_text, api_key):
    """
    Generate AI-powered suggestions for improving resume-job fit.
    
    Args:
        resume_text: Extracted resume text
        job_desc_text: Job description text
        api_key: OpenAI API key
    
    Returns:
        String with improvement suggestions
    """
    try:
        client = OpenAI(api_key=api_key)
        
        # Truncate texts to fit within token limits (reduced for lower API usage)
        resume_snippet = resume_text[:800]
        job_snippet = job_desc_text[:600]
        
        prompt = f"""
        Analyze this resume against the job description. Provide 3 key improvements:

        RESUME: {resume_snippet}
        JOB: {job_snippet}

        Give me:
        1. Overall fit (1 sentence)
        2. Top 2 missing skills to add
        3. Top 2 action items
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert career counselor and resume optimization specialist. Provide practical, actionable advice that helps job seekers improve their resume's match with specific job postings."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=300,
            temperature=0.5
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating suggestions: {str(e)}\n\nPlease check your API key and try again."

def get_keyword_suggestions(resume_text, job_desc_text, api_key):
    """
    Get specific keyword suggestions for ATS optimization.
    """
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        List 5 key terms from this job description missing from this resume:

        Job: {job_desc_text[:600]}
        Resume: {resume_text[:600]}

        Return only keywords, one per line.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip().split('\n')
        
    except Exception as e:
        return [f"Error: {str(e)}"]

def generate_cover_letter_tips(resume_text, job_desc_text, api_key):
    """
    Generate cover letter tips based on the resume and job description.
    """
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Give 2 cover letter tips based on:
        Resume: {resume_text[:800]}
        Job: {job_desc_text[:600]}

        Focus on specific matching experiences.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.6
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating cover letter tips: {str(e)}"

def analyze_resume_structure(resume_text, api_key):
    """
    Analyze resume structure and formatting suggestions.
    """
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Quick resume structure feedback for:
        {resume_text[:1000]}

        Give 2 improvement suggestions for organization/format.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing resume structure: {str(e)}"