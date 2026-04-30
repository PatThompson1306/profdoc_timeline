# imports
from sys import modules

from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse 
from contextlib import asynccontextmanager
from database import create_table, get_connection # import functions from database.py 
from models import WorkLoadCreate, WorkLoad # import the WorkLoadCreate and WorkLoad models from models.py


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function to create the database table at the start of the app.
    This function is called when the FastAPI application starts. 
    It ensures that the necessary database table is created before handling any requests. 
    The create_table() function is responsible for setting up the database schema, 
    and it is called within this lifespan context to ensure that the database is ready for use when the application is running.
    """
    create_table()
    yield


# create the app and mount the static files
app = FastAPI(lifespan=lifespan)
app.mount("/frontend", StaticFiles(directory = "../frontend"), name = "frontend")


@app.get("/")
def root():
    """
    Root endpoint to serve the index.html file.
    When a GET request is made to the root URL ("/"), this function is called. 
    It returns the index.html file located in the ../frontend directory as a response.
    """
    return FileResponse("../frontend/index.html")


@app.post("/workloads/", response_model = WorkLoad, status_code = 201) 
def create_workload(workload: WorkLoadCreate): 
    """
    Create a new workload entry in the modules table.
    Accepts a WorkLoadCreate object in the request body. Enum fields are stored
    as their string values and date fields are converted to ISO 8601 format before
    insertion. The database assigns the id and timestamps automatically.
    Returns the newly created record as a WorkLoad object, including the
    database-generated id, created_at, and updated_at fields.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO modules (module_name, academic_year, term_or_semester, study_type, 
                   start_date, end_date, chart_colour, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (workload.module_name, workload.academic_year.value, workload.term_or_semester.value, workload.study_type.value, 
          workload.start_date.isoformat(), workload.end_date.isoformat(), workload.chart_colour, workload.notes))
    conn.commit()
    cursor.execute('SELECT * FROM modules WHERE id = ?', (cursor.lastrowid,))
    result = WorkLoad(**dict(cursor.fetchone()))
    conn.close()
    return result
