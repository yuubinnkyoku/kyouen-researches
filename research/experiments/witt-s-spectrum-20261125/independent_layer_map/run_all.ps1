# Reproduce the independent layer map of the W_24 s=7 Grundy spectrum.
#
# Requires: gcc (MSYS2 ucrt64 was used: gcc 15.2.0) and Python 3.12 (stdlib only).
# Everything is written inside this directory.
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $here
try {
    $gcc = Get-Command gcc -ErrorAction SilentlyContinue
    if ($gcc) { $gcc = $gcc.Source } else { $gcc = "C:\msys64\ucrt64\bin\gcc.exe" }
    Write-Host "gcc: $gcc"
    & $gcc -O2 -o layer_map.exe layer_map.c
    if ($LASTEXITCODE -ne 0) { throw "gcc failed" }

    $board = (Resolve-Path "..\..\design-kyouen-witt-20261125\output\board_w24.txt").Path
    Write-Host "=== task 1: board identification and Golay/dodecad recomputation ==="
    python task1_board.py

    Write-Host "=== task 2/3/4/5: exhaustive layer map (C) ==="
    & .\layer_map.exe $board (Join-Path $here "out\layer_map.txt")
    if ($LASTEXITCODE -ne 0) { throw "layer_map failed" }

    Write-Host "=== Python independent spot-check of sampled caps ==="
    python spotcheck.py
    if ($LASTEXITCODE -ne 0) { throw "spotcheck failed" }

    python make_tables.py

    Write-Host "=== claim comparison ==="
    python compare_claim.py
    if ($LASTEXITCODE -ne 0) { throw "claim comparison FAILED" }

    Write-Host "=== appendix table consistency ==="
    python check_appendix.py
    if ($LASTEXITCODE -ne 0) { throw "appendix table out of sync with REPORT.md" }
    Write-Host "ALL OK"
}
finally {
    Pop-Location
}
