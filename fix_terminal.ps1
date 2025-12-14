# Fix PowerShell Execution Policy for Railway CLI
Write-Host "Fixing PowerShell execution policy..." -ForegroundColor Yellow

# Set execution policy for current user
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "Execution policy updated successfully!" -ForegroundColor Green
} catch {
    Write-Host "Note: Policy may be overridden by system policy" -ForegroundColor Yellow
    Write-Host "Current effective policy: $(Get-ExecutionPolicy)" -ForegroundColor Cyan
}

# Test Railway CLI
Write-Host "`nTesting Railway CLI..." -ForegroundColor Yellow
$railwayVersion = railway --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Railway CLI is working! Version: $railwayVersion" -ForegroundColor Green
} else {
    Write-Host "Railway CLI test failed. Error: $railwayVersion" -ForegroundColor Red
}

Write-Host "`nDone! You can now use Railway commands." -ForegroundColor Green

