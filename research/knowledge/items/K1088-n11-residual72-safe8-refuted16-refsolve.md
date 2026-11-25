---
id: K1088
title: "残余72行 safe8 pool の REFUTED-D10 16根除外後再解決: 残余49行は16代替根で leftover 0 完全被覆（stranded 0・最大マッチング49・WIN8内在被覆は主張と一致）"
kind: computation
status: computed
topics: [search-methods, certificates, geometry, planning]
aliases:
  - post-exclusion re-solve of the residual 49 rows over the safe8 pool minus the 16 REFUTED-D10 roots of the K1086 add-two greedy-23 depth-10 sweep
  - 16 replacement roots (greedy, gains {4:3, 3:11, 2:2}) cover all 49 rows with zero stranded rows; lower bound 13; perfect bipartite matching 49
  - independent re-execution of the K1085 universe82/safe8/demand/greedy-23 plan (exact root-sequence and marginal-coverage reproduction) from the two published正本 only
relations:
- type: depends_on
  target: K1086
  note: depth-10 verdict join (7 WIN8 candidates + 16 REFUTED-D10 facts, both orderings uncapped) and the 23+49 row partition of the greedy plan
- type: depends_on
  target: K1085
  note: pinned census正本 (SHA-256 5fdd342d…) supplies the 72 rows, universe82 aggregates, and the greedy-23 plan reproduced independently here
- type: depends_on
  target: K1069
  note: sweep protocol reference (runner v17); this computation itself runs no probes
artifacts:
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/README.md
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/scripts/safe8_refuted16_refsolve_20261120.py
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/output/safe8-refuted16-refsolve-20261120.json
- path: research/log/2026-11-20-n11-residual72-safe8-refuted16-refsolve.md
evidence: |
  K1086「次の一手」第2項。K1086掃引でREFUTED-D10と確定した16根をsafe8 pool
  （120,474根）から除外し、greedy計画上この16根が主張被覆していた残余49行の
  代替被覆を再解決した。入力はK1085 census正本（SHA-256 5fdd342d…）と
  K1086掃引正本（SHA-256 3045e152…）のみをfail-closed pinで読む。本機械は
  universe82（generation witness 471,960 events→canon dedup 380,098根・
  unsafe8 259,624・safe8 120,474）・coverage（hist {1:82,602, 2:33,104,
  3:4,718, 4:50}・demand min 1,714/max 2,944/sum 163,164）・coverage
  crosscheck 39,255根（全C(8,6)=28部分集合再導入）をK1085実験と独立に再導入し、
  **lex-smallest max-gain greedy 23根計画（根順序と各根の主張被覆行の両方）を
  完全再現**した上で、除外後 pool P（120,458根）上の残余49行再解決を得た。
  結果: (1) 残余49行の除外後 demand は合計109,719・min 1,713・max 2,943で
  **stranded行0**（16 REFUTED根が唯一の供給源になる行は皆無）。
  (2) **greedy 16根が49行をleftover 0で完全被覆**（gains {4:3, 3:11, 2:2}）。
  情報論的下界ceil(49/4)=13に対し+3。 (3) **二部最大マッチング49**
  （全行に互いに異なる被覆根が存在・每行1根のwitnessも構成可能）。
  (4) **WIN8-D10 candidate 7根の内在被覆は主張23行と完全一致**（残余49行への
  巻き込みなし）なので、将来のWIN8 receipt fold 需要49行の需要構造は不変
  （scope1=scope2の同一16根で機械保証）。全体計画は7 WIN8根+16代替根=23根で
  72行を被覆（元計画と同数の23根）。代替16根は未掃引で、depth-10掃引には
  両AND順序32 probesが必要（候補であり証明書ではない）。
  正本SHA-256 16b38d04a488617b1b8c002c6a5f3171038f557cd3cca8b8e4dbd4657bc2f724・
  同一cwd2回+別cwd別プロセス1回の3実行byte-identical・全16 gate PASS・
  stdlibのみ・乱数・時刻を正本に含まない。greedy/witnessは条件付き計画
  （候補根の簿記）であり証明書ではない。行の閉鎖claim・証明書抽出・
  receipt foldの設計は本項目の対象外。REFUTED-D10はLOSS証明ではない。
  nodes数・solved数を勝敗として読まない。標準11×11空盤・二石root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。
---
