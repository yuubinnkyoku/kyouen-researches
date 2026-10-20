#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
python verify_joint_dag_optimized.py
python verify_direct_roots.py
python mutation_tests_optimized.py
