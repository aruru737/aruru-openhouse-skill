[CmdletBinding()]
param(
    [string]$TargetRoot = (Join-Path $HOME '.agents\skills'),
    [switch]$ReplaceCompanyProfile
)

$ErrorActionPreference = 'Stop'
$SkillName = 'openhouse-marketing-master'
$Source = [IO.Path]::GetFullPath($PSScriptRoot)
$TargetRoot = [IO.Path]::GetFullPath($TargetRoot)
$Destination = [IO.Path]::GetFullPath((Join-Path $TargetRoot $SkillName))

if ((Split-Path $Destination -Leaf) -ne $SkillName) {
    throw "Unexpected installation destination: $Destination"
}
if (-not (Test-Path -LiteralPath (Join-Path $Source 'SKILL.md'))) {
    throw "SKILL.md was not found in the distribution folder: $Source"
}
if ($Source.TrimEnd('\') -eq $Destination.TrimEnd('\')) {
    Write-Host "This folder is already the installation destination: $Destination" -ForegroundColor Yellow
    exit 0
}

New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
$Stage = Join-Path $TargetRoot ('.' + $SkillName + '.install-' + [guid]::NewGuid().ToString('N'))
$Backup = $null

try {
    New-Item -ItemType Directory -Path $Stage -Force | Out-Null
    Copy-Item -Path (Join-Path $Source '*') -Destination $Stage -Recurse -Force

    $stagedSkill = Join-Path $Stage 'SKILL.md'
    $stagedText = [IO.File]::ReadAllText($stagedSkill, [Text.Encoding]::UTF8)
    if ($stagedText -notmatch '(?s)^---\s*\nname:\s*openhouse-marketing-master\s*\ndescription:') {
        throw 'The staged SKILL.md has invalid frontmatter.'
    }

    $profileRelative = 'references\company-profile.yaml'
    $existingProfile = Join-Path $Destination $profileRelative
    $stagedProfile = Join-Path $Stage $profileRelative
    if (-not $ReplaceCompanyProfile -and (Test-Path -LiteralPath $existingProfile)) {
        New-Item -ItemType Directory -Path (Split-Path $stagedProfile -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $existingProfile -Destination $stagedProfile -Force
        Write-Host 'Existing company-profile.yaml will be preserved.' -ForegroundColor Cyan
    }

    if (Test-Path -LiteralPath $Destination) {
        $timestamp = Get-Date -Format 'yyyyMMdd-HHmmssfff'
        $Backup = "$Destination.backup-$timestamp"
        Move-Item -LiteralPath $Destination -Destination $Backup
    }

    Move-Item -LiteralPath $Stage -Destination $Destination
    $Stage = $null

    $fileCount = (Get-ChildItem -LiteralPath $Destination -Recurse -File).Count
    Write-Host ''
    Write-Host 'Installation completed.' -ForegroundColor Green
    Write-Host "  Destination: $Destination"
    Write-Host "  Files: $fileCount"
    if ($Backup) {
        Write-Host "  Previous version backup: $Backup"
    }
    Write-Host 'Restart Codex to ensure the updated skill is loaded.' -ForegroundColor Yellow
}
catch {
    if ($Stage -and (Test-Path -LiteralPath $Stage)) {
        Remove-Item -LiteralPath $Stage -Recurse -Force
    }
    if ($Backup -and -not (Test-Path -LiteralPath $Destination) -and (Test-Path -LiteralPath $Backup)) {
        Move-Item -LiteralPath $Backup -Destination $Destination
    }
    throw
}
