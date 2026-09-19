# 🤖 AI Resume Job Matcher

An end-to-end AI-powered Resume–Job Matching platform that analyzes a candidate's resume against a job description, identifies matching and missing skills, and generates an explainable compatibility score.

The project is designed as a production-oriented ML application with a modular pipeline, REST API, dashboard, automated testing, and GenAI-ready architecture.

---

## 🚀 Key Features

- 📄 Resume text processing and skill extraction
- 💼 Job description analysis
- 🔍 Resume–Job skill matching
- 📊 Match percentage calculation
- ✅ Matched skills identification
- ❌ Missing skills identification
- ➕ Extra candidate skills detection
- 🧠 Machine-learning-ready matching pipeline
- ⚡ FastAPI REST API
- 📈 Streamlit dashboard
- 🧪 Automated API and pipeline testing
- 🛡️ Input validation and structured error handling
- 🗂️ Modular and scalable project architecture
- 🔌 GenAI integration-ready architecture

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   Resume / Job JD   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Text Preprocessing │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Skill Extraction    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Matching Pipeline   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
          Matched Skills  Missing Skills  Extra Skills
                 │             │             │
                 └─────────────┼─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Match Score / Result│
                    └──────────┬──────────┘
                               │
                  ┌────────────┴────────────┐
                  ▼                         ▼
           FastAPI REST API          Streamlit Dashboard
📂 Project Structure
ai-resume-job-matcher/
│
├── api/
│   ├── main.py
│   ├── schemas.py
│   └── routes/
│       ├── assistant.py
│       ├── health.py
│       ├── jobs.py
│       ├── matching.py
│       └── resume.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── raw/
│
├── genai/
│   ├── assistant.py
│   └── schemas.py
│
├── sql/
│
├── src/
│   ├── embeddings/
│   ├── extraction/
│   ├── ingestion/
│   ├── matching/
│   ├── pipeline/
│   ├── preprocessing/
│   ├── scoring/
│   └── utils/
│
├── tests/
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
🛠️ Technology Stack
Programming
Python
Data & Processing
Pandas
NumPy
Machine Learning
Scikit-learn
Feature engineering
Matching and scoring pipelines
API
FastAPI
Pydantic
Uvicorn
Dashboard
Streamlit
Testing
Pytest
FastAPI TestClient
Development
Git
GitHub
Virtual environments
⚡ API
The project provides a FastAPI-based REST API.
Start the API
uvicorn api.main:app --reload
The API will be available at:
http://127.0.0.1:8000
Swagger Documentation
http://127.0.0.1:8000/docs
🔎 Health Check
Endpoint
GET /health
Example response:
{
  "status": "healthy",
  "service": "ai-resume-job-matcher"
}
🎯 Resume–Job Matching
Endpoint
POST /match
Example request:
{
  "resume_text": "Python SQL Machine Learning FastAPI Docker",
  "job_description": "Looking for an AI/ML Engineer with Python, SQL, Machine Learning, FastAPI and Docker skills."
}
Example response:
{
  "resume_name": "Candidate",
  "job_title": "AI/ML Engineer",
  "match_percentage": 100,
  "matched_skills": [
    "docker",
    "fastapi",
    "machine learning",
    "python",
    "sql"
  ],
  "missing_skills": [],
  "extra_skills": [],
  "matched_count": 5,
  "missing_count": 0,
  "extra_count": 0,
  "skill_score": 100,
  "skill_score_max": 100,
  "pipeline_status": "success"
}
🧪 Testing
The project includes automated tests covering API, extraction, ingestion, matching, preprocessing, scoring, and pipeline components.
Run:
pytest
Current test status:
17 passed
🖥️ Dashboard
The project includes a Streamlit dashboard for interacting with the resume-job matching system.
Run:
streamlit run dashboard/app.py
🔐 Input Validation
The API validates incoming requests and rejects empty or whitespace-only resume/job-description inputs.
Example validation response:
{
  "error": "validation_error",
  "message": "Request validation failed."
}
🎯 Example Use Cases
Candidate–job compatibility analysis
Resume screening
Skill-gap identification
Recruitment assistance
Career preparation
Job recommendation systems
Automated resume analysis
🔮 Future Enhancements
PDF/DOCX resume upload
Semantic embedding-based matching
Advanced NLP-based skill extraction
Resume ranking across multiple job descriptions
LLM-powered resume improvement suggestions
Personalized skill-gap recommendations
Authentication and user management
Database-backed candidate profiles
Docker deployment
Cloud deployment
CI/CD pipeline
Production monitoring
📌 Project Highlights
This project demonstrates practical implementation of:
Python application development
Data preprocessing
NLP-oriented text processing
Skill extraction
Matching algorithms
Scoring systems
REST API development
Input validation
Automated testing
Dashboard development
Modular software architecture
Git/GitHub workflow
Production-oriented project structure
👨‍💻 Author
Aashish
AI/ML & Data Analytics Enthusiast
GitHub:
https://github.com/aashish-ml⁠�
📄 License
This project is licensed under the terms of the LICENSE file included in this repository.