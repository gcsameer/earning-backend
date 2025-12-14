# Auto-run Railway commands script
# This will attempt to run commands and guide through authentication if needed

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Railway Commands Auto-Runner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if logged in
Write-Host "Checking Railway authentication..." -ForegroundColor Yellow
$authCheck = railway whoami 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "Authentication required!" -ForegroundColor Red
    Write-Host "Please run: railway login" -ForegroundColor Yellow
    Write-Host "This will open a browser for authentication." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "After logging in, run this script again." -ForegroundColor Cyan
    exit 1
}

Write-Host "Authenticated! Proceeding with commands..." -ForegroundColor Green
Write-Host ""

# Step 1: Remove video tasks
Write-Host "Step 1: Removing video tasks..." -ForegroundColor Yellow
railway run python manage.py remove_video_tasks
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error in step 1" -ForegroundColor Red
    exit 1
}
Write-Host "Step 1 completed!" -ForegroundColor Green
Write-Host ""

# Step 2: Create game tasks
Write-Host "Step 2: Creating game tasks..." -ForegroundColor Yellow
railway run python manage.py force_create_tasks
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error in step 2" -ForegroundColor Red
    exit 1
}
Write-Host "Step 2 completed!" -ForegroundColor Green
Write-Host ""

# Step 3: Verify tasks
Write-Host "Step 3: Verifying tasks..." -ForegroundColor Yellow
railway run python manage.py verify_tasks
Write-Host "Step 3 completed!" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All commands completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

