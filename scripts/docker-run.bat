@echo off
REM Markdown Foldmarks Generator - Docker Wrapper Script for Windows
REM This script provides a convenient way to run the foldmarks generator in Docker

setlocal enabledelayedexpansion

set IMAGE_NAME=foldmarks-generator
set IMAGE_TAG=latest

REM Get script directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Color codes (limited in cmd, but we'll use echo)
set "INFO=[INFO]"
set "ERROR=[ERROR]"
set "WARNING=[WARNING]"

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo %ERROR% Docker is not installed or not in PATH
    exit /b 1
)

REM Check arguments
if "%~1"=="" (
    echo %ERROR% No arguments provided
    echo Usage: %~nx0 ^<input_file^> [output_file]
    echo.
    echo Examples:
    echo   %~nx0 index.md                    # Modify input file in place
    echo   %~nx0 index.md index_slides.md    # Create new output file
    echo.
    echo Options:
    echo   --build    Force rebuild the Docker image
    exit /b 1
)

REM Handle --build flag
if "%~1"=="--build" (
    echo %INFO% Forcing image rebuild...
    docker build -t %IMAGE_NAME%:%IMAGE_TAG% "%PROJECT_ROOT%"
    echo %INFO% Rebuild complete!
    exit /b 0
)

REM Build image if it doesn't exist
docker image inspect %IMAGE_NAME%:%IMAGE_TAG% >nul 2>&1
if errorlevel 1 (
    echo %INFO% Building Docker image %IMAGE_NAME%:%IMAGE_TAG%...
    docker build -t %IMAGE_NAME%:%IMAGE_TAG% "%PROJECT_ROOT%"
    echo %INFO% Image built successfully!
) else (
    echo %INFO% Using existing image %IMAGE_NAME%:%IMAGE_TAG%
)

REM Get current directory
set WORKSPACE_DIR=%CD%

REM Run the container
echo %INFO% Processing markdown file...
docker run --rm -v "%WORKSPACE_DIR%:/workspace" %IMAGE_NAME%:%IMAGE_TAG% %*

echo %INFO% Done!
