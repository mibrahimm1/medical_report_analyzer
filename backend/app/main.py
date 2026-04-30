from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analyze
from app.config import settings

app = FastAPI(title="Multimodal Medical Report Analyzer API")

# Configure CORS - FRONTEND_URL env var controls allowed origins
# Set to your Vercel URL in production, defaults to '*' for local dev
allow_origins = [settings.frontend_url] if settings.frontend_url != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api", tags=["Analyze"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Multimodal Medical Report Analyzer API"}
