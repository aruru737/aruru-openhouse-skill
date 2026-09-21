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
    $Source = Join-Path $RepoDir.FullName ("skills\" + $SkillName + "\SKILL.md")
    if (-not (Test-Path $Source)) { throw "統合版 SKILL.md が見つかりません。" }

    if (Test-Path $InstallDir) { Remove-Item $InstallDir -Recurse -Force }
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    Copy-Item $Source (Join-Path $InstallDir "SKILL.md") -Force

    Write-Host ""
    Write-Host "インストール完了" -ForegroundColor Green
    Write-Host ("インストール先: " + $InstallDir)
    Write-Host ""
    Write-Host "Codexを再起動し、住宅写真を添付して"
    Write-Host "「完成見学会の資料を作って」"
    Write-Host "と入力してください。" -ForegroundColor Yellow
}
catch {
    Write-Host ("エラー: " + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
finally {
    if (Test-Path $TempRoot) { Remove-Item $TempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
