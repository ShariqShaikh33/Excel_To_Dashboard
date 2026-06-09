from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import models
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Section 1: Gender Distribution"]
)

@router.get("/section1")
def get_section_1_data(db: Session = Depends(get_db)):
    try:
        # ------------------------------------------------------------------
        # DATA POINT 1: OVERALL REPRESENTATION RATIO (Donut Chart)
        # ------------------------------------------------------------------
        representation_query = (
            db.query(models.Candidate.gender, func.count(models.Candidate.candidate_id).label("count"))
            .group_by(models.Candidate.gender)
            .all()
        )
        print("R",representation_query)
        
        # Format directly into a simple clean array of key-value pairs for Donut Chart
        representation_ratio = [
            {"gender": row.gender if row.gender else "unspecified", "count": row.count}
            for row in representation_query
        ]
        print(representation_ratio)

        # ------------------------------------------------------------------
        # DATA POINT 2: EMPLOYMENT STATUS OVERLAP MATRIX (Data Matrix Table)
        # ------------------------------------------------------------------
        employment_query = (
            db.query(
                models.Candidate.employment_status,
                models.Candidate.gender,
                func.count(models.Candidate.candidate_id).label("count")
            )
            .group_by(models.Candidate.employment_status, models.Candidate.gender)
            .all()
        )

        # We use Pandas here to effortlessly pivot the raw relational database 
        # rows into a structured cross-tabulation matrix format
        raw_emp_data = [
            {
                "status": row.employment_status if row.employment_status else "unspecified",
                "gender": row.gender if row.gender else "unspecified",
                "count": row.count
            }
            for row in employment_query
        ]
        
        if raw_emp_data:
            df_emp = pd.DataFrame(raw_emp_data)
            # Pivot table makes columns out of gender types and keeps status as rows
            pivot_emp = df_emp.pivot_table(
                index="status", 
                columns="gender", 
                values="count", 
                aggfunc="sum"
            ).fillna(0).astype(int)
            
            # Add a row total calculation field natively via pandas utilities
            pivot_emp["total"] = pivot_emp.sum(axis=1)
            pivot_emp = pivot_emp.reset_index()
            
            # Format dataframe back to native JSON-ready dictionary structures
            employment_matrix = pivot_emp.to_dict(orient="records")
        else:
            employment_matrix = []

        # ------------------------------------------------------------------
        # DATA POINT 3: HIGHEST EDUCATION LEVEL BY GENDER (Stacked Column Chart)
        # ------------------------------------------------------------------
        education_query = (
            db.query(
                models.Candidate.highest_education_level,
                models.Candidate.gender,
                func.count(models.Candidate.candidate_id).label("count")
            )
            .group_by(models.Candidate.highest_education_level, models.Candidate.gender)
            .all()
        )

        raw_edu_data = [
            {
                "education": row.highest_education_level if row.highest_education_level else "unspecified",
                "gender": row.gender if row.gender else "unspecified",
                "count": row.count
            }
            for row in education_query
        ]

        if raw_edu_data:
            df_edu = pd.DataFrame(raw_edu_data)
            # Pivot ensures data aligns neatly by educational level blocks
            pivot_edu = df_edu.pivot_table(
                index="education", 
                columns="gender", 
                values="count", 
                aggfunc="sum"
            ).fillna(0).astype(int).reset_index()
            
            education_gender_matrix = pivot_edu.to_dict(orient="records")
        else:
            education_gender_matrix = []

        # ------------------------------------------------------------------
        # UNIFIED RETURN PAYLOAD
        # ------------------------------------------------------------------
        return {
            "representation_ratio": representation_ratio,
            "employment_matrix": employment_matrix,
            "education_gender_matrix": education_gender_matrix
        }

    except Exception as e:
        print(f"❌ Analytics Aggregation Failure: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate gender analytics: {str(e)}")