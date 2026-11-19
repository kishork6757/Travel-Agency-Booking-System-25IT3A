@echo off
echo ==============================================================================
echo Wanderlust Travel Agency - Fullstack Web Application (Flask + Tailwind)
echo Student: Kishor K (RegNo: 732925ITR051) ^| Class: 25IT3A
echo ==============================================================================
echo Starting Fullstack REST API and Web Server on http://127.0.0.1:5000...
if exist ".venv\Scripts\python.exe" (
    start http://127.0.0.1:5000
    .venv\Scripts\python.exe server.py
) else (
    start http://127.0.0.1:5000
    python server.py
)
pause
