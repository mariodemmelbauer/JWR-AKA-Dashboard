@echo off
echo Starting AKA Teams Dashboard...
echo.
echo Make sure you have installed the requirements:
echo pip install -r requirements_aka.txt
echo.
echo Starting Streamlit...
python -m streamlit run aka_dashboard.py
pause
