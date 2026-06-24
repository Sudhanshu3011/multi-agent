# Resume Analyser API

Multi-agent resume analysis system built with **LangGraph + LangChain + Groq + FastAPI**.

## Architecture

```
POST /api/v1/analyse (PDF + optional JD)
        │
        ▼
  OrchestratorAgent  ←── LangGraph StateGraph
   ├── ParserAgent       → pdfplumber tool + LLM section segmentation
   ├── SkillsAgent       → skill_matcher tool + LLM soft-skill enrichment
   ├── ScoringAgent      → rule-based scorer tool + LLM interpretation
   └── FeedbackAgent     → LLM actionable feedback generation
        │
        ▼
  Structured JSON Response
```

## Setup

### 1. Clone and install

```bash
cd resume-analyser
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

Get a free Groq API key at https://console.groq.com

### 3. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Reference

### `POST /api/v1/analyse`

**Content-Type:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume` | file (PDF) | ✅ | Resume PDF, max 5 MB |
| `job_description` | string | ❌ | JD text for skills gap analysis |

**Example (curl):**

```bash
curl -X POST http://localhost:8000/api/v1/analyse \
  -F "resume=@/path/to/resume.pdf" \
  -F "job_description=We are looking for a Python developer with FastAPI and PostgreSQL experience."
```

**Example Response:**

```json
{
  "candidate_name": "Sudhanshu Shekhar",
  "parsed_sections": {
    "summary": "...",
    "experience": "...",
    "education": "...",
    "skills": "...",
    "projects": "...",
    "certifications": ""
  },
  "skills": {
    "found": ["python", "fastapi", "langchain", "postgresql", "docker"],
    "missing": ["kubernetes", "terraform"],
    "match_score": 71.4,
    "technical_skills": ["python", "fastapi", "langchain"],
    "soft_skills": ["communication", "problem-solving"],
    "tools_and_platforms": ["docker", "github"],
    "domains": ["ai/ml", "backend engineering"]
  },
  "scores": {
    "experience": 82.0,
    "education": 90.0,
    "skills_match": 71.4,
    "overall": 81.5,
    "interpretations": {
      "experience_interpretation": "Strong experience section with quantified achievements.",
      "education_interpretation": "Solid academic background with CGPA mentioned.",
      "skills_interpretation": "Good skills match; cloud and infra gaps visible.",
      "overall_interpretation": "Strong candidate. Address missing cloud skills to improve fit."
    }
  },
  "feedback": [
    "Add quantifiable impact metrics (% improvement, user count) to each experience bullet.",
    "Include Kubernetes or Terraform in your projects to close the identified cloud gap.",
    "Expand your projects section with GitHub links and deployment details.",
    "Add a certifications section — AWS Cloud Practitioner or GCP Associate are quick wins.",
    "Your summary is strong; tailor it explicitly to each role's tech stack.",
    "Consider adding a separate 'Open Source Contributions' section for Trade-Agentic."
  ]
}
```

### `GET /api/v1/health`

Returns `{"status": "ok"}`.

### Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
resume-analyser/
├── app/
│   ├── main.py                  # FastAPI app
│   ├── api/routes.py            # POST /analyse endpoint
│   ├── agents/
│   │   ├── base_agent.py        # BaseAgent ABC
│   │   ├── orchestrator.py      # LangGraph graph
│   │   ├── parser_agent.py
│   │   ├── skills_agent.py
│   │   ├── scoring_agent.py
│   │   └── feedback_agent.py
│   ├── tools/
│   │   ├── pdf_extractor.py
│   │   ├── skill_matcher.py
│   │   └── scorer.py
│   ├── state/graph_state.py     # TypedDict state
│   ├── prompts/*.yaml           # Agent prompts
│   └── core/
│       ├── config.py
│       ├── errors.py
│       └── logger.py
├── .env.example
├── requirements.txt
└── README.md
```

## Notes

- LLM used: `llama-3.1-8b-instant` via Groq (free tier, ~10k tokens/min)
- Scoring is deterministic (rule-based) — LLM only adds qualitative interpretation
- Skill taxonomy is in `app/tools/skill_matcher.py` — extend `SKILL_TAXONOMY` freely
- No database, no auth, no queue — stateless per-request pipeline
