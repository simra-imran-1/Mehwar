[CmdletBinding()]
param(
    [string]$Python = 'python',
    [string]$ExpectedSha,
    [switch]$InstallDependencies
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-DemoPython {
    param([string]$Label, [string[]]$Arguments)
    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed (exit $LASTEXITCODE). See the Python error above."
    }
}

try {
    $repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
    if ((Get-Location).Provider.Name -ne 'FileSystem' -or
        [IO.Path]::GetFullPath((Get-Location).Path) -ne $repoRoot) {
        throw "Run from this checkout's root: $repoRoot"
    }
    $gitRoot = & git rev-parse --show-toplevel
    if ($LASTEXITCODE -ne 0 -or [IO.Path]::GetFullPath($gitRoot) -ne $repoRoot) {
        throw 'Cannot identify this MEHWAR Git worktree.'
    }
    $origin = & git remote get-url origin
    if ($LASTEXITCODE -ne 0 -or $origin -notmatch '^(https://github\.com/|git@github\.com:|ssh://git@github\.com/)simra-imran-1/Mehwar(\.git)?/?$') {
        throw 'Expected origin: simra-imran-1/Mehwar on GitHub.'
    }
    $gitSha = & git rev-parse HEAD
    if ($LASTEXITCODE -ne 0) { throw 'Cannot determine HEAD.' }
    $baseSha = '3f19a2710b78144857a0dbeb60a65a0910a53ee1'
    & git merge-base --is-ancestor $baseSha HEAD
    if ($LASTEXITCODE -ne 0) { throw "HEAD must include the selected-demo base $baseSha." }
    if ($ExpectedSha -and $gitSha -ne $ExpectedSha) {
        throw "HEAD mismatch: expected $ExpectedSha, found $gitSha."
    }
    $state = & git status --porcelain --untracked-files=normal
    if ($LASTEXITCODE -ne 0) { throw 'Cannot determine worktree state.' }
    Write-Host "Repository: $origin"
    Write-Host "MEHWAR Git SHA: $gitSha (base $baseSha)"
    if ($state) {
        Write-Warning 'Worktree has uncommitted changes; export manifest will omit the Git SHA. Use a clean reviewed commit for the jury.'
    } else {
        Write-Host 'Worktree: clean'
    }

    if ([string]::IsNullOrWhiteSpace($env:MEHWAR_SEED33_CHECKPOINT)) {
        throw 'Set $env:MEHWAR_SEED33_CHECKPOINT to the separately supplied seed-33 ZIP, then rerun.'
    }
    if (-not (Test-Path -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT -PathType Leaf)) {
        throw 'MEHWAR_SEED33_CHECKPOINT does not name an existing file.'
    }
    $env:MEHWAR_SEED33_CHECKPOINT = (Resolve-Path -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT).Path
    $expectedHash = 'c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf'
    $before = Get-Item -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT
    $beforeSize = $before.Length
    $beforeWrite = $before.LastWriteTimeUtc
    if ((Get-FileHash -LiteralPath $before.FullName -Algorithm SHA256).Hash -ne $expectedHash) {
        throw 'Checkpoint SHA256 mismatch; stopping before imports or execution.'
    }
    Write-Host 'Checkpoint SHA256: verified'

    # Each attempt gets a fresh disposable folder; preserve previous upload evidence.
    $outputRoot = Join-Path $repoRoot 'outputs'
    $operatorRoot = Join-Path $outputRoot 'demo_operator'
    foreach ($directory in @($outputRoot, $operatorRoot)) {
        if (Test-Path -LiteralPath $directory) {
            $item = Get-Item -LiteralPath $directory -Force
            if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                throw "Output directory must be a normal directory, not a file or link: $directory"
            }
        } else {
            New-Item -ItemType Directory -Path $directory | Out-Null
        }
    }
    $outputDir = Join-Path $operatorRoot ([guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $outputDir | Out-Null
    $probe = Join-Path $outputDir '.write-probe'
    [IO.File]::WriteAllText($probe, 'MEHWAR disposable output check')
    Remove-Item -LiteralPath $probe
    Write-Host "Writable disposable output: $outputDir"

    Get-Command $Python -ErrorAction Stop | Out-Null
    if ($InstallDependencies) {
        Invoke-DemoPython -Label 'Dependency installation' -Arguments @('-m', 'pip', 'install', '-e', '.[dev,ppo,dashboard]')
    }
    # Reject an editable install pointing at a different worktree before running it.
    $importCheck = @'
import importlib
import pathlib
import sys
root = pathlib.Path(sys.argv[1]).resolve()
for name in ('mehwar', 'mehwar.selected_demo', 'mehwar.dashboard.app'):
    module = importlib.import_module(name)
    if not pathlib.Path(module.__file__).resolve().is_relative_to(root / 'src'):
        raise RuntimeError(f'{name} imports from another checkout: {module.__file__}')
for name in ('numpy', 'torch', 'streamlit'):
    importlib.import_module(name)
print(f'Required imports: OK ({sys.executable})')
'@
    Invoke-DemoPython -Label 'Required imports / checkout identity' -Arguments @('-c', $importCheck, $repoRoot)
    try {
        # Existing tooling owns ALL outcome, reference and full-trace assertions.
        Invoke-DemoPython -Label 'Selected-demo reproduction' -Arguments @('scripts/run_selected_demo.py', '--all', '--output-dir', $outputDir)
    } finally {
        $after = Get-Item -LiteralPath $env:MEHWAR_SEED33_CHECKPOINT
        if ((Get-FileHash -LiteralPath $after.FullName -Algorithm SHA256).Hash -ne $expectedHash -or
            $after.Length -ne $beforeSize -or $after.LastWriteTimeUtc -ne $beforeWrite) {
            throw 'Checkpoint changed during preflight (SHA256, size or modification time).'
        }
    }
    Write-Host "Upload backup: $outputDir\C4-0000.json and C4-0001.json"
    Write-Host 'PASS: both exact selected C4 results verified; checkpoint unchanged.'
} catch {
    throw "DEMO PREFLIGHT FAILED: $($_.Exception.Message) See docs/DEMO_RUNBOOK.md."
}
