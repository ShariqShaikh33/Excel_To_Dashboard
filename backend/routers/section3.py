# backend/routers/analytics_employment.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
import models
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Employment Analytics Engine"]
)

@router.get("/section3")
async def get_employment_tab_data(db: Session = Depends(get_db)):
    try:
        # Debug Check: Verify data presence before calculation engines fire
        total_candidates = db.query(func.count(models.Candidate.candidate_id)).scalar()
        if total_candidates == 0:
            return {
                "workforce_status": [],
                "earnings_distribution": [],
                "income_disparity_index": []
            }

        # ------------------------------------------------------------------
        # DATA POINT 1: WORKFORCE STATUS (Pie Chart)
        # ------------------------------------------------------------------
        status_query = (
            db.query(
                models.Candidate.employment_status,
                func.count(models.Candidate.candidate_id).label("count")
            )
            .group_by(models.Candidate.employment_status)
            .all()
        )
        
        workforce_status = [
            {
                "status": row.employment_status if row.employment_status else "unspecified",
                "count": row.count
            }
            for row in status_query
        ]

        # ------------------------------------------------------------------
        # DATA POINT 2: INDIVIDUAL EARNINGS DISTRIBUTION (Histogram Bins)
        # ------------------------------------------------------------------
        # Leverages SQL CASE constructs to execute lightning-fast binning on 50k+ rows
        earnings_query = (
            db.query(
                case(
                    (models.Candidate.monthly_income == 0, "No Income"),
                    (models.Candidate.monthly_income <= 10000, "₹1 - ₹10k"),
                    (models.Candidate.monthly_income <= 20000, "₹10k - ₹20k"),
                    else_="Above ₹20k"
                ).label("income_bracket"),
                func.count(models.Candidate.candidate_id).label("count")
            )
            .group_by("income_bracket")
            .all()
        )
        
        # Helper dictionary to maintain an intentional sort order on the front-end axis
        order_mapping = {"No Income": 1, "₹1 - ₹10k": 2, "₹10k - ₹20k": 3, "Above ₹20k": 4}
        
        earnings_distribution = sorted(
            [
                {"bracket": row.income_bracket, "count": row.count}
                for row in earnings_query
            ],
            key=lambda x: order_mapping.get(x["bracket"], 5)
        )

        # ------------------------------------------------------------------
        # DATA POINT 3: INCOME DISPARITY INDEX (Scatter Plot Data Feed)
        # ------------------------------------------------------------------
        # Performs an internal relational table JOIN to pair individual vs household records
        disparity_query = (
            db.query(
                models.Candidate.monthly_income.label("candidate_income"),
                models.Household.average_monthly_income.label("household_income")
            )
            .join(models.Household, models.Candidate.household_id == models.Household.household_id)
            .filter(models.Household.average_monthly_income > 0)
            # Limit the output points to prevent front-end browser canvas crashes over 50k+ nodes
            .limit(2000) 
            .all()
        )
        
        income_disparity_index = [
            {
                "x": float(row.candidate_income), # Candidate individual earnings plotted on X axis
                "y": float(row.household_income)  # Shared household revenue plotted on Y axis
            }
            for row in disparity_query
        ]

        # ------------------------------------------------------------------
        # UNIFIED RETURN JSON PAYLOAD
        # ------------------------------------------------------------------
        return {
            "workforce_status": workforce_status,
            "earnings_distribution": earnings_distribution,
            "income_disparity_index": income_disparity_index
        }

    except Exception as e:
        print(f"❌ Section 3 Analytics Engine Failure: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate employment analytics: {str(e)}")