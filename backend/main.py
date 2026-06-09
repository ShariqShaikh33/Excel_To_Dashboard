# main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy import func, case, cast, Float
from sqlalchemy.orm import Session
from routers import uploadfile,section1,section2,section3
import models
from database import engine, get_db
import datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your React server to connect seamlessly
    allow_credentials=True,
    allow_methods=["*"],  # Allows all actions (GET, POST, etc.)
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend infrastructure is online"}

@app.get("/api/test-data")
def get_sample_data(db: Session = Depends(get_db)):
    # Fetch just the first 5 records from the database
    candidates_sample = db.query(models.Candidate).limit(5).all()
    households_sample = db.query(models.Household).limit(5).all()
    
    return {
        "total_records_requested": 5,
        "candidates": candidates_sample,
        "households": households_sample
    }

def pct_of(numerator, denominator):
    return func.round(cast(100.0 * numerator / func.nullif(denominator, 0), Float), 2)

# models.Base.metadata.drop_all(bind=engine)
# models.Base.metadata.create_all(bind=engine)

app.include_router(uploadfile.router)
app.include_router(section1.router)
app.include_router(section2.router)
app.include_router(section3.router)

# # ==========================================
# # SECTION 4: AREA COVERAGE
# # ==========================================
# @app.get("/api/dashboard/section4")
# def get_section_4_data(db: Session = Depends(get_db)):
#     total_households = db.query(models.Household).count()
#     if total_households == 0:
#         return {"error": "No household data available"}

#     # 4.1 District/Area coverage metrics card array
#     area_raw = db.query(
#         models.Household.district.label("area_name"),
#         func.count(models.Household.household_id).label("household_count")
#     ).group_by(models.Household.district).all()

#     area_coverage_cards = []
#     for row in area_raw:
#         area_coverage_cards.append({
#             "area_name": row.area_name if row.area_name else "Unknown Region",
#             "no_of_household": row.household_count,
#             "percentage": round((row.household_count / total_households) * 100, 2)
#         })

#     # 4.2 High density region matrix with HQS and operational conversions
#     region_raw = db.query(
#         models.Household.district.label("region"),
#         func.count(models.Household.household_id).label("total_hh"),
#         func.count(case((models.Household.status == 'COMPLETED', 1))).label("approved_hh"),
#         func.count(case((models.Household.status == 'REJECTED', 1))).label("refused_hh"),
#         func.avg(models.Household.hqs_score).label("avg_hqs")
#     ).group_by(models.Household.district).all()

#     region_summary_table = []
#     for row in region_raw:
#         region_summary_table.append({
#             "region": row.region if row.region else "Unknown Region",
#             "household_number": row.total_hh,
#             "percentage": round((row.total_hh / total_households) * 100, 2),
#             "approved_percentage": pct_of(row.approved_hh, row.total_hh),
#             "refusal_percentage": pct_of(row.refused_hh, row.total_hh),
#             "avg_hqs": round(row.avg_hqs, 2) if row.avg_hqs is not None else 0.0
#         })

#     return {
#         "area_coverage_cards": area_coverage_cards,
#         "region_summary_table": region_summary_table
#     }


# # ==========================================
# # SECTION 5: HOUSING CONTEXT
# # ==========================================
# @app.get("/api/dashboard/section5")
# def get_section_5_data(db: Session = Depends(get_db)):
#     total_households = db.query(models.Household).count()
#     total_residents = db.query(models.Candidate).count()

#     # 5.1 Comprehensive housing context table + calculated spatial metrics
#     housing_raw = db.query(
#         models.Household.household_type.label("housing_type"),
#         func.count(models.Household.household_id).label("total_hh"),
#         func.count(case((models.Household.status == 'COMPLETED', 1))).label("approved_hh"),
#         func.count(case((models.Household.status == 'REJECTED', 1))).label("refused_hh"),
#         func.avg(models.Household.hqs_score).label("avg_hqs"),
#         func.percentile_cont(0.5).within_group(models.Household.average_monthly_income.asc()).label("median_income")
#     ).group_by(models.Household.household_type).all()

