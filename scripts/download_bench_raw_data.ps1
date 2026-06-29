$ErrorActionPreference = "Stop"

$Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$Raw = Join-Path $Root "data\raw"

function Ensure-Dir {
  param([string]$Path)
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

function Remove-InWorkspace {
  param([string]$Path)
  if (Test-Path -LiteralPath $Path) {
    $Resolved = (Resolve-Path -LiteralPath $Path).Path
    if (-not $Resolved.StartsWith($Root, [System.StringComparison]::OrdinalIgnoreCase)) {
      throw "Refusing to remove path outside workspace: $Resolved"
    }
    Remove-Item -LiteralPath $Resolved -Recurse -Force
  }
}

Ensure-Dir $Raw

function Download-IfMissing {
  param(
    [string]$DirName,
    [string]$FileName,
    [string]$Url
  )
  $Dir = Join-Path $Raw $DirName
  Ensure-Dir $Dir
  $Path = Join-Path $Dir $FileName
  if (-not (Test-Path -LiteralPath $Path)) {
    Invoke-WebRequest -Uri $Url -OutFile $Path -UseBasicParsing
  }
}

$IjocRoot = Join-Path $Raw "ijoc-data"
$IjocMonotone = Join-Path $IjocRoot "monotone-classification-problems"
$IjocResearch = Join-Path $IjocRoot "research-unit-evaluation"

if (-not ((Test-Path -LiteralPath $IjocMonotone) -and (Test-Path -LiteralPath $IjocResearch))) {
  $Tmp = Join-Path $Raw "_ijoc_download_tmp"
  $Zip = Join-Path $Raw "ijoc-data-download.zip"
  Remove-InWorkspace $Tmp
  if (Test-Path -LiteralPath $Zip) { Remove-Item -LiteralPath $Zip -Force }

  Invoke-WebRequest -Uri "https://github.com/ijoc-data/download/archive/refs/heads/master.zip" -OutFile $Zip
  Expand-Archive -LiteralPath $Zip -DestinationPath $Tmp -Force

  Ensure-Dir $IjocRoot
  Copy-Item -LiteralPath (Join-Path $Tmp "download-master\monotone-classification-problems") -Destination $IjocRoot -Recurse -Force
  Copy-Item -LiteralPath (Join-Path $Tmp "download-master\research-unit-evaluation") -Destination $IjocRoot -Recurse -Force

  Remove-InWorkspace $Tmp
  Remove-Item -LiteralPath $Zip -Force
}

$WineDir = Join-Path $Raw "uci_wine_quality"
Ensure-Dir $WineDir
$WineZip = Join-Path $WineDir "wine_quality.zip"
if (-not (Test-Path -LiteralPath $WineZip)) {
  Invoke-WebRequest -Uri "https://archive.ics.uci.edu/static/public/186/wine+quality.zip" -OutFile $WineZip
}

Download-IfMissing `
  -DirName "uci_student_performance" `
  -FileName "student_performance.zip" `
  -Url "https://archive.ics.uci.edu/static/public/320/student+performance.zip"

Download-IfMissing `
  -DirName "uci_maternal_health_risk" `
  -FileName "maternal_health_risk.zip" `
  -Url "https://archive.ics.uci.edu/static/public/863/maternal+health+risk.zip"

Download-IfMissing `
  -DirName "uci_higher_education_students_performance" `
  -FileName "higher_education_students_performance.zip" `
  -Url "https://archive.ics.uci.edu/static/public/856/higher+education+students+performance+evaluation.zip"

Download-IfMissing `
  -DirName "toc_uco" `
  -FileName "TOC-UCO.zip" `
  -Url "https://www.uco.es/grupos/ayrna/datasets/TOC-UCO.zip"

$LocalQs = Join-Path $Raw "local_qs"
Ensure-Dir $LocalQs
$Docs = Join-Path $Root "docs"
$QsFiles = Get-ChildItem -LiteralPath $Docs -Recurse -File |
  Where-Object {
    $_.Name -like "*2020.csv" -or
    $_.Name -like "*2022.csv" -or
    ($_.Name -like "*2026*.xlsx" -and $_.Name -like "*属性*")
  }

foreach ($File in $QsFiles) {
  Copy-Item -LiteralPath $File.FullName -Destination (Join-Path $LocalQs $File.Name) -Force
}

Write-Output "Raw benchmark data is ready under $Raw"
