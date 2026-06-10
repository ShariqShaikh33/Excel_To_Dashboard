# backend/routers/analytics_education.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
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
                "specialization_heatmap": {
                    "x_labels": [],
                    "y_labels": [],
                    "matrix_data": []
                },
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
        # REVISED DATA POINT 2: SPECIALIZATION HEATMAP MATRIX (Top 10 Majors)
        # ------------------------------------------------------------------
        # Uses SQL case optimizations to pivot intersected counts directly on disk pages
        heatmap_query = (
            db.query(
                models.Candidate.degree.label("major"),
                func.count(
                    case((models.Candidate.employment_status == "employed full-time (salaried)", 1))
                ).label("employed_full_time"),
                func.count(
                    case((models.Candidate.employment_status == "unemployed/currently seeking work", 1))
                ).label("unemployed"),
                func.count(
                    case((models.Candidate.employment_status == "student", 1))
                ).label("student")
            )
            .filter(models.Candidate.degree.isnot(None))
            .filter(models.Candidate.degree != "")
            .filter(models.Candidate.degree != "unspecified")
            .group_by(models.Candidate.degree)
            .order_by(func.count(models.Candidate.candidate_id).desc())
            .limit(10)
            .all()
        )
        
        specialization_matrix_data = [
            {
                "major": row.major if row.major else "unspecified",
                "employed_full_time": row.employed_full_time,
                "unemployed": row.unemployed,
                "student": row.student
            }
            for row in heatmap_query
        ]

        # Structure precise layout coordinate labels for the Heatmap implementation
        specialization_heatmap = {
            "x_labels": ["Employed Full-Time", "Unemployed", "Student"],
            "y_labels": [row["major"] for row in specialization_matrix_data],
            "matrix_data": specialization_matrix_data
        }

        # ------------------------------------------------------------------
        # DATA POINT 3: ACADEMIC INCOME THRESHOLD (Line Graph)
        # ------------------------------------------------------------------
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
        # DATA POINT 4: EDUCATION VS EMPLOYMENT STATUS (Nested Matrix Layout)
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

        # Define fine-grained statuses to combine under "employed"
        working_statuses = {
            "employed full-time (salaried)",
            "employed part-time (salaried)",
            "self-employed/entrepreneur",
            "apprentice/intern",
            "daily wage labourer/casual worker"
        }

        raw_matrix_data = []
        for row in matrix_query:
            level = row.highest_education_level if row.highest_education_level else "unspecified"
            raw_status = row.employment_status
            
            if raw_status in working_statuses:
                bundled_status = "employed"
            elif raw_status == "unemployed/currently seeking work":
                bundled_status = "unemployed"
            elif raw_status == "student":
                bundled_status = "student"
            else:
                continue  # Skips unneeded categories to maintain sharp layout focus

            raw_matrix_data.append({
                "level": level,
                "status": bundled_status,
                "count": row.count
            })

        # Initialize fallback variables
        matrix_data_records = []
        y_labels = []
        x_labels = ["Employed", "Unemployed", "Student"]

        if len(raw_matrix_data) > 0:
            df_mat = pd.DataFrame(raw_matrix_data)
            
            # Pivot table dynamically reshapes the rows into cross-tabulated columns
            pivot_mat = df_mat.pivot_table(
                index="level",
                columns="status",
                values="count",
                aggfunc="sum"
            ).fillna(0).astype(int)
            
            # Ensure all target columns exist
            for col in ["employed", "unemployed", "student"]:
                if col not in pivot_mat.columns:
                    pivot_mat[col] = 0
            
            # Enforce column sorting alignment
            pivot_mat = pivot_mat[["employed", "unemployed", "student"]]
            pivot_mat = pivot_mat.reset_index()
            
            # Generate your text row identifiers (e.g., ["undergraduate", "postgraduate"])
            y_labels = [str(lvl).title() for lvl in pivot_mat["level"].tolist()]
            
            # Map into the clean JSON record structures
            matrix_data_records = [
                {
                    "level": row["level"],
                    "employed": row["employed"],
                    "unemployed": row["unemployed"],
                    "student": row["student"]
                }
                for _, row in pivot_mat.iterrows()
            ]

        # Nesting everything under a dedicated object payload
        education_employment_matrix = {
            "x_labels": x_labels,
            "y_labels": y_labels,
            "matrix_data": matrix_data_records
        }
        # ------------------------------------------------------------------
        # UNIFIED RETURN JSON PAYLOAD
        # ------------------------------------------------------------------
        return {
            "attainment_ladder": attainment_ladder,
            "specialization_heatmap": specialization_heatmap, # Replaced old flat list with unified component payload
            "income_thresholds": income_thresholds,
            "education_employment_matrix": education_employment_matrix
        }

    except Exception as e:
        print(f"❌ Section 2 Analytics Engine Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate education analytics: {str(e)}")