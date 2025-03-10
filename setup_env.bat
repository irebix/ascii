@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Environment name
set ENV_NAME=ascii_art

:: Search for conda
echo Searching for conda installation...

:: Method 1: Try where.exe
where conda 2>nul | findstr /i "conda.exe" > temp_conda_path.txt
if %errorlevel% equ 0 (
    for /f "tokens=*" %%a in (temp_conda_path.txt) do (
        echo %%a | findstr /i "Scripts\\conda.exe" > nul
        if !errorlevel! equ 0 (
            set "CONDA_PATH=%%a"
            echo Found conda using where.exe: !CONDA_PATH!
            goto :found_conda
        )
    )
)

:: Method 2: Check CONDA_EXE environment variable
if defined CONDA_EXE (
    if exist "%CONDA_EXE%" (
        set "CONDA_PATH=%CONDA_EXE%"
        echo Found conda from environment variable: !CONDA_PATH!
        goto :found_conda
    )
)

:: Method 3: Check common installation paths
set "PATHS_TO_CHECK=C:\ProgramData\miniconda3;C:\ProgramData\Anaconda3;%USERPROFILE%\miniconda3;%USERPROFILE%\Anaconda3;%ProgramFiles%\miniconda3;%ProgramFiles%\Anaconda3;%ProgramFiles(x86)%\miniconda3;%ProgramFiles(x86)%\Anaconda3"

for %%p in ("%PATHS_TO_CHECK:;=";"%") do (
    set "CHECK_PATH=%%~p\Scripts\conda.exe"
    echo Checking path: !CHECK_PATH!
    if exist "!CHECK_PATH!" (
        set "CONDA_PATH=!CHECK_PATH!"
        echo Found conda in common installation path: !CONDA_PATH!
        goto :found_conda
    )
)

:: If we get here, conda was not found
echo Conda not found. Please make sure Miniconda or Anaconda is installed.
echo Checked methods:
echo - where.exe command
echo - CONDA_EXE environment variable
echo - Common installation paths
if exist temp_conda_path.txt del temp_conda_path.txt
pause
exit /b 1

:found_conda
if exist temp_conda_path.txt del temp_conda_path.txt

:: Initialize conda
call "!CONDA_PATH!" activate base

:: Check current conda environment
echo Current environment: %CONDA_DEFAULT_ENV%

:: Check if environment exists
"%CONDA_PATH%" env list | findstr /C:"%ENV_NAME%" > nul
if %errorlevel% equ 0 (
    echo Found existing environment: %ENV_NAME%
    echo Activating environment...
    call "%CONDA_PATH%" activate %ENV_NAME%
) else (
    echo Creating new conda environment: %ENV_NAME%
    call "%CONDA_PATH%" create -n %ENV_NAME% python=3.9 -y
    if %errorlevel% equ 0 (
        echo Environment created successfully
        call "%CONDA_PATH%" activate %ENV_NAME%
        
        echo Installing dependencies...
        call "%CONDA_PATH%" install -c conda-forge pillow numpy opencv rich -y
        if %errorlevel% equ 0 (
            echo Dependencies installed successfully
        ) else (
            echo Failed to install dependencies. Please check your network connection or install manually.
            pause
            exit /b 1
        )
    ) else (
        echo Failed to create environment
        pause
        exit /b 1
    )
)

:: Check if environment is activated successfully
"%CONDA_PATH%" env list | findstr /C:"%ENV_NAME%.*\*" > nul
if %errorlevel% equ 0 (
    echo.
    echo Environment setup completed!
    echo Active environment: %ENV_NAME%
    echo Python version:
    python --version
    echo.
    echo Installed packages:
    pip list
) else (
    echo Failed to activate environment
    pause
    exit /b 1
) 