#     household_type_breakdown_table = []
#     for row in housing_raw:
#         household_type_breakdown_table.append({
#             "housing_type": row.housing_type if row.housing_type else "Other",
#             "household_number": row.total_hh,
#             "percentage": round((row.total_hh / total_households) * 100, 2) if total_households > 0 else 0,
#             "approved_percentage": pct_of(row.approved_hh, row.total_hh),
#             "refusal_percentage": pct_of(row.refused_hh, row.total_hh),
#             "avg_hqs": round(row.avg_hqs, 2) if row.avg_hqs is not None else 0.0,
#             "median_income": round(row.median_income, 2) if row.median_income is not None else 0.0
#         })

#     # 5.2 Residents demographic concentration grouped by house structure
#     # This requires an implicit SQL JOIN between Candidate and Household
#     residents_raw = db.query(
#         models.Household.household_type.label("category"),
#         func.count(models.Candidate.candidate_id).label("resident_count")
#     ).join(models.Candidate, models.Household.household_id == models.Candidate.household_id)\
#      .group_by(models.Household.household_type).all()

#     residents_by_housing_type_table = []
#     for row in residents_raw:
#         residents_by_housing_type_table.append({
#             "category": row.category if row.category else "Other",
#             "count": row.resident_count,
#             "percentage": round((row.resident_count / total_residents) * 100, 2) if total_residents > 0 else 0
#         })

#     return {
#         "household_type_breakdown_table": household_type_breakdown_table,
#         "residents_by_housing_type_table": residents_by_housing_type_table
#     }


# # ==========================================
# # SECTION 6: AGE DISTRIBUTION
# # ==========================================
# @app.get("/api/dashboard/section6")
# def get_section_6_data(db: Session = Depends(get_db)):
#     # SQL logic to derive age directly from Date of Birth relative to current time
#     current_year = datetime.date.today().year
#     age_expression = current_year - func.extract('year', models.Candidate.date_of_birth)

#     # 6.1 Meta Metrics Cards (Total, Median, Mean)
#     total_residents = db.query(models.Candidate).count()
#     if total_residents == 0:
#         return {"error": "No residents available for demographic age testing"}

#     mean_age = db.query(func.avg(age_expression)).scalar() or 0.0
#     median_age = db.query(func.percentile_cont(0.5).within_group(age_expression.asc())).scalar() or 0.0

#     age_meta_cards = {
#         "total_residents": total_residents,
#         "median_age": round(median_age, 1),
#         "mean_age": round(mean_age, 1)
#     }

#     # SQL Case structures to dynamically segment candidates into standard analytical groups
#     age_band_case = case(
#         (age_expression < 18, 'Under 18'),
#         (age_expression.between(18, 25), '18-25'),
#         (age_expression.between(26, 35), '26-35'),
#         (age_expression.between(36, 50), '36-50'),
#         (age_expression.between(51, 65), '51-65'),
#         else_='65+'
#     ).label("age_band")

#     # 6.2 Table of Age Bands
#     age_bands_raw = db.query(
#         age_band_case,
#         func.count(models.Candidate.candidate_id).label("count")
#     ).group_by("age_band").all()

#     age_band_table = []
#     for row in age_bands_raw:
#         age_band_table.append({
#             "age_band": row.age_band,
#             "count": row.count,
#             "percentage": round((row.count / total_residents) * 100, 2)
#         })

#     # 6.3 Table of median income by age band segment
#     age_income_raw = db.query(
#         age_band_case,
#         func.percentile_cont(0.5).within_group(models.Candidate.monthly_income.asc()).label("median_income")
#     ).group_by("age_band").all()

#     median_income_by_age_band_table = []
#     for row in age_income_raw:
#         median_income_by_age_band_table.append({
#             "age_band": row.age_band,
#             "median_income": round(row.median_income, 2) if row.median_income is not None else 0.0
#         })

#     return {
#         "age_meta_cards": age_meta_cards,
#         "age_band_table": age_band_table,
#         "median_income_by_age_band_table": median_income_by_age_band_table
#     }