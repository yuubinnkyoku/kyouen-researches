---
id: K1067
title: "windfall 4証明書receipt fold（第13〜第16 receipt・fold機械の全連鎖gateをbase 6,259/495,507から再計算・第9〜第12 receipt被覆は幾何再導出で出版記録と一致・frontier 6,213行/492,021 cost→6,209/491,722・solved S6 1,635→1,639・incidence 11,826→11,818・5親target 34→38/112・残余78→74行・閉鎖はちょうど4行で副次閉鎖なし）"
kind: computation
status: computed
topics: [coverage, receipts, verification]
aliases:
  - thirteenth-sixteenth windfall receipt fold: the four certificate-backed cost65h-lane windfall WIN7-D10 roots (child 00000000000000803202000000001000, bit 40/43/99/118) are consumed as receipts and their covered residual rows are closed in the five-parent head-1410 frontier bookkeeping
  - full chain recomputation and gating: base frontier 6,259/495,507 through cost78c/79c, first, second/third, fourth, fifth/sixth, seventh and eighth receipts to the published 6,222 rows/492,688 cost (parent incidence 11,848), verdict universe 340/164 pre-sweep43 and 379/168 post-sweep43, all recomputed from sha256/blob-pinned inputs
  - ninth-twelfth fold record re-derived: published record sha256-pinned (ee002d79...), its four sweep43 WIN receipts' covered S6 rows, target rows and post-twelfth frontier (6,213/492,021, solved 1,635, needed 4,513/357,882, incidence 11,826) re-derived by geometry and gated byte-for-byte against the record
  - per-receipt windfall gates: raw root = c65h|1<<bit construction, canonical mapping (bit 99/118 raw roots are D4 non-canonical, gate-checked against the K1063 evidence roots), certificate sha256/bytes/header/root line, blind extraction run1/rerun byte-identical with per-move ok/uncapped and fbt_drops 0, TS Bareiss subroot stats + union audit, pure-python exact Bareiss replay, BigInt independent verification, cross-method state-flow equality, runner v16 fresh nodes node-exact vs the published raw batch3/4/7/8 bit lines, pilot_d6 control line, legal-move rederivation (48/58/52/56), win/loss conflict scan against the published verdict universe, and covered residual rows equal to the resolve6/K1066 records
relations:
- type: depends_on
  target: K0001
  note: 標準11×11の合法手・安全性判定・D4正準形規約
- type: depends_on
  target: K0003
  note: 解決段階の区別（foldは行被覆の簿記であり勝敗確定ではない）
- type: depends_on
  target: K0863
  note: cost-lane corpus体系と正準形verdict cache（raw bit_line出典の下流）
- type: depends_on
  target: K1063
  note: resolve6正本（SHA-256 e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a）のwin-coverage-of-residual evidenceが4根・被覆行・raw batch provenanceの出典
- type: depends_on
  target: K1066
  note: 三重独立検証済み証明書とK1066 fail-closed検証正本（SHA-256 a3ca1b3df...、50 gate全PASS）がreceiptの裏付け
artifacts:
- path: research/experiments/n11-residual78-windfall4-receipt-fold-20261120/README.md
  role: data
  note: 実験README（fold方式・連鎖gate・結果表・解釈規約）
- path: research/experiments/n11-residual78-windfall4-receipt-fold-20261120/scripts/fold_windfall4.py
  role: verifier
  note: fold機械本体（fold9全連鎖gate再現・第9〜第12幾何再導出・windfall 4 receipt gate・fail-closed）
- path: research/experiments/n11-residual78-windfall4-receipt-fold-20261120/output/windfall4-thirteenth-sixteenth-win7-receipt-fold-20261120.json
  role: data
  note: fold正本（2回実行byte-identical・SHA-256 24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2）
scope: >-
  windfall 4証明書receipt fold（第13〜第16 receipt）の閉鎖計上まで。
  残余74行のwitness計画再計算（resolve7相当）・39 live witness掃引の
  更新・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・標準11×11
  空盤の勝敗確定は対象外。
