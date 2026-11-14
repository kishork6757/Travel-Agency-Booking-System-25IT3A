@echo off
echo ==============================================================================
echo Travel Agency Booking and Tourism Trend Analysis System
echo Student: Kishor K (RegNo: 732925ITR051) ^| Class: 25IT3A
echo ==============================================================================
echo Compiling Java source files...
if not exist "bin" mkdir bin
javac -cp "lib/*" -d bin src/com/travel/model/*.java src/com/travel/exception/*.java src/com/travel/util/*.java src/com/travel/dao/*.java src/com/travel/service/*.java src/com/travel/Main.java

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Compilation failed!
    pause
    exit /b %ERRORLEVEL%
)

echo [SUCCESS] Compilation successful!
echo Starting application...
java -cp "bin;lib/*" com.travel.Main
pause
