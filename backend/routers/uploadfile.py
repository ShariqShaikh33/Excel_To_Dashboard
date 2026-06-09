# backend/routers/upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
import io
import models
from database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Data Ingestion & Cleaning Pipeline"]
)

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    buffer = io.BytesIO(contents)
    
    try:
        xls = pd.ExcelFile(buffer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Excel workbook structure: {str(e)}")

    # =======================================================
    # 1. DATABASE CLEARANCE (PREVENTS PRIMARY KEY COLLISIONS)
    # =======================================================
    try:
        print("🧹 Wiping old data layers...")
        db.query(models.Candidate).delete()
        db.query(models.Household).delete()
        db.flush() 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear database constraints: {str(e)}")
    
    # =======================================================
    # 2. EXPANDED VECTORIZED DATA CLEANING ENGINE
    # =======================================================
    try:
        # ---------------------------------------------------
        # SHEET A: HOUSEHOLDS EXPANDED PIPELINE
        # ---------------------------------------------------
        if 'Households' in xls.sheet_names:
            df_hh = pd.read_excel(xls, 'Households')
            df_hh.columns = [c.lower().strip().replace(' ', '_') for c in df_hh.columns]
            
            # Text Categorical Standardization (Lowercase & strip whitespace)
            categorical_hh_cols = [
                'household_type', 'district', 'willingness', 'status', 
                'street_and_locality_name', 'territory_name', 
                'created_by_name', 'supervisor_name', 'household_rejected_reason'
            ]
            for text_col in categorical_hh_cols:
                if text_col in df_hh.columns:
                    df_hh[text_col] = df_hh[text_col].astype(str).str.strip().str.lower()
                    df_hh[text_col] = df_hh[text_col].replace({'nan': None, '': None})

            # Clean Pincodes (Strip trailing .0 floats from Excel numeric auto-detect)
            if 'pincode' in df_hh.columns:
                df_hh['pincode'] = df_hh['pincode'].astype(str).str.split('.').str[0].str.strip()
                df_hh['pincode'] = df_hh['pincode'].replace({'nan': None, '': None})

            # Geographic Coordinate Floating Point Safeguards
            for geo_col in ['latitude', 'longitude']:
                if geo_col in df_hh.columns:
                    df_hh[geo_col] = pd.to_numeric(df_hh[geo_col], errors='coerce')
                    df_hh[geo_col] = np.where(df_hh[geo_col].isna(), None, df_hh[geo_col])

            # Numeric/Financial Firewall Coercion
            if 'average_monthly_income' in df_hh.columns:
                df_hh['average_monthly_income'] = pd.to_numeric(df_hh['average_monthly_income'], errors='coerce').fillna(0.0)
            
            # if 'monthly_expenses_including_housing_and_food' in df_hh.columns:
            #     df_hh['monthly_expenses_including_housing_and_food'] = pd.to_numeric(
            #         df_hh['monthly_expenses_including_housing_and_food'], errors='coerce'
            #     ).fillna(0.0)

            # if 'members_age_18_to_40' in df_hh.columns:
            #     df_hh['members_age_18_to_40'] = pd.to_numeric(df_hh['members_age_18_to_40'], errors='coerce').fillna(0).astype(int)

            if 'urgent_candidate_count' in df_hh.columns:
                df_hh['urgent_candidate_count'] = pd.to_numeric(df_hh['urgent_candidate_count'], errors='coerce').fillna(0).astype(int)

            if 'hqs_score' in df_hh.columns:
                scores = pd.to_numeric(df_hh['hqs_score'], errors='coerce')
                df_hh['hqs_score'] = np.where(scores.isna(), None, scores)

            # Map & Push Households
            print(f"✅ Cleaned {len(df_hh)} Household rows.")
            for _, row in df_hh.iterrows():
                row_data = row.where(pd.notnull(row), None).to_dict()
                
                new_house = models.Household(
                    household_id=row_data.get("household_id"),
                    household_type=row_data.get("household_type"),
                    # street_and_locality_name=row_data.get("street_and_locality_name"),
                    latitude=row_data.get("latitude"),
                    longitude=row_data.get("longitude"),
                    territory_name=row_data.get("territory_name"),
                    district=row_data.get("district"),
                    pincode=row_data.get("pincode"),
                    willingness=row_data.get("willingness"),
                    average_monthly_income=row_data.get("average_monthly_income"),
                    # monthly_expenses_including_housing_and_food=row_data.get("monthly_expenses_including_housing_and_food"),
                    # members_age_18_to_40=row_data.get("members_age_18_to_40"),
                    urgent_candidate_count=row_data.get("urgent_candidate_count"),
                    status=row_data.get("status"),
                    created_by_name=row_data.get("created_by_name"),
                    # supervisor_name=row_data.get("supervisor_name"),
                    # household_rejected_reason=row_data.get("household_rejected_reason"),
                    hqs_score=row_data.get("hqs_score")
                )
                db.add(new_house)
                
            db.flush() # Locks foreign keys before processing candidates

        # ---------------------------------------------------
        # SHEET B: CANDIDATES EXPANDED PIPELINE
        # ---------------------------------------------------
        if 'Candidates' in xls.sheet_names:
            df_cand = pd.read_excel(xls, 'Candidates')
            df_cand.columns = [c.lower().strip().replace(' ', '_') for c in df_cand.columns]

            # Expanded String Normalization (Handles newly added strings and text arrays)
            categorical_cand_cols = [
                'name', 'gender', 'highest_education_level', 'degree', 
                'digital_tools_used', 'work_related_skills',
                'preferred_job_roles', 'preferred_sectors', 'how_far_will_travel', 
                'support_factors', 'employment_status', 'main_reason_not_working'
            ]
            for text_col in categorical_cand_cols:
                if text_col in df_cand.columns:
                    df_cand[text_col] = df_cand[text_col].astype(str).str.strip().str.lower()
                    df_cand[text_col] = df_cand[text_col].replace({'nan': None, '': None})

            # Resilient Date Parsing Pipeline (Ages and Pyramids)
            if 'date_of_birth' in df_cand.columns:
                df_cand['date_of_birth'] = pd.to_datetime(df_cand['date_of_birth'], errors='coerce')

            # Financial Individual Target Coercion
            if 'monthly_income' in df_cand.columns:
                df_cand['monthly_income'] = pd.to_numeric(df_cand['monthly_income'], errors='coerce').fillna(0.0)

            if 'hqs_score' in df_cand.columns:
                c_scores = pd.to_numeric(df_cand['hqs_score'], errors='coerce')
                df_cand['hqs_score'] = np.where(c_scores.isna(), None, c_scores)

            # Map & Push Candidates
            print(f"✅ Cleaned {len(df_cand)} Candidate rows.")
            for _, row in df_cand.iterrows():
                row_data = row.where(pd.notnull(row), None).to_dict()
                
                dob_val = row_data.get("date_of_birth")
                if dob_val and not pd.isnull(dob_val):
                    dob_val = dob_val.date()
                else:
                    dob_val = None

                new_candidate = models.Candidate(
                    candidate_id=row_data.get("candidate_id"),
                    household_id=row_data.get("household_id"),
                    name=row_data.get("name"),
                    date_of_birth=dob_val,
                    gender=row_data.get("gender"),
                    highest_education_level=row_data.get("highest_education_level"),
                    degree=row_data.get("degree"),
                    # any_skill_certificate=row_data.get("any_skill_certificate"),
                    digital_tools_used=row_data.get("digital_tools_used"),
                    work_related_skills=row_data.get("work_related_skills"),
                    # Resolves naming mismatch: maps file column 'preferred_job_roles' into DB column 'preferred_opportunity_mode'
                    preferred_opportunity_mode=row_data.get("preferred_job_roles"),
                    preferred_sectors=row_data.get("preferred_sectors"),
                    how_far_will_travel=row_data.get("how_far_will_travel"),
                    support_factors=row_data.get("support_factors"),
                    employment_status=row_data.get("employment_status"),
                    main_reason_not_working=row_data.get("main_reason_not_working"),
                    monthly_income=row_data.get("monthly_income"),
                    hqs_score=row_data.get("hqs_score")
                )
                db.add(new_candidate)

        # =======================================================
        # 3. ATOMIC TRANSACT COMMIT SAVEPOINT
        # =======================================================
        db.commit()
        print("🎉 Processing Complete! All high-insight dimensions are sanitized and committed.")
        
        return {
            "status": "success", 
            "message": "Expanded processing completed smoothly. High-density metrics parsed."
        }

    except Exception as e:
        db.rollback()
        print(f"❌ Critical Cleaning Failure Rollback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Expanded data parsing pipeline crashed: {str(e)}")