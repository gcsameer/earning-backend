# PowerShell script to run all Railway commands for task updates
# Make sure you're logged in: railway login
# Make sure you're linked: railway link

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running Railway Commands for Task Updates" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Remove video tasks
Write-Host "Step 1: Removing video tasks..." -ForegroundColor Yellow
railway run python manage.py remove_video_tasks
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to remove video tasks" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Video tasks removed" -ForegroundColor Green
Write-Host ""

# Step 2: Force create all game tasks
Write-Host "Step 2: Creating game tasks with new coin ranges..." -ForegroundColor Yellow
railway run python manage.py force_create_tasks
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create tasks" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Game tasks created" -ForegroundColor Green
Write-Host ""

# Step 3: Verify tasks
Write-Host "Step 3: Verifying tasks..." -ForegroundColor Yellow
railway run python manage.py verify_tasks
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Verification showed issues" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ All commands completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

