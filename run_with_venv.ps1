# Run the Task Management System with virtual environment
# Usage: .\run_with_venv.ps1
# Or in PowerShell: cd task_management_system; .\run_with_venv.ps1

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Create venv if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate venv (PowerShell)
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "$projectRoot\venv\Scripts\Activate.ps1"

# Install dependencies if needed
$flaskInstalled = pip show Flask 2>$null
if (-not $flaskInstalled) {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
}

# Run the app
Write-Host "Starting Flask server at http://127.0.0.1:5000 ..." -ForegroundColor Green
python run.py
