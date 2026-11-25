# Reproduce the whole independent verification (PowerShell, from this directory).
# Python 3.10+ standard library only; C compiled with gcc (or clang/cc).
$ErrorActionPreference = "Stop"

Write-Host "== build =="
gcc -O2 -std=c11 -Wall -Wextra -o pg8.exe pg8.c
if ($LASTEXITCODE -ne 0) { throw "gcc failed" }

Write-Host "== C engine: verify + order + census + decompose + orbits + quads =="
.\pg8.exe all "..\output\board_pg2q8.txt" > results_c.txt
if ($LASTEXITCODE -ne 0) { throw "pg8.exe failed" }

Write-Host "== task 1: board is PG(2,8) =="
python task1_board.py

Write-Host "== task 2: |PGL(3,8)| and collineations =="
python task2_group.py

Write-Host "== task 3: orbit sizes of the K1327 start caps (python BFS) =="
python task3_orbits.py

Write-Host "== task 4: conic layer =="
python task4_conics.py

Write-Host "== task 5: arithmetic =="
python task5_arithmetic.py

Write-Host "done"
