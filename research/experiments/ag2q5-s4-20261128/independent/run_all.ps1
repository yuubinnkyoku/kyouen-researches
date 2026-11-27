# Reproduce every check in this directory from scratch.
#   pwsh -File run_all.ps1
# Requires: python 3, gcc on PATH.
$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$root = (Resolve-Path (Join-Path $here '..\..\..\..')).Path
$board = Join-Path $root 'research\experiments\s-parameter-kyouen-20261125\output\board_ag2q5.txt'
$published = Join-Path $root 'research\experiments\pg2q7-cap-game-20261125\scripts\grundy_s_stats.c'
Set-Location $here

Write-Host '== board structure =='
python verify_board.py
if ($LASTEXITCODE -ne 0) { throw 'verify_board failed' }

Write-Host '== build =='
gcc -O2 -Wall -Wextra -o ag2q5_s4_independent.exe ag2q5_s4_independent.c
if ($LASTEXITCODE -ne 0) { throw 'independent build failed' }
gcc -O2 -Wall -Wextra -o grundy_s_stats_published.exe $published
if ($LASTEXITCODE -ne 0) { throw 'published build failed' }
gcc -O2 -Wall -Wextra -o count_complements.exe count_complements.c
if ($LASTEXITCODE -ne 0) { throw 'complement build failed' }

function Invoke-Engine([string]$exe, [string[]]$arguments, [string]$out, [string]$err) {
    $p = Start-Process -FilePath $exe -ArgumentList $arguments -WorkingDirectory $here `
        -RedirectStandardOutput $out -RedirectStandardError $err -Wait -PassThru
    if ($p.ExitCode -ne 0) { throw "$exe failed with exit code $($p.ExitCode)" }
}

Write-Host '== run independent solver =='
Invoke-Engine (Join-Path $here 'ag2q5_s4_independent.exe') @($board, '4') `
    (Join-Path $here 'my_run.txt') (Join-Path $here 'my_run.err')

Write-Host '== run published solver =='
Invoke-Engine (Join-Path $here 'grundy_s_stats_published.exe') @($board, '4') `
    (Join-Path $here 'published_run.txt') (Join-Path $here 'published_stderr.txt')

Write-Host '== run complement counter =='
Invoke-Engine (Join-Path $here 'count_complements.exe') @($board, '4') `
    (Join-Path $here 'complements_run.txt') (Join-Path $here 'complements_run.err')

Write-Host '== cross-check claim, arithmetic, structure =='
python compare.py
if ($LASTEXITCODE -ne 0) { throw 'compare failed' }

Write-Host '== validate both engines on tiny boards =='
python validate_small.py
if ($LASTEXITCODE -ne 0) { throw 'small-board validation failed' }

Write-Host '== permutation invariance =='
python permute_test.py
if ($LASTEXITCODE -ne 0) { throw 'permutation test failed' }

Write-Host ''
Write-Host 'ALL CHECKS PASSED'
