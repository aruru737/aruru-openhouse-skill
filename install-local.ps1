$ErrorActionPreference = "Stop"
$SkillName = "openhouse-marketing-master"
$SourceRoot = Join-Path $PSScriptRoot ("skills\" + $SkillName)
$InstallRoot = Join-Path $HOME ".agents\skills"

try {
    $Installer = Join-Path $SourceRoot "install.ps1"
    if (-not (Test-Path $Installer)) {
        throw "完全版スキルの install.ps1 が見つかりません。ZIPを展開してから実行してください。"
    }
    & $Installer -TargetRoot $InstallRoot
}
catch {
    Write-Host ("エラー: " + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
