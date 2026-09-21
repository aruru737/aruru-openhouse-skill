$ErrorActionPreference = "Stop"
$SourceRoot = Join-Path $PSScriptRoot "skills"
$InstallRoot = Join-Path $HOME ".agents\skills"

try {
    if (-not (Test-Path $SourceRoot)) {
        throw "skills フォルダが見つかりません。ZIPを展開してから実行してください。"
    }
    New-Item -ItemType Directory -Path $InstallRoot -Force | Out-Null
    $SkillDirs = Get-ChildItem $SourceRoot -Directory
    foreach ($dir in $SkillDirs) {
        $dst = Join-Path $InstallRoot $dir.Name
        if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
        Copy-Item $dir.FullName $dst -Recurse -Force
        Write-Host ("  OK " + $dir.Name)
    }
    Write-Host ""
    Write-Host "インストール完了" -ForegroundColor Green
    Write-Host ("インストール先: " + $InstallRoot)
    Write-Host ("インストール数: " + $SkillDirs.Count + " Skill")
    Write-Host "Codexを再起動し、住宅写真を添付して「完成見学会の資料を作って」と入力してください。"
}
catch {
    Write-Host ("エラー: " + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
