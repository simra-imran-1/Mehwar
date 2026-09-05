[CmdletBinding()]
param(
    [string]$Python = 'python',
    [string]$ExpectedSha,
    [ValidateRange(1024, 65535)]
    [int]$Port = 8501,
    [switch]$InstallDependencies
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

try {
    & (Join-Path $PSScriptRoot 'demo_preflight.ps1') -Python $Python -ExpectedSha $ExpectedSha -InstallDependencies:$InstallDependencies
    # Fail before launch if another server already owns the requested local port.
    $listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $Port)
    try {
        $listener.Start()
    } catch {
        throw "Port $Port is unavailable. Stop your previous demo with Ctrl+C or rerun with -Port 8502."
    } finally {
        $listener.Stop()
    }
    Write-Host "Starting dashboard at http://127.0.0.1:$Port"
    Write-Host 'Wait for Streamlit to print its URL, then open it in your browser. Keep this terminal open; Ctrl+C stops the server.'
    Write-Host 'Input source -> Run selected verified C4 demo locally (the initial view is a labeled synthetic fixture).'
    Write-Host 'First: C4-0000 -> Run verified C4 demo -> success / 16 steps / 0 invalid actions.'
    Write-Host 'Second: C4-0001 -> Run verified C4 demo -> two_cell_loop / 28 steps / 0 invalid actions.'
    Write-Host 'Legal action selection does not by itself guarantee mission liveness.'
    & $Python -m streamlit run (Join-Path $PSScriptRoot '../app.py') --server.address 127.0.0.1 --server.port $Port --server.headless true --browser.gatherUsageStats false
    if ($LASTEXITCODE -ne 0) {
        throw "Streamlit exited with code $LASTEXITCODE. See docs/DEMO_RUNBOOK.md for recovery."
    }
} catch {
    throw "DEMO START FAILED: $($_.Exception.Message)"
}
