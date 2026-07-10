# Sync know-skills core skills into the local Agent skills directory.
#
# Default target: $env:USERPROFILE\.agents\skills  (override with $env:SKILLS_ROOT)
# Usage:
#   .\scripts\sync-skills.ps1
#   .\scripts\sync-skills.ps1 -DryRun
#   .\scripts\sync-skills.ps1 -Symlink   # requires Developer Mode or admin on Windows

[CmdletBinding()]
param(
    [switch]$DryRun,
    [switch]$Symlink
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SkillsSrc = Join-Path $RepoRoot "skills"
$SkillsRoot = if ($env:SKILLS_ROOT) { $env:SKILLS_ROOT } else {
    Join-Path $env:USERPROFILE ".agents\skills"
}
$CoreSkills = @("css-professor", "agent-loop")

$professor = Join-Path $SkillsSrc "css-professor"
if (-not (Test-Path -LiteralPath $professor -PathType Container)) {
    throw "Expected skill dir missing: $professor"
}

Write-Host "Source: $SkillsSrc"
Write-Host "Target: $SkillsRoot"
if ($DryRun) { Write-Host "(dry-run)" }

if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null
} else {
    Write-Host "DRY: New-Item -ItemType Directory -Force $SkillsRoot"
}

foreach ($name in $CoreSkills) {
    $src = Join-Path $SkillsSrc $name
    $dst = Join-Path $SkillsRoot $name
    if (-not (Test-Path -LiteralPath $src -PathType Container)) {
        Write-Warning "SKIP missing source: $src"
        continue
    }

    if ($Symlink) {
        if ($DryRun) {
            Write-Host "DRY: New-Item -ItemType SymbolicLink -Path $dst -Target $src"
        } else {
            if (Test-Path -LiteralPath $dst) {
                Remove-Item -LiteralPath $dst -Recurse -Force
            }
            New-Item -ItemType SymbolicLink -Path $dst -Target $src | Out-Null
        }
        Write-Host "LINK  $name -> $src"
    } else {
        if ($DryRun) {
            Write-Host "DRY: Copy-Item -Recurse -Force $src $dst"
        } else {
            if (Test-Path -LiteralPath $dst) {
                Remove-Item -LiteralPath $dst -Recurse -Force
            }
            Copy-Item -Recurse -Force -Path $src -Destination $dst
        }
        Write-Host "COPY  $name -> $dst"
    }
}

Write-Host ""
Write-Host "Done. Reload Agent skills / start a new session if the host caches skill files."
