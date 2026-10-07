$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $root "backend"
$frontendPath = Join-Path $root "frontend"
$venvPython = Join-Path $backendPath ".venv\Scripts\python.exe"
$modelPath = Join-Path $root "models\liar_text_model.joblib"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating the project Python environment..." -ForegroundColor Cyan
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -m venv (Join-Path $backendPath ".venv")
    } else {
        & python -m venv (Join-Path $backendPath ".venv")
    }
}

if (-not (Test-Path $venvPython)) {
    throw "Could not create the backend Python environment. Install Python 3 and retry."
}

Write-Host "Checking backend dependencies..." -ForegroundColor Cyan
& $venvPython -c "import fastapi, uvicorn, sqlalchemy, pydantic_settings, networkx, sklearn, joblib" 2>$null
if ($LASTEXITCODE -ne 0) {
    & $venvPython -m pip install -r (Join-Path $backendPath "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "Backend dependency installation failed." }
}

if (-not (Test-Path $modelPath)) {
    Write-Host "Training the local 800-example LIAR model..." -ForegroundColor Cyan
    & $venvPython (Join-Path $root "scripts\train_model.py")
    if ($LASTEXITCODE -ne 0) { throw "Dataset preparation or model training failed." }
}

if (-not (Test-Path (Join-Path $frontendPath "node_modules"))) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    npm --prefix $frontendPath install
    if ($LASTEXITCODE -ne 0) { throw "Frontend dependency installation failed." }
}

$backendReady = $false
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 2 | Out-Null
    $backendReady = $true
    Write-Host "Backend is already running." -ForegroundColor DarkGray
} catch {
    Write-Host "Starting TruthNet AI backend..." -ForegroundColor Cyan
    Start-Process -FilePath $venvPython -ArgumentList @(
        "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"
    ) -WorkingDirectory $backendPath | Out-Null
}

for ($attempt = 0; -not $backendReady -and $attempt -lt 60; $attempt++) {
    try {
        Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 2 | Out-Null
        $backendReady = $true
        break
    } catch {
        Start-Sleep -Seconds 1
    }
}
if (-not $backendReady) { throw "Backend did not become ready. Check its terminal for the startup error." }

$frontendReady = $false
try {
    Invoke-WebRequest -Uri "http://127.0.0.1:5173" -UseBasicParsing -TimeoutSec 2 | Out-Null
    $frontendReady = $true
    Write-Host "Frontend is already running." -ForegroundColor DarkGray
} catch {
    Write-Host "Starting TruthNet AI frontend..." -ForegroundColor Cyan
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "Set-Location '$frontendPath'; npm run dev -- --host 127.0.0.1 --port 5173 --strictPort" | Out-Null
}

for ($attempt = 0; -not $frontendReady -and $attempt -lt 60; $attempt++) {
    try {
        Invoke-WebRequest -Uri "http://127.0.0.1:5173" -UseBasicParsing -TimeoutSec 2 | Out-Null
        $frontendReady = $true
        break
    } catch {
        Start-Sleep -Seconds 1
    }
}
if (-not $frontendReady) { throw "Frontend did not become ready. Check its terminal for the startup error." }

Write-Host "TruthNet AI is running and both services are responding." -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host "Backend: http://localhost:8000/health" -ForegroundColor Yellow
Write-Host "Press Ctrl+C in each terminal to stop the services." -ForegroundColor DarkGray
Start-Process "http://localhost:5173"
