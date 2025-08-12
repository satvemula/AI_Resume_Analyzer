import streamlit as st
import os
from dotenv import load_dotenv
from resume_utils import extract_resume_text
from nlp_utils import extract_skills_nlp, calculate_fit_score
from suggestions_engine import suggest_improvements

# Load environment variables
load_dotenv()

st.title("AI-Powered Resume Analyzer")
st.write("Upload your resume and paste a job description to get an AI-powered analysis of how well they match.")

# File upload
resume_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=['pdf', 'docx'])

# Job description input
job_desc = st.text_area("Paste the job description here", height=200)

# API key check
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.warning("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your .env file for AI suggestions.")

# Analysis button
if st.button("Analyze Resume", type="primary"):
    if not resume_file:
        st.error("Please upload a resume file.")
    elif not job_desc.strip():
        st.error("Please paste a job description.")
    else:
        try:
            with st.spinner("Analyzing your resume..."):
                # Extract text from resume
                file_type = resume_file.name.split('.')[-1].lower()
                resume_text = extract_resume_text(resume_file, file_type)
                
                if not resume_text.strip():
                    st.error("Could not extract text from the resume. Please check the file format.")
                    st.stop()
                
                # Extract skills using NLP
                resume_skills = extract_skills_nlp(resume_text)
                job_skills = extract_skills_nlp(job_desc)
                
                # Find matches and gaps
                matched_skills = set(resume_skills) & set(job_skills)
                missing_skills = set(job_skills) - set(resume_skills)
                
                # Calculate fit score
                score = calculate_fit_score(resume_text, job_desc)
                
                # Display results
                st.success("Analysis Complete!")
                
                # Score display with color coding
                col1, col2, col3 = st.columns(3)
                with col2:
                    if score >= 70:
                        st.metric("Job Fit Score", f"{score}%", delta="Excellent Match", delta_color="normal")
                    elif score >= 50:
                        st.metric("Job Fit Score", f"{score}%", delta="Good Match", delta_color="normal")
                    else:
                        st.metric("Job Fit Score", f"{score}%", delta="Needs Improvement", delta_color="inverse")
                
                # Skills analysis
                st.subheader("Skills Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**✅ Matched Skills:**")
                    if matched_skills:
                        for skill in sorted(matched_skills):
                            st.write(f"• {skill}")
                    else:
                        st.write("No direct skill matches found.")
                
                with col2:
                    st.write("**❌ Missing Skills:**")
                    if missing_skills:
                        for skill in sorted(missing_skills)[:10]:  # Limit to top 10
                            st.write(f"• {skill}")
                    else:
                        st.write("No missing skills identified.")
                
                # AI Suggestions (if API key available)
                if openai_api_key:
                    st.subheader("AI-Powered Suggestions")
                    with st.spinner("Generating AI suggestions..."):
                        try:
                            suggestions = suggest_improvements(resume_text, job_desc, openai_api_key)
                            st.write(suggestions)
                        except Exception as e:
                            st.error(f"Error getting AI suggestions: {str(e)}")
                else:
                    st.info("💡 Add your OpenAI API key to get personalized improvement suggestions!")
                
                # Resume preview (optional)
                with st.expander("View Extracted Resume Text"):
                    st.text_area("Extracted Text", resume_text, height=200, disabled=True)
                    
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.write("Please check your file format and try again.")

# Sidebar with instructions
with st.sidebar:
    st.header("How to Use")
    st.write("""
    1. **Upload Resume**: Choose a PDF or DOCX file
    2. **Paste Job Description**: Copy the job posting text
    3. **Click Analyze**: Get your match score and insights
    4. **Review Results**: See matched/missing skills
    5. **Get AI Suggestions**: Add OpenAI API key for personalized tips
    """)
    
    st.header("Setup Instructions")
    st.write("""
    **For AI suggestions, create a `.env` file:**
    ```
    OPENAI_API_KEY=your_api_key_here
    ```
    """)
    
    st.header("Supported Formats")
    st.write("📄 PDF files")
    st.write("📝 DOCX files")