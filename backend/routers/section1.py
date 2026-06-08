from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
import models
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Section 1: Gender Distribution"]
)

@router.get("/section1")
def get_section_1_data(db: Session = Depends(get_db)):
    total_candidates = db.query(models.Candidate).count()
    if total_candidates == 0:
        return {"error": "No candidate data available"}

    # 1.1 High level totals and overall percentages
    gender_raw = db.query(
        models.Candidate.gender,
        func.count(models.Candidate.candidate_id).label("count")
    ).group_by(models.Candidate.gender).all()

    gender_distribution = []
    for gender, count in gender_raw:
        gender_name = gender if gender else "Other/Not Specified"
        gender_distribution.append({
            "gender": gender_name,
            "count": count,
            "percentage": round((count / total_candidates) * 100, 2)
        })

    # 1.2 Gender x Employment cross-tabulation table
    # Using conditional aggregation (CASE WHEN) to build the pivot table efficiently
    gender_emp_raw = db.query(
        models.Candidate.employment_status.label("employment_type"),
        func.count(case((models.Candidate.gender == 'Male', 1))).label("male_count"),
        func.count(case((models.Candidate.gender == 'Female', 1))).label("female_count"),
        func.count(case((~models.Candidate.gender.in_(['Male', 'Female']), 1))).label("other_count"),
        func.count(models.Candidate.candidate_id).label("total")
    ).group_by(models.Candidate.employment_status).all()

    gender_employment_table = []
    for row in gender_emp_raw:
        gender_employment_table.append({
            "employment_type": row.employment_type if row.employment_type else "Not Specified",
            "no_of_male": row.male_count,
            "no_of_female": row.female_count,
            "no_of_other": row.other_count,
            "total": row.total
        })

    return {
        "gender_distribution": gender_distribution,
        "gender_employment_table": gender_employment_table
    }

