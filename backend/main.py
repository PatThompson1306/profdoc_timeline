#imports
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# create the app and mount the static files
app = FastAPI()
app.mount("/frontend", StaticFiles(directory = "../frontend"), name = "frontend")

# function defining the root endpoint to serve the index.html file
@app.get("/")
def root():
    return FileResponse("../frontend/index.html")