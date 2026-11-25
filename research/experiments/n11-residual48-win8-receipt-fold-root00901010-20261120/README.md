# n11-residual48-win8-receipt-fold-root00901010-20261120

fold18（第25 receipt・8番目の WIN8 receipt fold）。本レーンが抽出・三重検証・出版した K1120 の WIN8-D10 証明書
（root `00000000000000801202000000901010`・石 [4,12,20,23,49,57,60,71]・証明書 SHA-256 `d6745edbc77a53bbef66e807fd18e69c039e3007345af906452af11d3206cbe1`・
13,422 行 484,892 bytes・19 gate 正本 `n11-residual48-win8-cert-extract-root00901010-20261120`・
監査正本 SHA-256 `ea6f1945c5a8ff359b93336a0a5d4e29035928447503e2bf2f0d13277174b516`・
K1095 掃引由来の両 AND 順序 uncapped probes 240,848/198,622・mobility 45・主張 3 行・K1097 win16 footprint intrinsic == claimed == 3 行）を、
五親 S6 frontier receipt チェーン（… fold15 → fold16 → fold17）に fold する。
単一オーナー宣言: `research/log/2026-11-20-n11-fold18-win8-root00901010-single-owner-note.md`（commit `b5e1d5f6`・先行出版・fold17 出版後の residual-48 baseline）。

## 目的

1. root 00901010 の S6 被覆行（K1095 主張 == K1120 g07 == K1097 win16 intrinsic footprint の主張 3 行）を frontier から閉じ、5親 target 64/112 → 67/112・残余 48 → 45 行へ進める。
2. K1120 証明書が被覆しうる open 行のうち target 外の行（worklist 上・5親112行の外）も機械判定で自動的に閉じ、余剰として記録する。
3. 被覆幾何を 2 方法（8 D4像×C(8,2) 2石除去 224 操作、root の C(8,6)=28 部分集合の直列挙）で独立計算し、両者の canonical 行集合の一致（D4 同変性）を gate する。refsolve `coverage_of82` と同一規約。
4. fold17（`fold_win8_root22081000.py`・出版済み）を本実行環境で隔離 W 複写（FOLD17_W env）の下で再実行し、出版正本（SHA-256 `1175244d…`）と byte-identical であることを gate してから接続する。fold16→fold15→…→fold11 の再帰 rerun も含めて 8 機連鎖 rerun。

## 入力（fail-closed pin）

チェーン入力は fold17 と同一の 12 blob SHA-1 pin + 28 SHA-256 pin
（worklist / ledger / globalFold / previousCostFold / firstFoldTarball / census / audit / secondThirdFold / fold4 / fold56 / fold912 / fold_fourth_fifth_sixth 正本 / sv17 正本 / sv17 証明書 / fold10 正本 / K1096 正本 / K1096 証明書 / K1097 正本 / fold11 正本 / K1106 正本 / K1106 証明書 / fold12 正本 / K1108 正本 / K1108 証明書 / fold13 正本 / K1109 正本 / K1109 証明書 / fold14 正本 / K1114 正本 / K1114 証明書 / fold15 正本 / K1113 正本 / K1113 証明書 / fold16 正本 / K1117 正本 / K1117 証明書）。追加入力の SHA-256 pin:

- fold17 正本 `n11-residual51-win8-receipt-fold-root22081000-20261120/output/win8-root22081000-receipt-fold-20261120.json`（`1175244d…`・本環境で fold17 機械を隔離 W 複写の下で再実行し byte-identical を gate で確認）
- fold17 機械 `n11-residual51-win8-receipt-fold-root22081000-20261120/scripts/fold_win8_root22081000.py`（rerun gate の実行対象）
- K1120 監査正本 `n11-residual48-win8-cert-extract-root00901010-20261120/output/win8-cert-extract-verification-20261120.json`（`ea6f1945…`・19 gate 再検証・g01 K1095 正本 SHA pin 335eca5e…・g07 主張 3 行〔`g07_k1095_root_claimed_coverage_3rows`・`== 3` 定数による fail-closed〕・g05 root mobility 45・g06 uncapped probes 240,848/198,622 と terminal 石数範囲 [14,18]・g13 nodes 631,539/524,342・g16 第三方法 miss 0/extra 0/failure null・g19 footprint 照合を含む）
- K1120 証明書本体 `n11-residual48-win8-cert-extract-root00901010-20261120/certs/win8-root-00000000000000801202000000901010-20261120.n11`（`d6745edb…`・header/root/行数 13,422/sorted-unique/byte 数 484,892 全検証）

合計 43 input pins（12 blob SHA-1 + 31 SHA-256）。

## 機械

`scripts/fold_win8_root00901010.py`（fold17 機械の移行型・純 Python・乱数・時刻なし・1,000 行・約 186 秒/実行）。主要 gate:

