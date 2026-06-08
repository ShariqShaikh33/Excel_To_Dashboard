from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
import models
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Section 2: Gender Distribution"]
)

@router.get("/section2")
def get_section_2_data(db: Session = Depends(get_db)):
    print("Section2 working...")
    total_candidates = db.query(models.Candidate).count()
    
    # 2.1 Table of Education breakdown
    edu_breakdown_raw = db.query(
        models.Candidate.highest_education_level.label("category"),
        func.count(models.Candidate.candidate_id).label("count")
    ).group_by(models.Candidate.highest_education_level).all()

    education_breakdown_table = []
    for row in edu_breakdown_raw:
        education_breakdown_table.append({
            "category": row.category if row.category else "Unknown",
            "count": row.count,
            "percentage": round((row.count / total_candidates) * 100, 2) if total_candidates > 0 else 0
        })

    # 2.2 Table of median income by education
    # percentile_cont(0.5) handles the continuous median distribution mapping in PostgreSQL
    edu_median_raw = db.query(
        models.Candidate.highest_education_level.label("education"),
        func.percentile_cont(0.5).within_group(models.Candidate.monthly_income.asc()).label("median_income")
    ).group_by(models.Candidate.highest_education_level).all()

    education_median_income_table = []
    for row in edu_median_raw:
        education_median_income_table.append({
            "education": row.education if row.education else "Unknown",
            "median_income": round(row.median_income, 2) if row.median_income is not None else 0.0
        })

    return {
        "education_breakdown_table": education_breakdown_table,
        "education_median_income_table": education_median_income_table
    }

