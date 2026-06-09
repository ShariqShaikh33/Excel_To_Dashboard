from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Household(Base):
    __tablename__ = "households"

    household_id = Column(String, primary_key=True, index=True)
    household_type = Column(String, nullable=True)
    
    # NEW GEOGRAPHIC TRACKING
    # street_and_locality_name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    territory_name = Column(String, nullable=True)
    
    district = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    willingness = Column(String, nullable=True)
    
    # ECONOMICS & VULNERABILITY
    average_monthly_income = Column(Float, default=0.0)
    # monthly_expenses_including_housing_and_food = Column(Float, default=0.0) # NEW
    # members_age_18_to_40 = Column(Integer, default=0) # NEW
    urgent_candidate_count = Column(Integer, default=0)
    
    # AUDIT TRAIL & SYSTEM CORES
    status = Column(String, nullable=True)
    created_by_name = Column(String, nullable=True) # NEW
    # supervisor_name = Column(String, nullable=True) # NEW
    # household_rejected_reason = Column(String, nullable=True) # NEW
    hqs_score = Column(Float, nullable=True)

    candidates = relationship("Candidate", back_populates="household", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id = Column(String, primary_key=True, index=True)
    household_id = Column(String, ForeignKey("households.household_id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    
    # DYNAMIC SKILLS & EDUCATION EXPANSION
    highest_education_level = Column(String, nullable=True)
    degree = Column(String, nullable=True) # NEW
    # any_skill_certificate = Column(String, nullable=True) # NEW
    digital_tools_used = Column(String, nullable=True) # NEW
    work_related_skills = Column(String, nullable=True) # NEW
    
    # INTENT & COMMUTE METRICS
    preferred_opportunity_mode = Column(String, nullable=True) # Maps Preferred Job Roles
    preferred_sectors = Column(String, nullable=True) # NEW
    how_far_will_travel = Column(String, nullable=True) # NEW
    support_factors = Column(String, nullable=True) # NEW
    
    # EMPLOYMENT & BARRIERS TRACKING
    employment_status = Column(String, nullable=True)
    main_reason_not_working = Column(String, nullable=True) # NEW
    monthly_income = Column(Float, default=0.0)
    hqs_score = Column(Float, nullable=True)

    household = relationship("Household", back_populates="candidates")