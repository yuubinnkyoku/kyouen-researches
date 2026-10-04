#!/bin/bash
# Background runner for long stages
S=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/original-claims/scripts
V=/mnt/d/ghq/github.com/yuubinnkyoku/kyouen-researches/research/experiments/original-claims/output
STAGE="$1"
echo "BG start $STAGE $(date)" >> "$V/round5_b251a_bg.log"
/tmp/round5_b251a "$STAGE" > "$V/round5_b251a_${STAGE}.json" 2> "$V/round5_b251a_${STAGE}.log"
echo "BG done $STAGE exit:$? $(date)" >> "$V/round5_b251a_bg.log"
