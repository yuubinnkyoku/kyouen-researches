---
id: K1107
title: 残余68行のWIN8-D10 receipt fold root 8005021（fold12・第19 receipt・2番目のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold12 WIN8 receipt fold root 8005021
  - K1106証明書の五親frontierチェーンへのfoldと残余68→65行
relations:
  - type: depends_on
    target: K1106
    note: WIN8-D10証明書（root 00000000000000003800000008005021・26,083行・SHA-256 69f32661…）と19 gate抽出正本。証明自体は本項で再実行せずhash pin・gate再検証のみ
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張3行（intrinsic == claimed・exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1105
    note: fold11正本（SHA-256 d7bf2cd5…）。fold12機械はfold11出版機械をbyte-identical再実行した上でfold11レコードをchainingした
  - type: depends_on
    target: K1086
    note: addtwo-greedy23掃引のroot 8005021 probe記録（両AND順序uncapped 619,138/751,581・loss=true）とgreedy被覆3行の主張源
artifacts:
  - path: research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/scripts/fold_win8_root8005021.py
    role: verifier
    note: 純Python・乱数なし。チェーン全段frontier再計算・fold11再実行gate・K1106/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual68-win8-receipt-fold-root8005021-20261120/output/win8-root8005021-receipt-fold-20261120.json
    role: data
    note: fold12正本（status fold-complete・SHA-256 0f73795c…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold12-win8-root8005021-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold12-win8-root8005021-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit 7bb492cd・先行出版）
---

# fold12: WIN8-D10 receipt fold of root 8005021

単一オーナー宣言ノート（commit `7bb492cd`・先行出版）の下で、K1106 の WIN8-D10 証明書
（root `00000000000000003800000008005021`・26,083 行・SHA-256 `69f32661…`・19 gate・三重検証）を
第19 receipt・2番目の WIN8 receipt fold として五親 S6 frontier チェーンに fold した。

機械 `fold_win8_root8005021.py` は fold11 機械の移行型で、
(a) チェーン全段の frontier を worklist から再計算し（6,259/495,507 → … → 6,206/491,497 → fold11 chaining 6,201/491,110・incidence 11,803・residual 68 まで全段 gate）、
(b) fold11 出版機械を本環境で再実行して出版正本（SHA-256 `d7bf2cd5…`）と byte-identical であることを gate で確認した上で、
(c) K1106 19 gate・証明書本文（byte 数 945,298・行数 26,083・sorted-unique・header）・root 幾何（8石・quadruples 0・D4 正準・合法手 41 の独立再導出）を再検証し、
(d) K1097 refsolve 27 gate・win16 intrinsic footprint（root 8005021: intrinsic == claimed == 3 行・49 行 exactly-once partition）・residual23 と win16 主張の不交差（残余23行掃引計画に影響しないこと）を機械確認し、
(e) 被覆幾何を「8 D4像×C(8,2) 2石除去 224 操作」と「root の C(8,6)=28 部分集合直列挙」の 2 方法で独立計算して canonical 行集合が完全一致（refsolve coverage_of82 と同一規約・D4 同変性）する様に閉じた計算で再導出した。

## 結果

- **receipt は open 8 行を閉じた**（単一 WIN8 receipt としては最多）。K1106/K1097 主張 3 行
  `00000000000000003800000008001001`（cost 74）・`…8001020`（cost 65）・`…8005000`（cost 71・5親 target 内）に加え、
  **target 外・worklist 上の open 行 5 行** `00000000000000003800000000004021`（cost 79）・`…0005020`（cost 80）・
  `…08000021`（cost 69）・`…08004001`（cost 77）・`…08004020`（cost 69）を併閉した。
  **余剰行（5）が主張行（3）を数で上回った初の receipt**。余剰 5 行は c1 需要行が多く（c1×2 が 2 行・c1 単独 2 行・c2 1行）、class-1 側需要の簿記上の前進として記録される。
  closed edge cost 584。主張 3 行は再導出結果と完全一致（g07 gate）。
- 5親112行 target: 44 → 47 行・残余 68 → 65 行。
- frontier: 6,201/491,110 → 6,193/490,526・solved S6 1,647 → 1,655・parent 行 incidence 11,803 → 11,790
  （影響 5 parent: c1 3〔58→56・65→63・75→72〕・c2 2〔44→41・25→22〕・完全閉鎖 0）。
- s6_needed_by_open_classes 4,504 → 4,501・cost_needed_by_open_classes 357,196 → 356,974。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 8（本 receipt で閉鎖）・not-in-worklist 20。
- 出力正本（SHA-256 `0f73795ce71aec83ba4a9f1b97a530891f3e6d1c807bfa47c9fbb88a1b33f5bd`）は同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical。

K1097 の残余23行掃引計画（第5ラウンド・並走宣言済み）は不変。残り 14 WIN8 候補（主張 42 行）の証明書抽出と fold、
残余 65 行の refsolve は本項の対象外で未着手のまま（着手時に単一オーナー宣言を要する）。

## 解釈上の制限（不変）

- WIN8-D10 はこの 8 石 root のゲーム木のみを証明する。receipt fold は frontier の閉鎖簿記であり、閉じた行や target のゲーム理論的値を主張しない。
- REFUTED-D10 は LOSS 証明ではない。pn/dn・nodes・solved 数を勝敗として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
