@echo off
echo ==============================================================================
echo Travel Agency Tourism Trend Analysis - Python Data Science Pipeline
echo Student: Kishor K (RegNo: 732925ITR051) ^| Class: 25IT3A
echo ==============================================================================
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe analytics\tourism_trend_analysis.py
) else (
    python analytics\tourism_trend_analysis.py
)
pause
