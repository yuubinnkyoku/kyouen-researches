#!/bin/sh
# merge_manifest.sh - assemble the milestone-3 compact manifest from the repo
# milestone-2 output (ms2.json, field-name format) and the fresh certs 6-8 union
# (fresh678.json, emitted by milestone3_worklist.ts).
# Usage: sh merge_manifest.sh ms2.json fresh678.json > milestone3_manifest.json
# Reproduces the published output/milestone3_manifest.json byte-exactly
# (schema n11-s2-5960-milestone3-s6-manifest-v1-compact, 627770 bytes).
A="$1"; B="$2"
jq -n --slurpfile a "$A" --slurpfile b "$B" '
 ($a[0]) as $m2 | ($b[0]) as $fr |
 ($m2.s6All | map({key:.hex, cost:.cost, certs:.certs})) as $s2 |
 ($fr.s6All | map({key:.hex, cost:.cost, certs:.certs})) as $s6 |
 ($s2 + $s6 | group_by(.key) | map(if length==1 then .[0] else (.[0] + {certs: (map(.certs)|add)}) end)) as $mergedAll |
 ($m2.s5Reps | map({key:.hex, certs:.certs, obligations:.obligations})) as $r2 |
 ($fr.s5Reps | map({key:.hex, certs:.certs, obligations:.obligations})) as $r6 |
 ($r2 + $r6 | group_by(.key) | map(if length==1 then .[0] else {key:.[0].key, obligations:.[0].obligations, certs:(map(.certs)|add)} end)) as $mergedS5 |
 ($mergedAll | map(.cost) | sort) as $cs |
 def unpad: sub("^0+";"");
 {
   schema: "n11-s2-5960-milestone3-s6-manifest-v1-compact",
   board: 11, root_s2: "{59,60}", best_s3: 61,
   conditional_on: $m2.conditional_on,
   greedy_order: "K0729 greedy certs 1-8: {5,115} -> {27,93} -> {71} -> {82} -> {104} -> {73} -> {90,96} -> {23}; 12 of 60 blockers closed; certBits 1,2,4,8,16,32,64|128,256 in order ({90} and {96} are D4-mirror-identical orbit sets, bits 64+128 always co-occur)",
   certStats: [($m2.certStats[]), ($fr.certStats[])],
   s5UnionOrbits: ($mergedS5|length),
   s6Union: ($mergedAll|length),
   s6CostStats: {
     min: $cs[0],
     median: $cs[($cs|length/2|floor)],
     max: $cs[-1],
     mean: (($cs|add)/($cs|length)*1000|round/1000),
     sumRawS7Edges: ($cs|add)
   },
   entryFormat: "s6All entries are [unpaddedLowercaseHex, cost, certs] where unpaddedLowercaseHex = BigInt canonical 121-bit board key written in hex without leading zeros (zero key would be impossible here; keys are nonempty). s5Reps entries are [unpaddedLowercaseHex, certs, obligations]. s6All is sorted by (cost, paddedHex) ascending - identical ordering to the field-name format. certs = bitmask over the 9 certStats entries ({90},{96} identical sets, bits 64+128 joint).",
   s5Reps: ($mergedS5 | sort_by(.key) | map([( .key | unpad), .certs, .obligations])),
   s6All: ($mergedAll | sort_by(.cost, .key) | map([(.key | unpad), .cost, .certs])),
   protocol: "verdict = WIN_for_mover iff the 6-stone rep has a legal child classified WIN7 (mover-at-S7 loses). A WIN certificate needs exactly one certified WIN7 child key; a LOSS certificate needs all legal children certified. Merge rule: two workers disagreeing on one canonical key = WIN/LOSS conflict, halt certificate assembly. D4 invariance: certify one rep per orbit only. Cost = number of legal S7 children of the rep (raw S7 edges).",
   cross_checks: "single-cert S6 orbits 2191/2150/2421/2516/2563 (K0746) and 3868/4232/4232/4416 (K0729/K0748 ladder); cumulative union 2191/4262/6517/8780/10988 (milestone-2, K0748) -> 14134 -> 17395 -> 20534; fresh certs 6-8 mutual union 11794; merged union 20534 = 49.1% of 41842; {73} raw obligations 7890 matches verify_conditional_s6_cover_46.py; {90} and {96} orbit sets D4-mirror-identical; milestone-2 10988 keys are a subset with identical costs (verified with padded-hex group_by join, cost mismatch 0).",
   empty_board: "UNKNOWN"
 }
' | jq -c .
