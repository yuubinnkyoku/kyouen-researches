---
id: K1105
title: 残余72行のWIN8-D10 receipt fold root 8003180（fold11・第18 receipt・初のWIN8 receipt fold）
kind: experiment
status: verified
topics: [search-methods, certificates, frontier-bookkeeping]
aliases:
  - fold11 WIN8 receipt fold root 8003180
  - K1096証明書の五親frontierチェーンへのfoldと残余72→68行
relations:
  - type: depends_on
    target: K1096
    note: WIN8-D10証明書（root 00000000000000003800000008003180・34,529行・SHA-256 13931289…）と18 gate抽出正本。証明自体は本項で再実行せずhash pin・gate再検証のみ
  - type: depends_on
    target: K1097
    note: win16 intrinsic footprintの主張4行（intrinsic == claimed・exactly-once partition）と残余23行掃引計画の不交差機械確認。27 gate再検証
  - type: depends_on
    target: K1102
    note: K1097第4ラウンド再解決の独立第二検証としてのrefsolve正本・safe8候補 universeの信頼根拠
  - type: depends_on
    target: K1085
    note: fold10（seventeenth）receipt fold正本。fold11機械はfold10正本をbyte-identical再実行（SHA-256 bed7d331…）の上に接続した
artifacts:
  - path: research/experiments/n11-residual72-win8-receipt-fold-root8003180-20261120/README.md
    role: source
    note: 入力pin・方法・gate・結果・解釈上の制限
  - path: research/experiments/n11-residual72-win8-receipt-fold-root8003180-20261120/scripts/fold_win8_root8003180.py
    role: verifier
    note: 純Python・乱数なし。チェーン全段frontier再計算・K1096/K1097再検証・2方法被覆幾何・target簿記更新
  - path: research/experiments/n11-residual72-win8-receipt-fold-root8003180-20261120/output/win8-root8003180-receipt-fold-20261120.json
    role: data
    note: fold11正本（status fold-complete・SHA-256 d7bf2cd5…・3実行byte-identical）
  - path: research/log/2026-11-20-n11-fold11-win8-root8003180-receipt-fold.md
    role: log
    note: 発見・実行・再現・限界の研究記録
  - path: research/log/2026-11-20-n11-fold11-win8-root8003180-single-owner-note.md
    role: log
    note: 単一オーナー宣言（commit d36e15b6・先行出版）
---

# fold11: WIN8-D10 receipt fold of root 8003180

単一オーナー宣言ノート（commit `d36e15b6`・先行出版）の下で、K1096 の WIN8-D10 証明書
（root `00000000000000003800000008003180`・34,529 行・SHA-256 `13931289…`・18 gate・三重検証）を
第18 receipt・**初の WIN8 receipt fold** として五親 S6 frontier チェーンに fold した。

機械 `fold_win8_root8003180.py` は fold10（seventeenth）機械の完全移行で、
(a) チェーン全段の frontier を worklist から再計算し（6,259/495,507 → … → 6,206/491,497・parent incidence 11,810・residual 72 まで全段 gate）、
(b) fold10 正本を本環境で再実行して SHA-256 `bed7d331…` と byte-identical であることを事前確認した上で、
(c) K1096 18 gate・証明書本文（byte 数 1,251,923・行数 34,529・sorted-unique・header）・root 幾何（8石・quadruples 0・D4 正準・合法手 53 の独立再導出）を再検証し、
(d) K1097 refsolve 27 gate・win16 intrinsic footprint（root 8003180: intrinsic == claimed == 4 行・49 行 exactly-once partition）・residual23 と win16 主張の不交差（残余23行掃引計画に影響しないこと）を機械確認し、
(e) 被覆幾何を「8 D4像×C(8,2) 2石除去 224 操作」と「root の C(8,6)=28 部分集合直列挙」の 2 方法で独立計算して canonical 行集合が完全一致（refsolve coverage_of82 と同一規約・D4 同変性）する様に閉じた計算で再導出した。

## 結果

- **receipt は open 5 行を閉じた**。K1097 主張 4 行
  `00000000000000003800000008001080`・`…8001100`・`…8002080`・`…8002100`（いずれも c2 需要行・5親 target 内）に加え、
  **target 外・worklist 上の open 行 `0000000000000000380000000800000c`**（cost 83・c2・同じ root の C(8,6) 部分集合幾何に内在）を併閉した。
  closed edge cost 387。主張 4 行は再導出結果と完全一致（g07 gate）。
- 5親112行 target: 40 → 44 行・残余 72 → 68 行。
- frontier: 6,206/491,497 → 6,201/491,110・solved S6 1,642 → 1,647・parent 行 incidence 11,810 → 11,803（影響 3 parent・完全閉鎖 0）。
- s6_needed_by_open_classes 4,509 → 4,504・cost_needed_by_open_classes 357,583 → 357,196。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 5（本 receipt で閉鎖）・closed-before-this-receipt 1（`…8003000`）・not-in-worklist 22。
- 出力正本（SHA-256 `d7bf2cd53d99d836418678abd172f4d5890d70bf8a90633b1e434b784bf7e50e`）は同一 cwd 2 回 + 別 cwd・別プロセス・独立 W 複写 1 回の 3 実行で byte-identical。

K1097 の残余23行掃引計画（第5ラウンド・並走宣言済み）は不変。K1103 の 149 根二手応答被覆計画の item 化・
残り 15 WIN8 候補の証明書抽出は本項の対象外で未着手のまま。

## 解釈上の制限（不変）

- WIN8-D10 はこの 8 石 root のゲーム木のみを証明する。receipt fold は frontier の閉鎖簿記であり、閉じた行や target のゲーム理論的値を主張しない。
- REFUTED-D10 は LOSS 証明ではない。pn/dn・nodes・solved 数を勝敗として読まない。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
