@echo off
echo ==============================================================================
echo Travel Agency Booking and Tourism Trend Analysis System - Web Application
echo Student: Kishor K (RegNo: 732925ITR051) ^| Class: 25IT3A
echo ==============================================================================
echo Launching local interactive web application...
if exist ".venv\Scripts\streamlit.exe" (
    .venv\Scripts\streamlit.exe run app.py
) else (
    streamlit run app.py
)
pause
