from sqlalchemy.orm import Session
from db.users_db import JobDb, UserDb


def get_all_jobs(db: Session):
    return db.query(JobDb).all()


def get_by_company(db: Session, _company):
    query = db.query(JobDb).filter(JobDb.company == _company).first()
    return query


def get_by_id(db: Session, _id):
    query = db.query(JobDb).filter(JobDb.id == _id).first()
    return query


def add_jobs(db: Session, _title, _company, _location, _description, _user_id):
    new_job = JobDb(title= _title, company= _company, location = _location, description= _description, user_id= _user_id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


def add_jobs_td(db: Session):
    add_jobs(db, "villain", "sith", "death star", "looking to control the republic", 1)
    add_jobs(db, "billionaire", "wayne enterprise", "gotham city", "funding tech to help the world", 2)
    add_jobs(db, "soldier", "the avengers", "queens new york", "earths protectors", 3)


def update_job(db: Session, _id, _title, _company, _location, _description):
    job_to_update = db.query(JobDb).filter(JobDb.id == _id).first()
    

    if _title != '':
        job_to_update.title = _title

    if _description != '':
        job_to_update.description = _description

    if _company != '':
        job_to_update.company = _company

    if _location != '':
        job_to_update.location = _location


    db.commit()


def delete_job(db: Session, _id):
    db.query(JobDb).filter(JobDb.id == _id).delete()
    db.commit()