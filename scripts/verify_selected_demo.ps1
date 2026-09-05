[CmdletBinding()]
param(
    [string]$OutputDir = 'outputs/selected_demo',
    [switch]$InstallDependencies
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-Python {
    param([string[]]$Arguments)
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "python $($Arguments -join ' ') failed (exit $LASTEXITCODE)."
    }
}

$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$gitRoot = & git rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0 -or [IO.Path]::GetFullPath($gitRoot) -ne $repoRoot) {
    throw 'Run this helper from the MEHWAR repository, not another checkout.'
}
$projectFile = Join-Path $repoRoot 'pyproject.toml'
if (-not (Test-Path -LiteralPath (Join-Path $repoRoot 'src/mehwar/contracts.py')) -or
    (Get-Content -LiteralPath $projectFile -Raw) -notmatch '(?m)^name = "mehwar"\r?$') {
    throw 'This is not the expected MEHWAR repository.'
}
$gitSha = & git -C $repoRoot rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot determine the current Git SHA.' }
Write-Host "MEHWAR Git SHA: $gitSha"

if ([string]::IsNullOrWhiteSpace($env:MEHWAR_SEED33_CHECKPOINT)) {
    throw 'Set MEHWAR_SEED33_CHECKPOINT to the separately supplied seed-33 checkpoint.'
}
if (-not (Test-Path -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT -PathType Leaf)) {
    throw 'MEHWAR_SEED33_CHECKPOINT does not name an existing file.'
}
# Resolve before changing directory so relative checkpoint paths stay unambiguous.
$env:MEHWAR_SEED33_CHECKPOINT = (Resolve-Path -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT).Path
$expectedHash = 'c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf'
$checkpointHash = (Get-FileHash -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT -Algorithm SHA256).Hash
if ($checkpointHash -ne $expectedHash) { throw 'Checkpoint SHA256 mismatch; stopping before tests.' }
Write-Host 'Checkpoint SHA256 verified.'

Push-Location -LiteralPath $repoRoot
try {
    if ($InstallDependencies) {
        Invoke-Python -Arguments @('-m', 'pip', 'install', '-e', '.[dev,ppo,dashboard]')
    } else {
        Write-Host 'Prerequisite: activated venv with python -m pip install -e ".[dev,ppo,dashboard]"'
    }
    Invoke-Python -Arguments @('-m', 'pytest')
    Invoke-Python -Arguments @('-m', 'ruff', 'check', '.')
    & git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'git diff --check failed.' }
    Invoke-Python -Arguments @('scripts/run_selected_demo.py', '--all', '--output-dir', $OutputDir)
    $afterHash = (Get-FileHash -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT -Algorithm SHA256).Hash
    if ($afterHash -ne $expectedHash) { throw 'Checkpoint changed during verification.' }
    Write-Host "PASS: tests, Ruff, selected C4 evidence and checkpoint integrity. Outputs: $OutputDir"
} finally {
    Pop-Location
}
