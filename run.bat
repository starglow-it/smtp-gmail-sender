@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running python script...
python src\main.py
pause
