# Resume Analyser API

Multi-agent resume analysis pipeline powered by **LangGraph + LangChain + Groq + FastAPI**. It parses resume PDFs, performs skills analysis, scores the resume against a job description, provides structural feedback, and automatically searches matching jobs via SerpApi.

## Architecture

The orchestrator utilizes **LangGraph** to manage states and route steps. Some steps execute in parallel (such as scoring and job searching) to optimize performance:

```
              POST /api/v1/analyse (PDF + optional JD)
                                │
                                ▼
                       [ parser_node ] (ParserAgent)
                                │
                                ▼
                       [ skills_node ] (SkillsAgent)
                        /             \
                       /               \ (Parallel)
                      ▼                 ▼
          [ scoring_node ]       [ job_fetcher_node ]
           (ScoringAgent)        (JobFetcherAgent)
                  │                     │
                  ▼                     │
          [ feedback_node ]             │
          (FeedbackAgent)               │
                  \                     /
                   \                   /
                    ▼                 ▼
                   [ aggregator_node ] (combines outputs)
                                │
                                ▼
                     Structured JSON Response
```

- **ParserAgent**: Extracts text using the `pdfplumber` backend and segments it into structured profile fields.
- **SkillsAgent**: Groups and enriches identified candidate skills, tools & platforms, and domains.
- **ScoringAgent**: Matches skills/experience against the provided job description and computes a qualitative match score.
- **FeedbackAgent**: Suggests constructive improvements to improve the resume format and candidate profile.
- **JobFetcherAgent**: Invokes SerpApi's Google Jobs Search tool using search queries tailored to the candidate's skills.
- **Aggregator**: Consolidates all final agent outputs into the structured JSON payload returned by the API.

## Setup

### 1. Install dependencies

Make sure your virtual environment is active, then install dependencies:

```bash
cd resume-analyser
pip install -r requirements.txt
```

### 2. Configure environment

Copy the env template:

```bash
cp .env.example .env
```

Open `.env` and configure your API keys:

```ini
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
LOG_LEVEL=INFO
```

_Note: A free Groq API key can be generated at [console.groq.com](https://console.groq.com). A SerpApi key can be generated at [serpapi.com](https://serpapi.com)._

### 3. Run the API server

Start the FastAPI application:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Reference

### `POST /api/v1/analyse`

**Content-Type:** `multipart/form-data`

| Field             | Type       | Description                                         |
| ----------------- | ---------- | --------------------------------------------------- |
| `resume`          | file (PDF) | Resume PDF, maximum size 5 MB                       |
| `job_description` | string     | Target job description text for skills gap analysis |

**Example request (curl):**

```bash
curl -X POST http://localhost:8000/api/v1/analyse \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=We are looking for a Python developer with FastAPI and PostgreSQL experience."
```

**Example Response:**

```json
{
  "parsed_resume": {
    "candidate_name": "John Doe",
    "summary": "Experienced Software Engineer specializing in scalable web services.",
    "experience": "Software Engineer at Tech Corp (2022-Present)...",
    "education": "BS in Computer Science, State University",
    "skills": "Python, FastAPI, Docker, SQL",
    "projects": "Built and deployed a microservice architecture...",
    "certifications": "AWS Certified Developer"
  },
  "skills_analysis": {
    "technical_skills": ["python", "fastapi", "docker", "sql"],
    "tools_and_platforms": ["docker", "git"],
    "domains": ["backend engineering", "cloud computing"]
  },
  "scores": {
    "llm_score": 85,
    "missing_skills": ["postgresql"],
    "explanation": "Candidate matches Python, FastAPI, and Docker. Missing PostgreSQL."
  },
  "feedback": [
    "Quantify your metrics in your Tech Corp experience section.",
    "Mention PostgreSQL or database design experience since it is required for the target role."
  ],
  "recommended_jobs": [
    {
      "title": "Python Developer",
      "company": "FastAPI Solutions LLC",
      "location": "Remote",
      "via": "via LinkedIn",
      "posted_at": "2 days ago"
    }
  ]
}
```

---

### `GET /api/v1/health`

Returns a basic health check response:

```json
{
  "status": "ok",
  "service": "resume-analyser"
}
```

---

## Project Structure

```
resume-analyser/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py            # API router and endpoints
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py        # Base Agent abstract class
│   │   ├── parser_agent.py      # Resume Parser agent
│   │   ├── skills_agent.py      # Skills Matcher / Enricher agent
│   │   ├── scoring_agent.py     # Evaluation & scoring agent
│   │   ├── feedback_agent.py    # Feedback Generator agent
│   │   └── job_fetcher_agent.py # Job query & search agent
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py     # PDF extraction utility
│   │   └── job_search.py        # SerpApi Google Jobs search tool
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── builder.py           # LangGraph compiler & orchestrator
│   │   └── state.py             # TypedDict representing ResumeState
│   ├── prompts/                 # System & user templates (YAML)
│   │   ├── parser_agent.yaml
│   │   ├── skills_agent.yaml
│   │   ├── scoring_agent.yaml
│   │   ├── feedback_agent.yaml
│   │   └── job_query.yaml
│   └── core/
│       ├── __init__.py
│       ├── config.py            # Pydantic Settings
│       └── logger.py            # Python logging configuration
├── .env.example
├── requirements.txt
└── README.md
```
