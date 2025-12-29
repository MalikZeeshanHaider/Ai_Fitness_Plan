@echo off
title AI Gym Workout Recommendation System
echo ============================================
echo    AI Gym Workout Recommendation System
echo ============================================
echo.

:: Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then install dependencies: pip install -r requirements.txt
    pause
    exit /b 1
)

:: Activate virtual environment
echo [1/2] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Run the Streamlit application
echo [2/2] Starting Streamlit application...
echo.
echo ============================================
echo    Access the app at: http://localhost:8502
echo    Press Ctrl+C to stop the server
echo ============================================
echo.

streamlit run app.py --server.port 8502

:: Deactivate on exit
deactivate
