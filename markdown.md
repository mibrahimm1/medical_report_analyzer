# 🧠 Multimodal Medical Report Analyzer — Engineering Blueprint

## 0. Purpose

This document defines the exact implementation contract for building a full-stack AI system that:

- Accepts a Chest X-ray image + clinical report (text/PDF)
- Performs vision inference (YOLOv11)
- Executes multimodal reasoning (LangChain + Gemini 2.5 Flash)
- Outputs:
  - Annotated X-ray
  - Patient-friendly explanation (6th-grade level)

## 1. System Architecture
### 1.1 High-Level Design
```
[ Next.js Frontend ]
        ↓
[ FastAPI Backend ]
        ↓
 ┌──────────────────────────────┐
 │ Vision Engine (YOLOv11)      │
 │ Text Parser (PyMuPDF)        │
 │ LangChain Orchestrator       │
 │ Gemini 2.5 Flash (LLM)       │
 └──────────────────────────────┘
        ↓
[ Structured Response JSON ]
        ↓
[ Frontend Rendering Layer ]
``` 

## 2. Backend Specification (FastAPI)
### 2.1 Tech Stack
- Python 3.11+
- FastAPI
- Uvicorn
- Ultralytics (YOLOv11)
- LangChain
- langchain-google-genai
- PyMuPDF (fitz)
- OpenCV (opencv-python-headless)
- Pillow
- NumPy
### 2.2 Directory Structure
```plaintext
backend/
│
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── analyze.py
│   ├── services/
│   │   ├── vision.py
│   │   ├── parser.py
│   │   ├── orchestrator.py
│   │   └── utils.py
│   ├── schemas/
│   │   └── response.py
│   └── config.py
│
docker-compose.yml or Dockerfile, etc.
docker/
docker-compose.yml or Dockerfile, etc.
defaults and configs.
defaults and configs.
defaults and configs.
defaults and configs.
defaults and configs.
defaults and configs.
defaults and configs.
defaults and configs.
defaults and configs.
defaults and configs.
definitions of API endpoints, services, models, etc.
defined in respective files to modularize codebase.
to be used for deployment or local development setup.
to be used for deployment or local development setup.