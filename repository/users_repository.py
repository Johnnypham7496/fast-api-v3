from sqlalchemy.orm import Session
from db.users_db import UserDb, JobDb



def get_all_users(db: Session):
    return db.query(UserDb).all()


def add_user(db: Session, _username, _email, _role):
    new_user = UserDb(username = _username, email = _email, role = _role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def add_user_td(db: Session):
    add_user(db, "darth.vader", "darth.vader@gmail.com", "villain")
    add_user(db, "bruce.wayne", "batman@gmail.com", "hero")
    add_user(db, "steve.rogers", "captain.america@gmail.com", "hero")


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