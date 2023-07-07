from sqlalchemy.orm import Session
from db.users_db import JobDb


def get_all_jobs(db: Session):
    return db.query(JobDb).all()


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