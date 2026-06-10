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
import os
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    # Render automatically injects the PORT environment variable.
    # We read it as an integer, defaulting to 8000 for local development.
    port = int(os.getenv("PORT", 8000))
    
    # CRITICAL: Host must be "0.0.0.0" in production so Render can route traffic to it.
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

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
