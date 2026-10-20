#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
python3 verify_s6_win.py
python3 mutation_tests.py
g++ -std=c++20 -O3 -DNDEBUG -o /tmp/n11_s7_38_terminal_check verify_s10_direct.cpp
/tmp/n11_s7_38_terminal_check s10_leaves_857.txt /tmp/n11_s7_38_cpp.tsv
cmp s10_cpp_results.tsv /tmp/n11_s7_38_cpp.tsv
printf 'PASS all standalone independent checks\n'
