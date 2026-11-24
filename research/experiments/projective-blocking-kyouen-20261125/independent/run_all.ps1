# Runs the complete independent verification (standard library only).
$ErrorActionPreference = "Stop"
python task1_boards.py
python task2_grundy.py
python task2b_grundy_q4.py
python task3_maximal.py
python q4_profile_representatives.py
python task4_k3.py
python task5_lemma.py
Write-Host "All steps finished."
