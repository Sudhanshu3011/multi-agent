from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Resume Analyser API",
    description=(
        "Multi-agent resume analysis pipeline powered by LangGraph + Groq. "
        "Upload a PDF resume (and optionally a job description) to receive "
        "structured parsing, skills analysis, section scores, and actionable feedback."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
