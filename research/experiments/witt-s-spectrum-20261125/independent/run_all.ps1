# Full reproduction of the independent W_24 s-game verification.
# Run from this directory (or invoke with its path).  Requires python 3.10+ and gcc.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path out | Out-Null

# --- 0. build the C verifier -------------------------------------------------
gcc -O2 -march=native -o witt.exe witt.c

# --- 1. board is the Witt design S(5,8,24) -----------------------------------
python task1_board.py

# --- 2. Python full solve (DAFs + full Grundy/misere DP), s=1..6 -------------
python task2_python.py 1 2 3 4
python task2_python.py 5
python task2_python.py 6          # takes several minutes

# --- 3/4. Golay code and dodecad identification ------------------------------
python task3_golay.py

# --- C engine: DFS enumeration + full mex DP for every s --------------------
foreach ($s in 1..7) {
    .\witt.exe full $s | Tee-Object -FilePath out/c_full_s$s.txt
}
# second, independent enumeration for s=6 and s=7
.\witt.exe fullbrute 6 | Tee-Object -FilePath out/c_fullbrute_s6.txt
.\witt.exe fullbrute 7 | Tee-Object -FilePath out/c_fullbrute_s7.txt
# dump s=7 tables (used by the sampling cross-check below)
.\witt.exe full 7 dump | Tee-Object -FilePath out/c_full_s7.txt

# --- C engine: exhaustive per-size subset scans -----------------------------
# every C(24,k) subset is examined for each relevant k; prints SAFE/MAXIMAL
foreach ($k in 1..2)  { .\witt.exe brute 1 $k }
foreach ($k in 1..3)  { .\witt.exe brute 2 $k }
foreach ($k in 1..4)  { .\witt.exe brute 3 $k }
foreach ($k in 1..5)  { .\witt.exe brute 4 $k }
foreach ($k in 1..7)  { .\witt.exe brute 5 $k }
foreach ($k in 1..13) { .\witt.exe brute 6 $k }
foreach ($k in 1..14) { .\witt.exe brute 7 $k }
# C-side code checks
.\witt.exe code
.\witt.exe dodecads

# --- 5. independent cross-check of the s=7 DP tables ------------------------
python task5_crosscheck.py

# --- claim comparison -------------------------------------------------------
python compare_claims.py
