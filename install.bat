@echo off
echo Installing virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing required packages...
pip install -r requirements.txt

echo Setup is complete!
pause