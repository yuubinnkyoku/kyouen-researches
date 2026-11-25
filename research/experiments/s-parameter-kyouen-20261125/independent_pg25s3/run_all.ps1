# run_all.ps1 -- end-to-end independent verification (PG(2,5), s=3 blocking game)
# Run from this directory (pwsh).  Requires gcc and python on PATH.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$board = "..\..\projective-blocking-kyouen-20261125\output\board_pg2q5.txt"

function Check($name) {
    if ($LASTEXITCODE -ne 0) { throw "step failed: $name (exit $LASTEXITCODE)" }
}

$total = [System.Diagnostics.Stopwatch]::StartNew()

gcc -O2 -Wall -Wextra -o enum_safe.exe enum_safe.c
Check "compile enum_safe"
gcc -O2 -Wall -Wextra -o brute_count.exe brute_count.c
Check "compile brute_count"
gcc -O2 -Wall -Wextra -o grundy_level.exe grundy_level.c
Check "compile grundy_level"
gcc -O2 -Wall -Wextra -o grundy_rec.exe grundy_rec.c
Check "compile grundy_rec"

$t = [System.Diagnostics.Stopwatch]::StartNew()
python task1_board.py > task1_out.txt
Check "task1_board"
Write-Host ("task1_board             {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

$t.Restart()
.\enum_safe.exe $board safesets.bin > enum_out.txt
Check "enum_safe"
Write-Host ("enum_safe (DFS)         {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

$t.Restart()
.\brute_count.exe $board 12 > brute_out.txt
Check "brute_count"
Write-Host ("brute_count (all 0..12) {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

$t.Restart()
.\grundy_level.exe safesets.bin grundy_values.bin > grundy_level_out.txt
Check "grundy_level"
Write-Host ("grundy_level DP         {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

$t.Restart()
.\grundy_rec.exe $board 24 > grundy_rec_out.txt
Check "grundy_rec"
Write-Host ("grundy_rec DP           {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

$t.Restart()
python verify_sample.py > verify_sample_out.txt
Check "verify_sample"
Write-Host ("verify_sample           {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

$t.Restart()
python task5_parity.py > task5_out.txt
Check "task5_parity"
Write-Host ("task5_parity            {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

$t.Restart()
python compare_claims.py > compare_out.txt
Check "compare_claims"
Write-Host ("compare_claims          {0,7:N2}s" -f $t.Elapsed.TotalSeconds)

Write-Host ("TOTAL                   {0,7:N2}s" -f $total.Elapsed.TotalSeconds)
Write-Host "RESULT: all steps completed"
