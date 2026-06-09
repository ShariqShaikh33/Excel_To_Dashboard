# backend/routers/analytics_education.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import models
from database import get_db

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Education Analytics Engine"]
)

@router.get("/section2")
async def get_education_tab_data(db: Session = Depends(get_db)):
    try:
        # Debug Check: Verify if any data is present
        total_candidates = db.query(func.count(models.Candidate.candidate_id)).scalar()
        if total_candidates == 0:
            return {
                "attainment_ladder": [],
                "specialization_analytics": [],
                "income_thresholds": [],
                "education_employment_matrix": []
            }

        # ------------------------------------------------------------------
        # DATA POINT 1: ACADEMIC ATTAINMENT LADDER (Vertical Bar Chart)
        # ------------------------------------------------------------------
        attainment_query = (
            db.query(
                models.Candidate.highest_education_level, 
                func.count(models.Candidate.candidate_id).label("count")
            )
            .group_by(models.Candidate.highest_education_level)
            .order_by(func.count(models.Candidate.candidate_id).desc())
            .all()
        )
        
        attainment_ladder = [
            {
                "level": row.highest_education_level if row.highest_education_level else "unspecified", 
                "count": row.count
            }
            for row in attainment_query
        ]

        # ------------------------------------------------------------------
        # DATA POINT 2: SPECIALIZATION & MAJOR ANALYTICS (High-Density List)
        # ------------------------------------------------------------------
        # Grabs text-typed degrees (e.g., 'bcom', 'ba', 'bsc') while filtering out nulls
        degree_query = (
            db.query(
                models.Candidate.degree, 
                func.count(models.Candidate.candidate_id).label("count")
            )
            .filter(models.Candidate.degree.isnot(None))
            .filter(models.Candidate.degree != "")
            .group_by(models.Candidate.degree)
            .order_by(func.count(models.Candidate.candidate_id).desc())
            .limit(10) # Keeps the visualization clean by picking top 10 categories
            .all()
        )
        
        specialization_analytics = [
            {"degree": row.degree, "count": row.count}
            for row in degree_query
        ]

        # ------------------------------------------------------------------
        # DATA POINT 3: ACADEMIC INCOME THRESHOLD (Line Graph)
        # ------------------------------------------------------------------
        # Calculates the statistical average salary per academic milestone
        income_query = (
            db.query(
                models.Candidate.highest_education_level,
                func.avg(models.Candidate.monthly_income).label("avg_income")
            )
            .group_by(models.Candidate.highest_education_level)
            .all()
        )
        
        income_thresholds = [
            {
                "level": row.highest_education_level if row.highest_education_level else "unspecified",
                "average_income": round(float(row.avg_income), 2) if row.avg_income else 0.0
            }
            for row in income_query
        ]

        # ------------------------------------------------------------------
        # DATA POINT 4: EDUCATION VS EMPLOYMENT STATUS (Data Matrix Table)
        # ------------------------------------------------------------------
        matrix_query = (
            db.query(
                models.Candidate.highest_education_level,
                models.Candidate.employment_status,
                func.count(models.Candidate.candidate_id).label("count")
            )
            .group_by(models.Candidate.highest_education_level, models.Candidate.employment_status)
            .all()
        )

        raw_matrix_data = [
            {
                "level": row.highest_education_level if row.highest_education_level else "unspecified",
                "status": row.employment_status if row.employment_status else "unspecified",
                "count": row.count
            }
            for row in matrix_query
        ]

        if len(raw_matrix_data) > 0:
            df_mat = pd.DataFrame(raw_matrix_data)
            
            # Pivot table converts the vertical rows into an elegant, structural matrix layout
            pivot_mat = df_mat.pivot_table(
                index="level",
                columns="status",
                values="count",
                aggfunc="sum"
            ).fillna(0).astype(int)
            
            # Append horizontal row summaries natively
            pivot_mat["total"] = pivot_mat.sum(axis=1)
            pivot_mat = pivot_mat.reset_index()
            
            education_employment_matrix = pivot_mat.to_dict(orient="records")
        else:
            education_employment_matrix = []

        # ------------------------------------------------------------------
        # UNIFIED RETURN JSON PAYLOAD
        # ------------------------------------------------------------------
        return {
            "attainment_ladder": attainment_ladder,
            "specialization_analytics": specialization_analytics,
            "income_thresholds": income_thresholds,
            "education_employment_matrix": education_employment_matrix
        }

    except Exception as e:
        print(f"❌ Section 2 Analytics Engine Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate education analytics: {str(e)}")