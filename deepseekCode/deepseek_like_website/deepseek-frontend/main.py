from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DeepSeek API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to DeepSeek API"}

@app.get("/products")
async def get_products():
    return [
        {"id": 1, "name": "Language Model", "category": "NLP"},
        {"id": 2, "name": "Computer Vision", "category": "CV"},
        {"id": 3, "name": "Speech Recognition", "category": "ASR"}
    ]

@app.get("/docs")
async def get_docs():
    return [
        {"id": 1, "title": "API Reference", "type": "documentation"},
        {"id": 2, "title": "Quick Start", "type": "tutorial"}
    ]
