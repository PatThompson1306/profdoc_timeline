# imports
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
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


origins = [
    "http://localhost:8000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/workloads/", response_model = list[WorkLoad])
def read_workloads():
    """
    Retrieve all workload entries from the modules table.
    Executes a SELECT query to fetch all records from the modules table, 
    converts each record into a WorkLoad object, and returns a list of these objects as the response.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM modules')
    results = [WorkLoad(**dict(row)) for row in cursor.fetchall()]
    conn.close()
    return results


@app.delete("/workloads/{workload_id}", status_code = 204, response_model = None)
def delete_workload(workload_id: int):
    """
    Delete a workload entry from the modules table by its ID.
    Executes a DELETE query to remove the record with the specified ID from the modules table. 
    Returns a 204 No Content status code upon successful deletion.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM modules WHERE id = ?', (workload_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 404, detail = "Workload not found")
    conn.commit()
    conn.close()


@app.put("/workloads/{workload_id}", response_model = WorkLoad)
def update_workload(workload_id: int, workload: WorkLoadCreate):
    """
    Update an existing workload entry in the modules table by its ID.
    Executes an UPDATE query to modify the record with the specified ID based on the provided WorkLoadCreate data. 
    Returns the updated record as a WorkLoad object, including the database-generated id, created_at, and updated_at fields.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE modules
        SET module_name = ?, academic_year = ?, term_or_semester = ?, study_type = ?, 
            start_date = ?, end_date = ?, chart_colour = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
                   ''', 
        (workload.module_name, workload.academic_year.value, workload.term_or_semester.value, workload.study_type.value, 
        workload.start_date.isoformat(), workload.end_date.isoformat(), workload.chart_colour, workload.notes, workload_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 404, detail = "Workload not found")
    conn.commit()
    cursor.execute('SELECT * FROM modules WHERE id = ?', (workload_id,))
    result = WorkLoad(**dict(cursor.fetchone()))
    conn.close()
    return result
    