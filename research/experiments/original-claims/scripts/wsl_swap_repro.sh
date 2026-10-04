#!/usr/bin/env bash
S=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/original-claims/scripts
g++ -O0 -g -o /tmp/swap_repro "$S/swap_repro.cpp" || exit 1
/tmp/swap_repro
