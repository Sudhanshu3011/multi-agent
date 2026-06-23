import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# Instantiate FastAPI application
app = FastAPI(
    title="Multi-Agent Learning Path Generator",
    description="LangGraph-based pipeline for constructing learning paths and quizzes.",
    version="0.1.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router, tags=["API"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Multi-Agent Learning Path Generator API!",
        "health_check_url": "/health",
        "generate_path_url": "/generate-path"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
