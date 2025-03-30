from sqlalchemy.orm import Session
from . import models, schemas

def get_all_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee_by_id(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(name=employee.name, department=employee.department)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, updated: schemas.EmployeeCreate):
    db_employee = get_employee_by_id(db, employee_id)
    if db_employee:
        db_employee.name = updated.name
        db_employee.department = updated.department
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id)
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
