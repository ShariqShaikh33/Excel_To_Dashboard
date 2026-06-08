from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
import models
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Section 3: Gender Distribution"]
)

@router.get("/section3")
def get_section_3_data(db: Session = Depends(get_db)):
    total_candidates = db.query(models.Candidate).count()

    # 3.1 & 3.2 Main metrics grouping
    emp_raw = db.query(
        models.Candidate.employment_status.label("category"),
        func.count(models.Candidate.candidate_id).label("count")
    ).group_by(models.Candidate.employment_status).all()

    employment_cards = []
    detailed_employment_table = []

    for row in emp_raw:
        emp_type = row.category if row.category else "Not Specified"
        percentage = round((row.count / total_candidates) * 100, 2) if total_candidates > 0 else 0
        
        # Structure for 3.1 individual semantic UI cards
        employment_cards.append({
            "employment_type": emp_type,
            "number_of_people": row.count,
            "percentage": percentage
        })
        
        # Structure for 3.2 summary data matrix table
        detailed_employment_table.append({
            "category": emp_type,
            "count": row.count,
            "percentage": percentage
        })

    # 3.3 Table of median income by employment
    emp_median_raw = db.query(
        models.Candidate.employment_status.label("employment_type"),
        func.percentile_cont(0.5).within_group(models.Candidate.monthly_income.asc()).label("median_income")
    ).group_by(models.Candidate.employment_status).all()

    median_income_by_employment_table = []
    for row in emp_median_raw:
        median_income_by_employment_table.append({
            "employment_type": row.employment_type if row.employment_type else "Not Specified",
            "median_income": round(row.median_income, 2) if row.median_income is not None else 0.0
        })

    return {
        "employment_cards": employment_cards,
        "detailed_employment_table": detailed_employment_table,
        "median_income_by_employment_table": median_income_by_employment_table
    }
