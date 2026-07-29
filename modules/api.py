from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules.rag_engine import CoachingRAG
from modules.risk_predictor import RiskPredictor

app = FastAPI(title="CourtIQ Backend API")

# Initialize modules
rag_system = CoachingRAG()
risk_model = RiskPredictor()

class RiskInput(BaseModel):
    training_hours_weekly: float
    perceived_exertion_1to10: int
    sleep_hours: float
    past_injuries: int
    jump_load_count: int

class RAGQuery(BaseModel):
    question: str

@app.post("/predict_risk")
def predict_risk(data: RiskInput):
    return risk_model.predict_athlete_risk(data.dict())

@app.post("/ask_coach")
def ask_coach(query: RAGQuery):
    return rag_system.query_coaching_rag(query.question)
