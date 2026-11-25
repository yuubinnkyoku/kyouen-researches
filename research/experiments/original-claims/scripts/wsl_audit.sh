#!/usr/bin/env bash
R=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches
python3 "$R/research/experiments/original-claims/scripts/crt_threshold_audit.py" > /tmp/audit.log 2>&1
cat /tmp/audit.log
