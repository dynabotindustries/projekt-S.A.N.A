@echo off
setlocal

REM Path to the marker file
set marker_file=setup_done.marker

REM Check if the marker file exists
if exist %marker_file% (
    echo Setup already completed. Running the application...
) else (
    echo Performing initial setup...

    REM Check if Python is installed
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python is not installed. Please install Python to continue.
        exit /b 1
    )

    REM Ensure pip is up to date
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip

    REM Install required packages
    pip install pyqt5
    pip install pywhatkit
    pip install wikipedia-api
    pip install wolframalpha
    pip install pyttsx3
    pip install SpeechRecognition

    REM Create the marker file to indicate setup is done
    echo Setup completed on %date% at %time% > %marker_file%
)

REM Run the Python script
python sana.py

endlocal
