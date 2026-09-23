$ErrorActionPreference = "Stop"

$RepoZip = "https://github.com/aruru737/aruru-openhouse-skill/archive/refs/heads/main.zip"
$SkillName = "openhouse-marketing-master"
$InstallRoot = Join-Path $HOME ".agents\skills"
$InstallDir = Join-Path $InstallRoot $SkillName
$TempRoot = Join-Path $env:TEMP ("aruru-openhouse-" + [guid]::NewGuid().ToString("N"))
$ZipPath = Join-Path $TempRoot "repo.zip"
$ExtractPath = Join-Path $TempRoot "extract"

try {
    New-Item -ItemType Directory -Path $TempRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $InstallRoot -Force | Out-Null

    Invoke-WebRequest -Uri $RepoZip -OutFile $ZipPath -UseBasicParsing
    Expand-Archive -Path $ZipPath -DestinationPath $ExtractPath -Force

    $RepoDir = Get-ChildItem $ExtractPath -Directory | Select-Object -First 1
    $Source = Join-Path $RepoDir.FullName ("skills\" + $SkillName)
    $SkillInstaller = Join-Path $Source "install.ps1"
    if (-not (Test-Path $SkillInstaller)) { throw "完全版スキルの install.ps1 が見つかりません。" }

    & $SkillInstaller -TargetRoot $InstallRoot
}
catch {
    Write-Host ("エラー: " + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
finally {
    if (Test-Path $TempRoot) { Remove-Item $TempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
