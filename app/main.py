from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from faker import Faker
from . import crud, schemas
from tenacity import retry, wait_fixed, stop_after_attempt
from sqlalchemy.exc import OperationalError
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os

security = HTTPBearer()
API_TOKEN = "supersecrettoken"  # move to .env later if needed

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")

@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def init_db():
    try:
        models.Base.metadata.create_all(bind=engine)
        print("✅ Database initialized.")
    except OperationalError as e:
        print("⏳ Waiting for database to be ready...")
        raise e

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/employees/", response_model=schemas.EmployeeRead, dependencies=[Depends(verify_token)])
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)


@app.get("/employees/", response_model=list[schemas.EmployeeRead], dependencies=[Depends(verify_token)])
def read_employees(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)


@app.get("/employees/{employee_id}", response_model=schemas.EmployeeRead, dependencies=[Depends(verify_token)])
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_id(db, employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.put("/employees/{employee_id}", response_model=schemas.EmployeeRead, dependencies=[Depends(verify_token)])
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db, employee_id, employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@app.delete("/employees/{employee_id}", dependencies=[Depends(verify_token)])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_employee(db, employee_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

fake = Faker()

@app.on_event("startup")
def populate_employees():
    init_db()  # 👈 Add this
    db = SessionLocal()
    try:
        employees = crud.get_all_employees(db)
        if len(employees) == 0:
            for _ in range(500):
                name = fake.name()
                department = fake.job()
                employee = schemas.EmployeeCreate(name=name, department=department)
                crud.create_employee(db, employee)
            print("✅ Inserted 500 fake employees.")
        else:
            print("ℹ️ Employees already exist. Skipping population.")
    finally:
        db.close()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