evidence: >-
  （1）出典と入力pin: fold機械はwindfall 4根のverdict出典としてresolve6
  正本（SHA-256 e85d4bfb…）、裏付けとしてK1066検証正本（SHA-256
  a3ca1b3df…・全50 gate PASS）をsha256 pinで読み、証明書4本はK1066実験
  certs/から直接読む（sha256 02778cf5…/27e60fdca5…/04f545c88…/
  05356cbc16…）。chain入力（worklist・ledger・census・globalFold・
  previousCostFold・firstFoldTarball・cover49・coverResolve1・head1476・
  cost78c/79c/73j・joint・audit・sweep48・fold23・fold4/fold56/fold7/
  fold8・resolve4/5・sweep35・sweep6・sweep28・sweep43・
  fold_fourth_fifth_sixth.py）はfold9機械と同一のblob/sha256 pin集合で
  mainから取得し照合。（2）全連鎖再計算: base frontier 6,259/495,507 →
  cost78c/79c後6,240/493,965 → first後6,236/493,703 → second/third後
  6,229/493,184 → fourth後6,226/492,970 → fifth/sixth後6,224/492,830 →
  seventh後6,223/492,762 → eighth後6,222/492,688・incidence 11,848・
  verdict universe 340/164 → sweep43後379/168、全gate再現。
  （3）第9〜第12 receipt: 出版fold9記録（sha256 ee002d79…）のsweep43
  WIN 4根からcovered S6 rows（9行・うちtarget 8行＋extra 1行）・
  5親target 34/112・残余78行・frontier 6,213/492,021・solved 1,635・
  needed 4,513/357,882・incidence 11,826を幾何再導出し、出版記録の全
  row list・統計と一致をgate。resolve5正本（sha256 5a2f4815…）の
  基底残余78行とも完全一致。（4）windfall 4 receipt: 各bit について
  raw root = c65h|1<<bit を再構築し、canonical写像（bit 99: canonical
  00000000000000803800000008001200、bit 118: 000000000100008038000000
  08100000）がresolve6 evidence rootと一致、popcount 7・unsafe
  quadruples 0をgate。証明書はroot行=raw root（K1046の事故教訓を継承）
  でsha256照合・header・行数・K1066抽出summary（run1/rerun nodes
  3,074,926/7,700,023/3,355,354/6,137,302・rows 31,189/51,767/36,625/
  55,838・fbt_drops 0・per-move全ok/uncapped・rerun byte-identical）と
  照合。三重検証（TS Bareiss 4x4・aggregate seen/terminals/opponent
  edges、純python exact Bareiss replay・terminal {13,15,17}、BigInt 3x3
  余因子・terminal [13,17]）を再読みし、bigintとTS Bareissの状態流量
  一致をgate。runner v16 fresh再現nodes 1,105,860/3,269,824/1,114,855/
  2,307,338がresolve6出版raw bit_line（batch3/4/7/8）とnode-exact一致・
  pilot_d6対照 loss=false 3,402 nodes合格。legal move 48/58/52/56を
  独立再導出。WIN/LOSS衝突0（出版41万verdict universe明示結合379/168に
  対しconflict scan）。（5）閉鎖計上: 各rootの8 D4像・全single-bit
  削除でcovered open frontier rowsを再導出し、被覆4行
  （00000000000000801202010000001000 cost64・
  00000000000000801202080000001000 cost79・
  00000000000000003800000008001200 cost76・
  00000000010000003800000008100000 cost80）がresolve6/K1066の
  covered_residual_rowsと完全一致・fold前から開放・二重閉鎖なしを
  gate。副次閉鎖は0行（ちょうど4行だけ）。frontier 6,213/492,021 →
  6,209/491,722・solved 1,635→1,639・incidence 11,826→11,818・needed
  4,513→4,509・357,882→357,583・closed edge cost 299・fully-closed
  parent 0・affected parents 5。5親target 34→38/112・残余78→74行。
  （6）記録: 出力JSON 2回実行byte-identical（SHA-256 24db2352ad0d…）。
  snapは実行時main head 68b04984f22fe907120ded2deaf5b03182108fd7。
  （7）解釈規約: windfall receiptはdepth-10単一順
  （andclose=1）engine verdictに三重独立検証済み証明書が裏付けた
  receiptであり、sweep43系の双順序規約とは異なるvariant
  （詳細は記録のverdict_basis_note）。foldは行被覆の簿記であり、
  REFUTED-D10はLOSS証明ではなく、pn/dn・solved数を勝敗として読まない。
  残余74行の各自のreceipt出版までは閉鎖計上されず、resolve5の
  39-root live witness計画（条件付き）は74行を独自に全被覆する。
  **二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・標準11×11
  空盤はすべてUNKNOWNのまま。**
---

## 詳細

K1063（resolve6）がwindfallとして出典付きで記録し、K1066が証明書抽出と
三重独立検証を完了した4根（c65h child bit 40/43/99/118）を、fold機械で
receipt（第13〜第16）として計上した。機械はfold9の全連鎖gateをsha256
pin入力から再現し、第9〜第12 receiptの被覆は出版記録に対して幾何再導出で
一致検証した上で、windfall 4根を正当なreceiptとして閉じた。閉鎖は
ちょうど4行（78行中）、frontier探索総costは492,021→491,722、
5親targetは38/112閉鎖・残余74行。証明書の実在と三重検証はK1066の
正本にゆだね、本項のfold記録はその被覆計上のみを主張する。詳細は
[実験](../../experiments/n11-residual78-windfall4-receipt-fold-20261120/README.md)・
[研究ログ](../../log/2026-11-20-n11-windfall4-receipt-fold.md)。
