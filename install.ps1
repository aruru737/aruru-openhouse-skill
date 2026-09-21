# アルル制作所｜完成見学会Skill インストーラー
# Windows PowerShell 5.1+
$ErrorActionPreference = "Stop"

$RepoZip = "https://github.com/aruru737/aruru-openhouse-skill/archive/refs/heads/main.zip"
$InstallRoot = Join-Path $HOME ".agents\skills"
$TempRoot = Join-Path $env:TEMP ("aruru-openhouse-" + [guid]::NewGuid().ToString("N"))
$ZipPath = Join-Path $TempRoot "repo.zip"
$ExtractPath = Join-Path $TempRoot "extract"

function Step($m) { Write-Host ""; Write-Host "=== $m ===" -ForegroundColor Cyan }

try {
  Step "アルル制作所 完成見学会Skill をインストールします"
  New-Item -ItemType Directory -Path $TempRoot -Force | Out-Null
  New-Item -ItemType Directory -Path $InstallRoot -Force | Out-Null

  Step "最新版をダウンロードしています"
  Invoke-WebRequest -Uri $RepoZip -OutFile $ZipPath -UseBasicParsing

  Step "展開しています"
  Expand-Archive -Path $ZipPath -DestinationPath $ExtractPath -Force
  $RepoDir = Get-ChildItem $ExtractPath -Directory | Select-Object -First 1
  $SkillsRoot = Join-Path $RepoDir.FullName "skills"
  if (-not (Test-Path $SkillsRoot)) { throw "skills フォルダが見つかりません。" }

  Step "Skill をインストールしています"
  $SkillDirs = Get-ChildItem $SkillsRoot -Directory
  foreach ($dir in $SkillDirs) {
    $dst = Join-Path $InstallRoot $dir.Name
    if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
    Copy-Item $dir.FullName $dst -Recurse -Force
    Write-Host ("  OK " + $dir.Name)
  }

  Step "インストール完了"
  Write-Host ("インストール先: " + $InstallRoot) -ForegroundColor Green
  Write-Host ("インストール数: " + $SkillDirs.Count + " Skill") -ForegroundColor Green
  Write-Host ""
  Write-Host "Codexを再起動し、住宅写真を添付して"
  Write-Host "「完成見学会の資料を作って」"
  Write-Host "と入力してください。" -ForegroundColor Yellow
}
catch {
  Write-Host ""
  Write-Host ("エラー: " + $_.Exception.Message) -ForegroundColor Red
  exit 1
}
finally {
  if (Test-Path $TempRoot) { Remove-Item $TempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
