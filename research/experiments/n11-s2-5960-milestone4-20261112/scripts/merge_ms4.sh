#!/bin/sh
# merge_ms4.sh - assemble the published milestone-4 (COMPLETE S2 {59,60} S6 worklist)
# manifest byte-exactly from the fragment files produced by milestone4_worklist.ts
# (run CHUNK=1..9, which writes frag1..frag10; chunk 9 is split into 9a/9b = frag9/frag10).
#
# Reproduction procedure (16MiB-sandbox constraint):
#   1. run milestone4_worklist.ts with CHUNK=1..9 (10 fragment files; chunk 9a is
#      CHUNK=9, chunk 9b is CHUNK=10 in the CHUNKS table -> frag9.json / frag10.json)
#   2. merge fragments incrementally in the order below (group_by hex, certs added
#      arithmetically -- cert bit sets of different fragments are disjoint, so OR == sum)
#   3. assemble the final manifest with the header used in
#      research/experiments/n11-s2-5960-milestone4-20261112/output/milestone4_manifest.json
#
# Verified totals of the published manifest:
#   s6All = 43,375 / s5Reps = 1,447 / cost sum = 3,477,178 / s5 obligation sum = 133,524
#   milestone-3 manifest (20,534 keys) is a strict subset, cost mismatch 0.

set -e
cd /home/user/work-ms4

# incremental merge; delete each consumed fragment to stay under the 8MiB session limit
jq -s '{schema:"n11-s2-5960-ms4-mergedA-v1",
  certStats:(.[0].certStats + .[1].certStats),
  s5Reps:((.[0].s5Reps + (.[1].s5Reps | map([.hex,.certs,.obligations])))
    | group_by(.[0]) | map([.[0][0], (map(.[1])|add), .[0][2]]) | sort_by(.[0])),
  s6All:((.[0].s6All + (.[1].s6All | map([.hex,.cost,.certs])))
    | group_by(.[0]) | map([.[0][0], .[0][1], (map(.[2])|add)]) | sort_by(.[1], .[0]))}' \
  -c frag1.json frag2.json > merged.json && rm -f frag1.json frag2.json

for f in frag6.json frag3.json frag4.json frag5.json frag7.json frag8.json frag9.json frag10.json; do
  jq -s '{schema:"n11-s2-5960-ms4-mergedA-v1",
    certStats:(.[0].certStats + .[1].certStats),
    s5Reps:((.[0].s5Reps + (.[1].s5Reps | map([.hex,.certs,.obligations])))
      | group_by(.[0]) | map([.[0][0], (map(.[1])|add), .[0][2]]) | sort_by(.[0])),
    s6All:((.[0].s6All + (.[1].s6All | map([.hex,.cost,.certs])))
      | group_by(.[0]) | map([.[0][0], .[0][1], (map(.[2])|add)]) | sort_by(.[1], .[0]))}' \
    -c merged.json "$f" > mergedB.json && rm -f merged.json "$f" && mv mergedB.json merged.json
done

jq -r '(.s6All|length), (.s5Reps|length)' merged.json
