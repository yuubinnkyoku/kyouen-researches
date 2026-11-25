#!/bin/bash
# Bootstrap: re-download every pinned input after an environment reset.
set -e
cd "$(dirname "$0")"
B=https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/main
E=$B/research/experiments
mkdir -p inputs chain scripts out/ccp-reexec out/wave2-refresh out/fourthcost-probe \
         out/merger-selftest probe/input probe/raw val gate fakeroot/results \
         fakeroot/research/experiments/probepart/scripts
get() { # $1 dest  $2 url  $3 sha256 (TBD = download without pin check)
  if [ "$3" = "TBD" ]; then curl -sS -o "$1" "$2"; return 0; fi
  if [ -f "$1" ] && echo "$3  $1" | sha256sum -c --quiet 2>/dev/null; then return 0; fi
  curl -sS -o "$1" "$2"
  echo "$3  $1" | sha256sum -c --quiet || { echo "PIN FAIL: $1"; exit 1; }
}
get inputs/geometry.json.gz $E/n11-strategy-redesign-20261010/output/geometry.json.gz 146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54
get inputs/merged-exact-s5-after-js-probe-13.cache $E/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache 60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6
get inputs/shared-s5-tasks.csv $E/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/shared-s5-tasks.csv 31f0d29b820a69508af0c352c22f09b244bff5b9ae79476679047cdb160ea954
get inputs/candidate-classes.csv $E/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/post-probe/candidate-classes.csv 2a4c2382d812102f8132339c871b07ee998e933c80da876759e51e84f64fda80
get inputs/historical-cost-profile.json $E/n11-strategy-redesign-20261010/output/historical-cost-profile.json 6b2971e53059ac36af7bf161a61d90d65f85e604e27b93d013e7a2853fdceddc
get inputs/jsreplay.js $E/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/scripts/jsreplay.js 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df
get inputs/independent.py $E/n11-independent-exact-audit-20261010/scripts/independent.py 954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f
get inputs/s5_evidence_policy.py $E/n11-frontier-selection-20261005/scripts/s5_evidence_policy.py 78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2
get inputs/n11-s5-evidence-quarantine.json $B/results/n11-s5-evidence-quarantine.json 81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9
get inputs/ccp-class_closure_priority.py $E/n11-s5-class-closure-priority-20261121/scripts/class_closure_priority.py 2aa249d883d3948cf3c617d044f202eb0dac616005b7ce036658d8360a7d48b2
get inputs/sbd-corpus-def.json $E/n11-s4bd-fresh-corpus-regen-20261121/input/corpus-def.json 779685a789dd2ab83266f685d26ffd6d25ab12ef33f2252320e4e6e1b0823585
get inputs/ccp-published-class-closure-priority.json $E/n11-s5-class-closure-priority-20261121/output/class-closure-priority.json c837c52d252a632a2d247e0cac50222e2bf641062c8afd7ecdd4f839c67dcea6
get inputs/ccp-published-class-closure-priority.csv $E/n11-s5-class-closure-priority-20261121/output/class-closure-priority.csv 139eb0a0e3453309adcd617e9ca68ddd0615244c5e59f814d8c08bed5d69de87
# val gate inputs + published expected outputs
V=$E/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/input/val
O=$E/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/raw
get val/at2m-s5-1152921504606851072-536870946.input.csv $V/at2m-s5-1152921504606851072-536870946.input.csv ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348
get val/at2m-s5-1188950301626860544-536870912.input.csv $V/at2m-s5-1188950301626860544-536870912.input.csv 56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62
get val/first-15m-s5-1152921504606851072-536870946.input.csv $V/first-15m-s5-1152921504606851072-536870946.input.csv ecc0299b8142abde201fcc40ea9666dac7368d0888d0600abc717af66ddfe348
get val/second-15m-s5-1188950301626860544-536870912.input.csv $V/second-15m-s5-1188950301626860544-536870912.input.csv 56aacb71769b231c9728dcc841d39f0d5cb579517d34769f0e7382516d4c3a62
get val/val-at2m-first.expect.csv $O/val-at2m-first.out.csv d766154adda47bd2af09905fa8d3e709abc7192596b928d5ff1251f1e1c911e7
get val/val-at2m-second.expect.csv $O/val-at2m-second.out.csv 23e36443eb69d120e271cd80b8391f86873daf747ee1c7f78e91fc92fc1c6ebe
get val/val-first-15m.expect.csv $O/val-first-15m.out.csv 7f5040ae9358e780c61345f41a224d68d2a7f3c4f1ae782ed7701ecf2e19e092
get val/val-second-15m.expect.csv $O/val-second-15m.out.csv c45ea3fa8654241cdd2aa874c86ded1110a3527b159bb657b5ecdac4f68c2e6e
# chain caches
cp -f inputs/merged-exact-s5-after-js-probe-13.cache chain/merged-exact-s5-after-js-probe-13.cache
D=n11-reply27-s5-jsreplica-probe
for spec in "p01 1306114260682670080-20261121 -1" "p02 10376293541461622788-20261121 -2" "p03 10376293541461622788-77309411328-20261121 -3" "p04 10376293541461626880-12288-20261121 -4" "p05 10376293541461626880-134217744-20261121 -5" "p06 10376293541461626880-134225920-20261121 -6" "p07 10376293541461626880-150994944-20261121 -7" "p08 10376293541461626880-16777232-20261121 -8" "p09 10376293541461626880-16785408-20261121 -9" "p10 10376293541461626880-18874368-20261121 -10" "p11 10376293541461626880-25165824-20261121 -11" "p12 10376293541461626880-34359742464-20261121 -12" "p13 10376293541461626880-40960-20261121 -13"; do
  set -- $spec
  if [ ! -s "chain/chain-$1.cache" ]; then curl -sS -o "chain/chain-$1.cache" "$E/$D-$2/output/merged-exact-s5-after-js-probe$3.cache"; fi
done
get chain/base-merged-exact-s5.cache $E/n11-two-target-design-20261010/output/merged-exact-s5.cache 24e97b746667bd1c5468d5203e8444a0d379023f6c67facaf9bbd4787c3759e6
get chain/merged-exact-s5-after-class-excl-1.cache $E/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/merged-exact-s5-after-class-excl-1.cache bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0
# decl note (for the 41-key enumeration cross-check)
get decl-note.md $B/research/log/2026-11-21-n11-s5-wave2-refresh-union-merge-fourthcost-probe-single-owner.md 3726afd98a23a72386a955f8f3377104ae79f447d299acb229109d7ff95782f0
echo "BOOTSTRAP OK"