- チェーン段階別 frontier 再計算 6,259/495,507 → … → fold16 chaining（6,168/488,575・residual 51）→ **fold17 chaining: 被覆 7 行の open 性・記録 cost 照合・frontier_after 出版値（6,161/488,094・solved 1,687・incidence 11,729・s6_needed 4,469・cost_needed 354,542）・residual48 == residual51 − fold17 主張 3 行の差分照合・closed target 64**
- fold11 機 rerun gate（FOLD11_W）・fold12〜16 機 rerun gate（隔離 W 複写）・**fold17 機 byte-identical rerun gate（subprocess・隔離 W 複写 FOLD17_W）**: 出力 SHA-256 が出版正本（`1175244d…`）と一致しなければ fail-close。fold17→fold16→…→fold11 の再帰 rerun もこの中で走る（8 機連鎖 rerun）。
- K1120 19 gate 全再検証（g01 K1095 master SHA pin・g07 3 行定数 gate・g05 mobility 45・g06 uncapped probes 240,848/198,622〔K1095 出版値〕と terminal 石数範囲 [14,18]・g13 nodes 631,539/524,342・g16 第三方法 miss 0/extra 0・g19 footprint claimed == CLAIM（3 行）・k1097 SHA pin）・証明書全文 byte 検証（484,892 bytes・13,422 行・sorted unique・合法手 45 の独立再導出・D4 正準・quadruple-free・third_method 集計〔terminal 4,336・visited 30,999・winner 20,028・loser 6,635・loser_reply_edges 28,516〕）
- K1097 27 gate・win16 footprint の root 00901010 行の intrinsic == claimed == 3 行・49 行 exactly-once partition・residual23 と win16 主張の不交差・主張 3 行が residual48 内
- WIN8 被覆幾何 2 方法一致（224 操作 vs 28 部分集合）
- 再導出 target 行 == K1120 g07 主張 3 行・chain 不整合（worklist-but-not-open）0

## 結果

- **receipt は open 4 行を閉じた**:
  K1095/K1120/K1097 主張 3 行（5親 target 内）`00000000000000003800100008002000`（cost 74・unswept・c2×2 需要行）・`00000000000801202000000101000`（cost 71・unswept・c2×2 需要行）・`00000000000801202000000900000`（cost 68・unswept・c2×2 需要行）に加え、
  **target 外・worklist 上の open 行 1 行** `00000000000801202000000100010`（cost 81・c2×2 需要行・同じ root の C(8,6) 部分集合幾何に内在）を併閉。余剰 1 行は `extra_s6_rows_not_in_target` として正確に分離記録した。
- closed edge cost 294・5親112行 target: 64 → 67 行・残余 48 → 45 行。
- frontier: 6,161/488,094 → **6,157/487,800**・solved S6 1,687 → 1,691・parent 行 incidence 11,729 → 11,721
  （影響 4 parent・いずれも class 2: 15→14〔1行〕・19→17〔2行〕・59→57〔2行〕・37→34〔3行〕・完全閉鎖 0）。
- s6_needed_by_open_classes 4,469 → 4,465・cost_needed_by_open_classes 354,542 → 354,248。
- root の 6 石部分幾何 28 canonical 行の分類: open-frontier 4（本 receipt で閉鎖）・not-in-worklist 23・closed-before-this-receipt 1（`00000000000000003800000008003000`・K1096/fold11 で閉鎖済み）。
- win16 候補は 9 → 8 根（主張 25 → 22 行）。K1097 の残余23行掃引計画は不変（residual23 と全 win16 主張の不交差を機械再確認）。

## 再現

```
python3 scripts/fold_win8_root00901010.py   # env FOLD18_W で W ルートを上書き
```

出力 `output/win8-root00901010-receipt-fold-20261120.json`（SHA-256 `18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026`・同一 cwd 2 回 + 別 W 複写・別プロセス・別 HOME 1 回の 3 実行で byte-identical・3 実行とも GATE FAILED 0）。

## 生成と教訓の注記

機械は build_fold18.py 変換スクリプト（全 38 置換が出現回数 assert 1 で機械検証）で fold17 機から生成した。
fold17 機からの転写で 2 件の差し替え漏れ・打ち間違いが発生したが、いずれも fail-closed 設計で捕捉された:
(1) g01 の K1095 master SHA リテラルの 1 文字打ち間違い（`…b78991823…`→正 `…b78791823…`）は初回実行の `k1120 k1095 master sha pin` gate が即座に捕捉（K1120 抽出監査の教訓どおり SHA定数は正本値との照合でしか入力しない運用が確定した）。
(2) frontier_after 計算 4 行の `open51`→`open48` 参照漏れは最初の実行結果の数値照査（6,161−4=6,157 であるべき箇所に fold16 値 6,168 が現れる）で発見・機械修正のうえ 3 実行をやり直した（出版正本は修正後のみ）。

## 解釈上の制限

fold は receipt チェーン上の行の閉鎖簿計であり、閉じた行のゲーム理論的値を主張しない。
WIN8-D10 は root のゲーム木のみを証明する。REFUTED-D10 は LOSS 証明ではなく、node 数・solved 数を勝敗として読まない。
**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
