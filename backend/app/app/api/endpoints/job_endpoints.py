from fastapi import APIRouter, Depends, Form,requests
from sqlalchemy.orm import Session
from app.api import deps
from app.core.config import settings
from datetime import datetime
from app.utils import *

import random


router = APIRouter()

# Add New Jobs
@router.post("/add_job")
async def addJob(db:Session=Depends(deps.get_db),job_title:str=Form(...),
                      job_location:str=Form(...),company_name:str=Form(...),
                      salary_details:str=Form(...),skills:str=Form(...)):
    
    # Check job already Posted or Not
    checkJobExists = db.query(JobDetails).filter(JobDetails.job_title == job_title , 
                                                JobDetails.company_name==company_name,
                                                JobDetails.status == 1).first()
    if checkJobExists:
        return {"status":0,"msg":"Your are already posted this job"}
    else:
        createJob = JobDetails(
            job_tilte=job_title,
            job_location=job_location,
            company_name=company_name,
            salary_details=salary_details,
            skills=skills,
            status = 1,
            created_at=datetime.now()

        ) 
        db.add(createJob)
        db.commit()
        db.refresh(createJob)
        return {"status":1,"msg":"Added Successfully"}


#List Jobs -> Job listed  based on Job title, Location and Company name
@router.get("/list_jobs")
def listJobs(*, db: Session = Depends(deps.get_db),job_title:str=Form(None),
                      job_location:str=Form(None),company_name:str=Form(None)):

    getJobs=db.query(JobDetails).filter(JobDetails.status == 1)

    if job_title:
        getJobs=getJobs.filter(JobDetails.job_title.like(job_title))

    if job_location:
        getJobs=getJobs.filter(JobDetails.job_location.like(job_location))

    if company_name:
        getJobs=getJobs.filter(JobDetails.company_name.like(company_name))
    
    getJobs=getJobs.order_by(JobDetails.created_at.desc()).all()

    listOfJobs=[]
    for jobs in getJobs:
        listOfJobs.append({"job_id":jobs.id,
                            "job_title":jobs.job_title,
                            "job_location":jobs.job_location,
                            "company_name":jobs.company_name,
                            "posted_date":jobs.created_at
                            })
    
    
    return {"status":1,"msg":"Success","data":listOfJobs}  

# Update Job
@router.post("/update_job")
def updateJob(db: Session = Depends(deps.get_db),job_id:int=Form(...),
                                                    job_title:str=Form(None),
                                                    job_location:str=Form(None),
                                                    company_name:str=Form(None),
                                                    salary_details:str=Form(None),
                                                    skills:str=Form(None)):
    # Check Job
    check_job=db.query(JobDetails).filter(JobDetails.id == job_id).first()
    
    if not check_job:
       return {"status":0,"msg":"Invalid Job"}

    # Update Job
    check_job.job_title = name
    check_job.job_location = job_location
    check_job.company_name = company_name
    check_job.salary_details = salary_details
    check_job.skills = skills
    db.commit()

    return {"status":1,"msg":"Updated Successfully"} 


# Delete Job
@router.post("/delete_job")
def deleteJob(db: Session = Depends(deps.get_db),job_id:int=Form(...)):
    # Check Job
    check_job=db.query(JobDetails).filter(JobDetails.id == job_id).first()
    
    if not check_job:
       return {"status":0,"msg":"Invalid Job"}
    # Delete Job
    check_job.status = -1 # Status -1  means deleted
    db.commit()
    return {"status":1,"msg":"Deleted Successfully"}     

  