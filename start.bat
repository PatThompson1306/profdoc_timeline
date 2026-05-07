@echo off
cd /d "%~dp0backend"
call conda activate timeline_app
start http://localhost:8000
uvicorn main:app