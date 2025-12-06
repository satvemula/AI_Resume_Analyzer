# AI Resume Analyzer  

An intelligent resume parsing and analysis tool powered by Natural Language Processing (NLP) and AI.  

## Overview  
The AI Resume Analyzer reads PDF/DOCX resumes, extracts key skills and experience, and generates improvement recommendations tailored to the target job role. This tool is ideal for job seekers and recruiters looking for quick, AI-powered resume feedback.  
## Installation & Setup  
```bash
git clone [https://github.com/yourusername/AI_Resume_Analyzer.git](https://github.com/yourusername/AI_Resume_Analyzer.git)
cd AI_Resume_Analyzer
pip install -r requirements.txt

# --- MANDATORY: Download the English language model for spaCy ---
python -m spacy download en_core_web_sm
## Features  
- Parse resumes in PDF and DOCX formats  
- Extract skills, experience, and education using **spaCy**  
- Apply machine learning models for keyword matching and scoring  
- Generate improvement suggestions using **OpenAI API**  

## Tech Stack  
- **Python**  
- **spaCy**  
- **scikit-learn**  
- **OpenAI API**  
- **NumPy**  
- **PyPDF2**  
- **python-docx**  

## Installation & Setup  
```bash
git clone https://github.com/yourusername/AI_Resume_Analyzer.git
cd AI_Resume_Analyzer
pip install -r requirements.txt
