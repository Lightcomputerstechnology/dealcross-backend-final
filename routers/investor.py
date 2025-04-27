from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models import User

router = APIRouter(prefix="/investor", tags=["Investor Tools"])

# ─────────── Investment Reports ───────────
@router.get("/reports", summary="Investor: View investment reports")
def get_investment_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return [
        {"company": "Tesla", "amount": 5000, "roi": "12%", "date": "2024-01-10"},
        {"company": "Apple", "amount": 2000, "roi": "8%", "date": "2024-03-03"},
        {"company": "Amazon", "amount": 3500, "roi": "15%", "date": "2024-04-02"},
    ]

# ─────────── AI Insights ───────────
@router.get("/insights", summary="Investor: View AI insights")
def get_ai_insights():
    return [
        {
            "icon": "trending-up",
            "title": "Rising Deal Categories",
            "description": "Freelance design, crypto mentorship, and affiliate marketing are trending.",
            "category": "Deals",
            "confidence": 92,
        },
        {
            "icon": "shield-off",
            "title": "Fraud Spike Alerts",
            "description": "50% of fraud attempts are now linked to ID document forgery.",
            "category": "Fraud",
            "confidence": 88,
        },
        {
            "icon": "pie-chart",
            "title": "Top Share Opportunities",
            "description": "Tesla, Nvidia, and Apple offer strong short-term ROI in Q2.",
            "category": "Shares",
            "confidence": 95,
        },
    ]