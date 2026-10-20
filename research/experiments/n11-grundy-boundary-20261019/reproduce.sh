#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for i in 0 1 2 3; do python3 grundy_boundary.py --shard "$i"; done
python3 grundy_boundary.py --merge
${CXX:-g++} -std=c++20 -O3 -Wall -Wextra -o /tmp/n11_grundy_direct_verify_$$ verify_grundy_direct.cpp
/tmp/n11_grundy_direct_verify_$$ s10-input.txt s10-cpp-results.tsv
rm -f /tmp/n11_grundy_direct_verify_$$
python3 audit_crosscheck.py
sha256sum -c SHA256SUMS
