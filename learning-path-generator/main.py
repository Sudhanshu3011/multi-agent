import uvicorn
from app.config import settings

def main():
    print(f"Starting uvicorn server at http://{settings.HOST}:{settings.PORT}")
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

if __name__ == "__main__":
    main()
