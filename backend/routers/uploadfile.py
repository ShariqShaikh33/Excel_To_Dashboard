# backend/routers/upload.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import io
import models
from database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Data Ingestion & Upload"]
)

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Read the uploaded spreadsheet file into memory buffer
    contents = await file.read()
    buffer = io.BytesIO(contents)
    
    try:
        xls = pd.ExcelFile(buffer)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Excel file structure: {str(e)}")

    # =======================================================
    # 2. CLEAR THE EXISTING DATABASE ENTRIES (ORDER MATTERS)
    # =======================================================
    try:
        print("Wiping old database records...")
        # Delete candidates first to avoid breaking foreign key constraints on households
        db.query(models.Candidate).delete()
        db.query(models.Household).delete()
        db.flush() 
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear database: {str(e)}")
    
    # =======================================================
    # 3. READ EXCEL SHEETS AND POPULATE NEW ENTRIES
    # =======================================================
    try:
        # ---------------------------------------------------
        # A. Process Households Sheet (Parent Table)
        # ---------------------------------------------------
        if 'Households' in xls.sheet_names:
            df_households = pd.read_excel(xls, 'Households')
            
            # Standardize column headers to lowercase and replace spaces with underscores
            df_households.columns = [c.lower().replace(' ', '_') for c in df_households.columns]
            
            for _, row in df_households.iterrows():
                # Map empty/blank cell markers safely to Python None (SQL NULL)
                row_data = row.where(pd.notnull(row), None).to_dict()
                
                household_dict = {
                    "household_id": row_data.get("household_id"),
                    "household_type": row_data.get("household_type"),
                    "district": row_data.get("district"),
                    # Force pincodes to clean strings so floating points like .0 don't generate
                    "pincode": str(int(row_data.get("pincode"))) if row_data.get("pincode") is not None else None,
                    "willingness": row_data.get("willingness"),
                    "average_monthly_income": float(row_data.get("average_monthly_income")) if row_data.get("average_monthly_income") is not None else 0.0,
                    "urgent_candidate_count": int(row_data.get("urgent_candidate_count")) if row_data.get("urgent_candidate_count") is not None else 0,
                    "status": row_data.get("status"),
                    "hqs_score": float(row_data.get("hqs_score")) if row_data.get("hqs_score") is not None else None
                }
                
                new_house = models.Household(**household_dict)
                db.add(new_house)
                
            db.flush() # Sync primary keys to memory so the upcoming candidate rows can map safely

        # ---------------------------------------------------
        # B. Process Candidates Sheet (Child Table)
        # ---------------------------------------------------
        if 'Candidates' in xls.sheet_names:
            df_candidates = pd.read_excel(xls, 'Candidates')
            df_candidates.columns = [c.lower().replace(' ', '_') for c in df_candidates.columns]
            
            for _, row in df_candidates.iterrows():
                row_data = row.where(pd.notnull(row), None).to_dict()
                
                # Format timestamp metrics to true Python datetime.date format
                dob_value = row_data.get("date_of_birth")
                if dob_value is not None:
                    dob_value = pd.to_datetime(dob_value).date()

                # Clean and isolate column inputs explicitly to prevent argument crashes
                candidate_dict = {
                    "candidate_id": row_data.get("candidate_id"),
                    "household_id": row_data.get("household_id"),
                    "name": row_data.get("name"),
                    "date_of_birth": dob_value,
                    "gender": row_data.get("gender"),
                    "highest_education_level": row_data.get("highest_education_level"),
                    "employment_status": row_data.get("employment_status"),
                    "monthly_income": float(row_data.get("monthly_income")) if row_data.get("monthly_income") is not None else 0.0,
                    # Crucial Map: Captures 'preferred_job_roles' from the Excel layout structure
                    "preferred_opportunity_mode": row_data.get("preferred_job_roles"),
                    "hqs_score": float(row_data.get("hqs_score")) if row_data.get("hqs_score") is not None else None
                }
                
                new_candidate = models.Candidate(**candidate_dict)
                db.add(new_candidate)

        # =======================================================
        # 4. LOCK AND COMMIT THE DATA CHANGES
        # =======================================================
        db.commit()
        print("🎉 Database successfully cleared and refreshed with fresh upload records!")
        
        return {"status": "success", "message": "Database wiped and completely refreshed with real Excel values."}

    except Exception as e:
        db.rollback() # Safely roll back data deletion steps if parsing drops an anomaly error
        print(f"❌ Ingestion failure rollback executed. Details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process and ingest spreadsheet file: {str(e)}")