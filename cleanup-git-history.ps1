# Git History Cleanup Script
# Removes sensitive files from all Git commits

Write-Host "🚨 GIT HISTORY CLEANUP - REMOVING SENSITIVE FILES" -ForegroundColor Red
Write-Host "=================================================" -ForegroundColor Red
Write-Host ""

# Step 1: Check if git-filter-repo is installed
Write-Host "📋 Step 1: Checking for git-filter-repo..." -ForegroundColor Cyan
$filterRepoInstalled = $false
try {
    $result = git filter-repo --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $filterRepoInstalled = $true
        Write-Host "✅ git-filter-repo is installed" -ForegroundColor Green
    }
} catch {
    $filterRepoInstalled = $false
}

if (-not $filterRepoInstalled) {
    Write-Host "⚠️ git-filter-repo not found. Installing..." -ForegroundColor Yellow
    Write-Host "Run: pip install git-filter-repo" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative: Manual cleanup with BFG or filter-branch" -ForegroundColor Yellow
    Write-Host "See SECURITY_CLEANUP_INSTRUCTIONS.md for details" -ForegroundColor Yellow
    Write-Host ""
    
    # Ask if user wants to proceed with alternative method
    $response = Read-Host "Use alternative method (filter-branch)? (y/n)"
    if ($response -ne "y") {
        Write-Host "❌ Cleanup cancelled" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Backup repository
Write-Host ""
Write-Host "💾 Step 2: Creating backup..." -ForegroundColor Cyan
$backupName = "HRAIAgent-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$backupPath = "..\$backupName"

if (Test-Path $backupPath) {
    Write-Host "⚠️ Backup already exists at $backupPath" -ForegroundColor Yellow
} else {
    git clone . $backupPath
    Write-Host "✅ Backup created at $backupPath" -ForegroundColor Green
}

# Step 3: Create paths file for removal
Write-Host ""
Write-Host "📝 Step 3: Creating list of files to remove..." -ForegroundColor Cyan
$pathsFile = "paths-to-remove.txt"
@"
.env
HR_root_agent/.env
.env.*
**/.env
**/.env.*
credentials.json
google_credentials.json
service_account.json
token.json
*.key
*.pem
*.p12
"@ | Out-File -FilePath $pathsFile -Encoding UTF8

Write-Host "✅ Created $pathsFile" -ForegroundColor Green

# Step 4: Remove files from history
Write-Host ""
Write-Host "🧹 Step 4: Removing sensitive files from Git history..." -ForegroundColor Yellow
Write-Host "⚠️ This will rewrite Git history!" -ForegroundColor Red
Write-Host ""

$confirm = Read-Host "Continue with cleanup? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "❌ Cleanup cancelled" -ForegroundColor Red
    exit 1
}

# Method 1: Try git-filter-repo first
if ($filterRepoInstalled) {
    Write-Host "Using git-filter-repo method..." -ForegroundColor Cyan
    git filter-repo --invert-paths --paths-from-file $pathsFile --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Successfully removed files using git-filter-repo" -ForegroundColor Green
    } else {
        Write-Host "❌ git-filter-repo failed. Trying alternative method..." -ForegroundColor Yellow
        $filterRepoInstalled = $false
    }
}

# Method 2: Fallback to filter-branch
if (-not $filterRepoInstalled) {
    Write-Host "Using git filter-branch method..." -ForegroundColor Cyan
    
    $env:FILTER_BRANCH_SQUELCH_WARNING=1
    
    git filter-branch --force --index-filter @"
git rm --cached --ignore-unmatch .env
git rm --cached --ignore-unmatch HR_root_agent/.env
git rm --cached --ignore-unmatch .env.*
git rm --cached --ignore-unmatch credentials.json
git rm --cached --ignore-unmatch google_credentials.json
git rm --cached --ignore-unmatch service_account.json
git rm --cached --ignore-unmatch token.json
git rm --cached --ignore-unmatch *.key
git rm --cached --ignore-unmatch *.pem
git rm --cached --ignore-unmatch *.p12
"@ --prune-empty --tag-name-filter cat -- --all

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Successfully removed files using filter-branch" -ForegroundColor Green
    } else {
        Write-Host "❌ Filter-branch failed" -ForegroundColor Red
        exit 1
    }
}

# Step 5: Clean up
Write-Host ""
Write-Host "🗑️ Step 5: Cleaning up repository..." -ForegroundColor Cyan
git reflog expire --expire=now --all
git gc --prune=now --aggressive
Write-Host "✅ Repository cleaned and optimized" -ForegroundColor Green

# Step 6: Verify cleanup
Write-Host ""
Write-Host "🔍 Step 6: Verifying cleanup..." -ForegroundColor Cyan

$apiKeyFound = git log --all -p -S "AIzaSy" 2>&1 | Select-String "AIzaSy"
if ($apiKeyFound) {
    Write-Host "⚠️ API keys still found in history!" -ForegroundColor Red
    Write-Host "You may need to run additional cleanup" -ForegroundColor Yellow
} else {
    Write-Host "✅ No API keys found in history" -ForegroundColor Green
}

$envFileFound = git log --all --full-history -- .env 2>&1
if ($envFileFound -match "commit") {
    Write-Host "⚠️ .env file references still found" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env files removed from history" -ForegroundColor Green
}

# Step 7: Repository size comparison
Write-Host ""
Write-Host "📊 Repository size:" -ForegroundColor Cyan
git count-objects -vH

# Step 8: Next steps
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️ IMPORTANT NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. REVOKE OLD API KEYS:" -ForegroundColor Red
Write-Host "   - Go to: https://console.cloud.google.com/apis/credentials" -ForegroundColor White
Write-Host "   - Delete exposed keys" -ForegroundColor White
Write-Host "   - Generate new keys" -ForegroundColor White
Write-Host ""
Write-Host "2. FORCE PUSH TO GITHUB:" -ForegroundColor Yellow
Write-Host "   git push origin --force --all" -ForegroundColor White
Write-Host "   git push origin --force --tags" -ForegroundColor White
Write-Host ""
Write-Host "3. UPDATE CLOUD RUN:" -ForegroundColor Cyan
Write-Host "   gcloud run services update hraiagent \" -ForegroundColor White
Write-Host "     --region us-central1 \" -ForegroundColor White
Write-Host "     --update-env-vars GOOGLE_API_KEY=<NEW_KEY>" -ForegroundColor White
Write-Host ""
Write-Host "4. NOTIFY TEAM MEMBERS to re-clone repository" -ForegroundColor Magenta
Write-Host ""
Write-Host "5. VERIFY on GitHub:" -ForegroundColor Green
Write-Host "   - Search for 'AIzaSy' - should return no results" -ForegroundColor White
Write-Host "   - Check old commits - .env files should be gone" -ForegroundColor White
Write-Host ""
Write-Host "Backup location: $backupPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "SECURITY_CLEANUP_INSTRUCTIONS.md" -ForegroundColor White
Write-Host ""

# Clean up temporary files
Remove-Item $pathsFile -Force -ErrorAction SilentlyContinue
