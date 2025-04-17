from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.ainsight import AIInsight
from schemas.ainsight_schema import AIInsightCreate, AIInsightOut

router = APIRouter(
    prefix="/ainsights",
    tags=["AI Insights"]
)

@router.post("/", response_model=AIInsightOut)
def create_ai_insight(insight: AIInsightCreate, db: Session = Depends(get_db)):
    new_insight = AIInsight(**insight.dict())
    db.add(new_insight)
    db.commit()
    db.refresh(new_insight)
    return new_insight

@router.get("/{insight_id}", response_model=AIInsightOut)
def get_ai_insight(insight_id: int, db: Session = Depends(get_db)):
    insight = db.query(AIInsight).filter(AIInsight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    return insight

@router.get("/", response_model=list[AIInsightOut])
def list_ai_insights(db: Session = Depends(get_db)):
    return db.query(AIInsight).all()
