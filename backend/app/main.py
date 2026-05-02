from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze
from app.config import settings

app = FastAPI(title="Multimodal Medical Report Analyzer API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api", tags=["Analyze"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Multimodal Medical Report Analyzer API"}
