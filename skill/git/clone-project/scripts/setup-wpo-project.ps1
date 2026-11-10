<#
.SYNOPSIS
    Scaffold a new timestamped WPO working copy: create folder, clone dev branch, npm install.

.DESCRIPTION
    1. Ensures the base directory exists.
    2. Creates a new folder named wpo-new-<yyyyMMdd-HHmmss> inside it.
    3. Clones the wpo-app repo on the given branch into that folder.
    4. Runs `npm i` with the given flag inside the cloned repo.

    Any failed step stops the script (does not continue blindly to the next step).

.PARAMETER BaseDir
    Parent directory under which the new timestamped folder is created.
    Default: C:\Users\h22231\code\EEE-WPO

.PARAMETER RepoUrl
    Git remote to clone. Default assumes the SSH form (note the required
    colon after the host, which the originally supplied URL was missing):
    git@sjiojisoai:DFSDEV/apps/01-well-performance-optimization/source/wpo-app.git

.PARAMETER Branch
    Branch to check out on clone. Default: dev

.PARAMETER NpmFlag
    Flag(s) passed to `npm i`. Default: --force

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\setup-wpo-project.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\setup-wpo-project.ps1 `
        -BaseDir "C:\Users\h22231\code\EEE-WPO" `
        -RepoUrl "git@sjiojisoai:DFSDEV/apps/01-well-performance-optimization/source/wpo-app.git" `
        -Branch "dev" `
        -NpmFlag "--force"
#>

[CmdletBinding()]
param(
    [string]$BaseDir = "C:\Users\h22231\code\EEE-WPO",
    [string]$RepoUrl = "git@sjiojisoai:DFSDEV/apps/01-well-performance-optimization/source/wpo-app.git",
    [string]$Branch  = "dev",
    [string]$NpmFlag = "--force"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Fail {
    param([string]$Message)
    Write-Host ""
    Write-Host "FAIL: $Message" -ForegroundColor Red
    Write-Host "Setup complete: No"
    exit 1
}

# 1. Ensure base directory exists
Write-Step "Checking base directory: $BaseDir"
if (-not (Test-Path -LiteralPath $BaseDir)) {
    Write-Host "Base directory does not exist, creating it..."
    try {
        New-Item -ItemType Directory -Path $BaseDir -Force | Out-Null
    } catch {
        Fail "Could not create base directory '$BaseDir': $($_.Exception.Message)"
    }
}

# 2. Build timestamped folder name and create it
$timestamp  = Get-Date -Format "yyyyMMdd-HHmmss"
$folderName = "wpo-new-$timestamp"
$targetPath = Join-Path -Path $BaseDir -ChildPath $folderName

Write-Step "Creating project folder: $targetPath"
try {
    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
} catch {
    Fail "Could not create folder '$targetPath': $($_.Exception.Message)"
}

Set-Location -LiteralPath $targetPath

# 3. Clone the repo on the requested branch
Write-Step "Cloning $RepoUrl (branch: $Branch) into $targetPath"
git clone $RepoUrl -b $Branch .
if ($LASTEXITCODE -ne 0) {
    Fail "git clone failed (exit code $LASTEXITCODE). Check the repo URL/branch and your SSH access."
}

$headCommit = git rev-parse --short HEAD 2>$null
$headSubject = git log -1 --pretty=%s 2>$null
Write-Host "Clone succeeded. HEAD: $headCommit  $headSubject"

# 4. npm install
Write-Step "Running: npm i $NpmFlag"
npm i $NpmFlag
if ($LASTEXITCODE -ne 0) {
    Fail "npm install failed (exit code $LASTEXITCODE). See output above for details."
}

Write-Host ""
Write-Host "==> Summary" -ForegroundColor Green
Write-Host "New folder : $targetPath"
Write-Host "Repo       : $RepoUrl"
Write-Host "Branch     : $Branch (HEAD $headCommit`: $headSubject)"
Write-Host "npm install: OK ($NpmFlag)"
Write-Host ""
Write-Host "Setup complete: Yes"