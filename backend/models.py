# backend/models.py
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Household(Base):
    __tablename__ = "households"

    # Excel Header: "Household ID"
    household_id = Column(String, primary_key=True, index=True)
    
    # Excel Header: "Household Type"
    household_type = Column(String, nullable=True)
    
    # Excel Header: "District"
    district = Column(String, nullable=True)
    
    # Excel Header: "Pincode"
    pincode = Column(String, nullable=True)
    
    # Excel Header: "Willingness"
    willingness = Column(String, nullable=True)
    
    # Excel Header: "Average Monthly Income"
    average_monthly_income = Column(Float, default=0.0)
    
    # Excel Header: "Urgent Candidate Count"
    urgent_candidate_count = Column(Integer, default=0)
    
    # Excel Header: "Status"
    status = Column(String, nullable=True)
    
    # Excel Header: "HQS Score"
    hqs_score = Column(Float, nullable=True)

    # Relationship back link to all candidates living in this household
    candidates = relationship("Candidate", back_populates="household", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    # Excel Header: "Candidate ID"
    candidate_id = Column(String, primary_key=True, index=True)
    
    # Excel Header: "Household ID" (Foreign key relationship connecting to parent table)
    household_id = Column(String, ForeignKey("households.household_id", ondelete="CASCADE"), nullable=False)
    
    # Excel Header: "Name"
    name = Column(String, nullable=True) # Changed to True to protect against empty rows
    
    # Excel Header: "Date of Birth"
    date_of_birth = Column(Date, nullable=True) # Changed to True to handle missing data profiles safely
    
    # Excel Header: "Gender"
    gender = Column(String, nullable=True)
    
    # Excel Header: "Highest Education Level"
    highest_education_level = Column(String, nullable=True)
    
    # Excel Header: "Employment Status"
    employment_status = Column(String, nullable=True)
    
    # Excel Header: "Monthly Income"
    monthly_income = Column(Float, default=0.0)
    
    # Excel Header: "Preferred Job Roles" 
    # (Maps directly over from 'preferred_job_roles' string extracted during upload)
    preferred_opportunity_mode = Column(String, nullable=True)
    
    # Excel Header: "HQS Score"
    hqs_score = Column(Float, nullable=True)

    # Relationship link attaching candidate profile up to their specific home entry
    household = relationship("Household", back_populates="candidates")