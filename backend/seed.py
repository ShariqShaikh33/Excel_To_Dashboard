# seed.py
import datetime
import random
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

# 🔴 CRITICAL FIX: Tell SQLAlchemy to drop tables first, then recreate them 
# This forcefully updates the columns inside your local Postgres database!
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

TOTAL_RECORDS = 50000
BATCH_SIZE = 5000

GENDERS = ["Male", "Female"]
EDUCATION_LEVELS = ["Middle School", "SSC (10th - 11th std)", "HSC (12th std)", "Undergraduate degree", "Postgraduate degree"]
OPPORTUNITY_MODES = ["Job Only", "Work From Home", "Apprenticeship", "Skill Training"]
HOUSEHOLD_TYPES = ["Apartment/Housing Society", "Chawl", "Independent House", "Slum Cluster"]
DISTRICTS = ["Mumbai Suburban", "Mumbai City", "Thane", "Palghar"]
PINCODES = ["400054", "400052", "400050", "400051", "400053"]
STATUSES = ["COMPLETED", "IN_PROGRESS", "REJECTED"]

# 🟢 ADD THIS NEW LIST FOR EMPLOYMENT STATUSES
EMPLOYMENT_STATUSES = ["Employed full-time (salaried)", "Unemployed", "Self-employed / Business Owner", "Student"]

def generate_mock_data():
    print("Running the seed.py script")
    db: Session = SessionLocal()
    print(f"Refreshing schema and starting database seeding for {TOTAL_RECORDS} rows...")
    
    household_ids = [f"HH_{i:06d}" for i in range(1, TOTAL_RECORDS + 1)]
    
    try:
        households_batch = []
        candidates_batch = []
        start_date = datetime.date(1980, 1, 1)

        for i in range(TOTAL_RECORDS):
            hh_id = household_ids[i]
            income = random.choice([0.0, 15000.0, 18000.0, 20000.0, 25000.0, 30000.0, 45000.0, 60000.0])
            
            household = models.Household(
                household_id=hh_id,
                household_type=random.choice(HOUSEHOLD_TYPES),
                district=random.choice(DISTRICTS),
                pincode=random.choice(PINCODES),
                willingness="Yes" if random.random() > 0.1 else "No",
                average_monthly_income=income,
                urgent_candidate_count=random.choice([0, 1, 2]),
                status=random.choice(STATUSES),
                hqs_score=round(random.uniform(85.0, 100.0), 2)
            )
            households_batch.append(household)

            random_days = random.randint(0, 12000)
            dob = start_date + datetime.timedelta(days=random_days)
            
            candidate = models.Candidate(
                candidate_id=f"CAND_{i:06d}",
                household_id=hh_id,
                name=f"Mock Name {i}",
                date_of_birth=dob,
                gender=random.choice(GENDERS),
                highest_education_level=random.choice(EDUCATION_LEVELS),
                monthly_income=income if random.random() > 0.3 else 0.0,
                preferred_opportunity_mode=random.choice(OPPORTUNITY_MODES),
                employment_status=random.choice(EMPLOYMENT_STATUSES),  # 🟢 POPULATE THE NEW COLUMN HERE
                hqs_score=round(random.uniform(90.0, 100.0), 2)
            )
            candidates_batch.append(candidate)

            if (i + 1) % BATCH_SIZE == 0:
                db.bulk_save_objects(households_batch)
                db.bulk_save_objects(candidates_batch)
                db.commit()
                households_batch.clear()
                candidates_batch.clear()
                print(f"Inserted {i + 1}/{TOTAL_RECORDS} rows safely...")

        print("Database schema updated and successfully packed with 50,000 clean rows!")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_mock_data()