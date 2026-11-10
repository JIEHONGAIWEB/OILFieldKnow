param(
    [string]$RepoPath = ".",
    [string]$Remote = "origin",
    [string]$Prefix = "sync",
    [switch]$Push,
    [switch]$CreateCommit
)

$ErrorActionPreference = "Stop"
$Script:GitRepoPath = $null

# Keep native command stderr as output text; success/failure is based on git exit code.
$PSNativeCommandUseErrorActionPreference = $false

function Run-Git {
    param([string[]]$GitArgs)

    if (-not $Script:GitRepoPath) {
        throw "Git repository path is not initialized."
    }

    $previousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & git -C $Script:GitRepoPath @GitArgs 2>&1 | ForEach-Object { $_.ToString() }
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorAction
    }

    return [pscustomobject]@{
        ExitCode = $exitCode
        Output = $output
    }
}

function Assert-GitSuccess {
    param(
        [string[]]$GitArgs,
        [string]$ErrorMessage
    )

    $result = Run-Git -GitArgs $GitArgs
    if ($result.ExitCode -ne 0) {
        throw "$ErrorMessage`n$($result.Output -join "`n")"
    }

    return $result.Output
}

$resolvedRepoPath = (Resolve-Path -Path $RepoPath).Path
$Script:GitRepoPath = $resolvedRepoPath

Assert-GitSuccess -GitArgs @("rev-parse", "--is-inside-work-tree") -ErrorMessage "Current path is not a Git repository."

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$startBranch = (Assert-GitSuccess -GitArgs @("branch", "--show-current") -ErrorMessage "Unable to detect current branch.") | Select-Object -First 1

$remoteBranchRefs = Assert-GitSuccess -GitArgs @("for-each-ref", "--format=%(refname:short)", "refs/remotes/$Remote") -ErrorMessage "Unable to list remote branches from '$Remote'."
$remoteBranches = $remoteBranchRefs | Where-Object {
    $_ -and
    ($_ -notmatch "/HEAD$") -and
    ($_ -notlike "$Remote/$Prefix/*")
}

if (-not $remoteBranches -or $remoteBranches.Count -eq 0) {
    throw "No eligible remote branches found under refs/remotes/$Remote."
}

$results = @()

foreach ($remoteBranch in $remoteBranches) {
    $baseBranch = $remoteBranch.Substring($Remote.Length + 1)
    $safeBaseBranch = ($baseBranch -replace "[^A-Za-z0-9._/-]", "-") -replace "/", "-"
    $newBranch = "$Prefix/$safeBaseBranch/update-$timestamp"

    $existsCheck = Run-Git -GitArgs @("show-ref", "--verify", "--quiet", "refs/heads/$newBranch")
    if ($existsCheck.ExitCode -eq 0) {
        $results += [pscustomobject]@{
            BaseBranch = $baseBranch
            NewBranch = $newBranch
            Status = "skipped (already exists)"
        }
        continue
    }

    $createResult = Run-Git -GitArgs @("branch", $newBranch, $remoteBranch)
    if ($createResult.ExitCode -ne 0) {
        $results += [pscustomobject]@{
            BaseBranch = $baseBranch
            NewBranch = $newBranch
            Status = "failed to create"
        }
        continue
    }

    if ($CreateCommit.IsPresent) {
        Assert-GitSuccess -GitArgs @("switch", $newBranch) -ErrorMessage "Failed to switch to '$newBranch'."

        $markerDir = ".branch-sync"
        $markerFile = Join-Path $markerDir "update-$safeBaseBranch.md"

        if (-not (Test-Path $markerDir)) {
            New-Item -Path $markerDir -ItemType Directory | Out-Null
        }

        @(
            "# Branch Update Marker"
            ""
            "- base-branch: $baseBranch"
            "- update-time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')"
            "- generated-by: git-branch-sync-assistant.ps1"
        ) | Set-Content -Path $markerFile -Encoding UTF8

        $addResult = Run-Git -GitArgs @("add", "-A")
        if ($addResult.ExitCode -ne 0) {
            $results += [pscustomobject]@{
                BaseBranch = $baseBranch
                NewBranch = $newBranch
                Status = "failed to add changes"
            }
            Assert-GitSuccess -GitArgs @("switch", $startBranch) -ErrorMessage "Failed to restore start branch '$startBranch'."
            continue
        }

        $commitMessage = "chore: update current time for $baseBranch ($timestamp)"
        $commitResult = Run-Git -GitArgs @("commit", "-m", $commitMessage)
        if ($commitResult.ExitCode -ne 0) {
            $results += [pscustomobject]@{
                BaseBranch = $baseBranch
                NewBranch = $newBranch
                Status = "failed to commit"
            }
            Assert-GitSuccess -GitArgs @("switch", $startBranch) -ErrorMessage "Failed to restore start branch '$startBranch'."
            continue
        }

        Assert-GitSuccess -GitArgs @("switch", $startBranch) -ErrorMessage "Failed to restore start branch '$startBranch'."
    }

    if ($Push.IsPresent) {
        $pushResult = Run-Git -GitArgs @("push", "-u", $Remote, $newBranch)
        if ($pushResult.ExitCode -ne 0) {
            $results += [pscustomobject]@{
                BaseBranch = $baseBranch
                NewBranch = $newBranch
                Status = "created locally, push failed"
            }
            continue
        }

        $results += [pscustomobject]@{
            BaseBranch = $baseBranch
            NewBranch = $newBranch
            Status = "created and pushed"
        }
    }
    else {
        $results += [pscustomobject]@{
            BaseBranch = $baseBranch
            NewBranch = $newBranch
            Status = "created locally"
        }
    }
}

$results | Sort-Object BaseBranch | Format-Table -AutoSize
