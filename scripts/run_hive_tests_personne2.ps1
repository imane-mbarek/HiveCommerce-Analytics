<#
PowerShell wrapper for Binôme 1 - Personne 2 Hive tests.
Usage: Open PowerShell as Administrator (if needed) and run:
  powershell -ExecutionPolicy Bypass -File .\scripts\run_hive_tests_personne2.ps1

This script attempts to start Docker Desktop if the daemon is not responding,
waits for the Docker daemon, then runs the Beeline test commands inside the
`hive-server2` container.
#>

Set-StrictMode -Version Latest

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Wait-Docker {
    param([int]$TimeoutSeconds = 180)
    $sw = [Diagnostics.Stopwatch]::StartNew()
    while ($sw.Elapsed.TotalSeconds -lt $TimeoutSeconds) {
        try {
            docker version > $null 2>&1
            return $true
        } catch {
            Start-Sleep -Seconds 2
        }
    }
    return $false
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker CLI not found. Install Docker Desktop and ensure 'docker' is on PATH."
    exit 1
}

try {
    docker version > $null 2>&1
} catch {
    Write-Output "Docker daemon not available. Attempting to start Docker Desktop (may prompt for elevation)..."
    $exe = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
    if (-not (Test-Path $exe)) {
        Write-Error "Docker Desktop executable not found at $exe. Start Docker manually."
        exit 1
    }
    Start-Process -FilePath $exe -Verb RunAs
    if (-not (Wait-Docker -TimeoutSeconds 180)) {
        Write-Error "Docker did not start within timeout. Start Docker Desktop manually and rerun this script."
        exit 1
    }
}

# Check hive-server2 container
$container = docker ps --filter name=hive-server2 --format '{{.Names}}'
if (-not $container) {
    Write-Error "Container 'hive-server2' is not running. Start the stack with: docker compose up -d"
    exit 1
}

Write-Output "--- 1. Beeline connectivity ---"
docker exec -i hive-server2 beeline -u jdbc:hive2://localhost:10000 -e "SHOW DATABASES;"

Write-Output "--- 2. Managed vs External ---"
docker exec -i hive-server2 beeline -u jdbc:hive2://localhost:10000 -f /queries/table_types_comparison.hql

Write-Output "--- 3. File formats (CSV, ORC, Parquet) ---"
docker exec -i hive-server2 beeline -u jdbc:hive2://localhost:10000 -f /queries/file_formats_comparison.hql

Write-Output "--- Done ---"