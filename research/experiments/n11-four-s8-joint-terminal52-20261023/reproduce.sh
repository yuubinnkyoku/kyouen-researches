#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
g++ -std=c++17 -O3 -Wall -Wextra verify_s10_direct.cpp -o /tmp/n11-four-root-52-verify-$$
trap 'rm -f /tmp/n11-four-root-52-verify-$$ /tmp/n11-four-root-52-result-$$' EXIT
awk '{print $1}' s10-all1017.tsv > /tmp/n11-four-root-52-result-$$
/tmp/n11-four-root-52-verify-$$ /tmp/n11-four-root-52-result-$$ /tmp/n11-four-root-52-result-$$.tsv
trap 'rm -f /tmp/n11-four-root-52-verify-$$ /tmp/n11-four-root-52-result-$$ /tmp/n11-four-root-52-result-$$.tsv' EXIT
cmp s10-all1017.tsv /tmp/n11-four-root-52-result-$$.tsv
python3 verify_global.py
python3 mutation_test.py
sha256sum -c SHA256SUMS
