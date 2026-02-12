from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from src.models.predict_pipeline import predict

app = FastAPI(
    title="Bug Classification & Severity API",
    version="1.0"
)

# ---------- CORS CONFIG ----------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://bug-classification-api.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request Schema ----------
class BugRequest(BaseModel):
    text: str


# ---------- Response Schema ----------
class BugResponse(BaseModel):
    type: List[str]
    severity: str
    severity_score: float
    explanation: List[str] | None = None


# ---------- Routes ----------
@app.get("/")
def home():
    return {"message": "Bug Classification API running"}


@app.post("/predict", response_model=BugResponse)
def predict_bug(req: BugRequest):
    result = predict(req.text)
    return result