@echo off
cd /d "%~dp0.."
echo Verifying Python syntax and running tests...
python -c "import glob, py_compile; [py_compile.compile(f, doraise=True) for f in glob.glob('./**/*.py', recursive=True)]"
if errorlevel 1 (
    echo Python syntax verification failed!
    pause
    exit /b 1
)

python -m unittest discover -s tests
if errorlevel 1 (
    echo Tests failed!
    pause
    exit /b 1
)

echo Verification successful!
pause
