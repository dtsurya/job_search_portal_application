from sqlalchemy import  Column, Integer, String, DateTime, ForeignKey,TEXT,DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT

from app.db.base_class import Base

class JobDetails(Base):
    __tablename__="job_details"
    id = Column(Integer,primary_key=True)
    job_tilte = Column(String(255))
    job_location= Column(String(250))
    company_name = Column(String(250))
    salary_details=Column(String(100))
    skills=Column(TEXT)
    status = Column(TINYINT)
    created_at=Column(DateTime)


    