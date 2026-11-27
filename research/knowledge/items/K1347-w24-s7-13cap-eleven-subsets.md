---
id: K1347
title: "W_24 s=7 — 極大 13-キャップはドデカッドをちょうど 1 個含み、11-部分集合は 66 個が G=2・12 個がドデカッド部分（G=0）"
kind: proposition
status: proved
topics: [grundy, geometry]
aliases:
- eleven-subsets of maximal 13-caps in the W_24 s=7 game
- 66 12 split of 13-cap 11-subsets
- each maximal 13-cap contains exactly one dodecad
relations:
- type: related
  target: K1346
  note: ドデカッド 9-/11-部分集合の G=2/G=0 層（全数検証）
- type: related
  target: K1342
  note: W_24 s=7 のサイズ別分解（サイズ 11 は G=0 30,912 / G=2 2,040,192）
- type: related
  target: K1293
  note: 極大 13-キャップ 30,912 のスペクトル
- type: related
  target: K1348
  note: ドデカッド 3 層（k=9,10,11 の G=2/1/0、全数 DP）
- type: related
  target: K1349
  note: 層マップの 11 の非ドデカッド行 {12:6, 13:1} と d11 行 {13:12} を全数で裏付け
artifacts:
- path: research/experiments/w24-s7-13cap-dodecad-structure-20261128/README.md
  role: log
  note: 全 30,912 cap の包含・分割・インシデンス全数検証と 2,040,192 全数 Grundy DP の総括
- path: research/experiments/w24-s7-13cap-dodecad-structure-20261128/output/structure_summary.json
  role: certificate
  note: 全検証の統合結果（all_pass true、恒等式 3 本を含む）
- path: research/experiments/w24-s7-13cap-dodecad-structure-20261128/scripts/gen_structure.c
  role: solver
  note: Golay 張・13-cap 全列挙・包含全数・66/12 分割（stage1）
- path: research/experiments/w24-s7-13cap-dodecad-structure-20261128/scripts/grundy_fullcheck.c
  role: solver
  note: 非ドデカッド 11-部分集合 2,040,192 個の全数 Grundy DP と拡大プロファイル（stage2、4 並列）
- path: research/experiments/w24-s7-13cap-dodecad-structure-20261128/scripts/check_golay.py
  role: verifier
  note: Python による独立再導出とクロスチェック（PASS）
- path: research/log/2026-11-28-w24-13cap-dodecad-structure.md
  role: log
  note: 全数検証の記録と「高々 1 個」の純粋証明
- path: research/log/2026-11-27-w24-13cap-split.md
  role: log
  note: 3 個の極大 13-キャップでの 66/12 分割の当初検証
scope: W_24（24 点、759 オクタッド）の s=7 ゲームにおける極大 13-キャップ 30,912 個のドデカッド包含と、11-部分集合 78 個の Grundy 分布・ドデカッド部分への分割。
evidence: 全数検証（stage1、単一プロセス 1.4 秒）で、759 オクタッドの F2 張 4,096 語の重み分布 {0:1, 8:759, 12:2,576, 16:759, 24:1} を再計算し、重み 12 語（ドデカッド）2,576 個を得た。C(24,13) 全走査による安全 13-集合（= 極大 13-cap、全 30,912 個が終端であることも全数確認）の列挙は 30,912 個。**30,912 cap すべてがドデカッドをちょうど 1 個含む**（30,912×2,576 の包含全数検査）、**各ドデカッドは 12 個の cap に含まれる**（2,576 個すべてで 12）。30,912×12 = 2,576×12×1 のインシデンス恒等式が閉じる。各 cap の 78 個の 11-部分集合は 30,912 cap すべてで **12 個が d11**（いずれも含まれた唯一のドデカッドの部分集合）+ **66 個が非 d11**。非 d11 は 30,912×66 = 2,040,192 個で重複ゼロ（ソート確認）。全数 Grundy DP（stage2、4 並列約 42 秒）で **非 d11 2,040,192 個すべてが G=2**（他の値なし、K1342 のサイズ 11 G=2 総数と一致 → 集合一致）、極大拡大プロファイルは **(極大 12-拡大 6, 13-cap 親 1) が全 2,040,192 個で一様**（拡大一意性の全数確認）。d11 側も全数で G=0・13-cap 親 12 一様。Python による独立再導出（Golay・d11・cap 安全性・サンプル照合・bin ハッシュ）も PASS。「高々 1 個」は純粋証明も成立する。Golay コードは線形で最小重み 8 なので、2 つの相異なるドデカッドが同一 13-cap に含まれると |D1∩D2| ≥ 11 → D1+D2 は重み ≤2 の非零符号語となり矛盾。
---

# 極大 13-キャップのドデカッド包含と 11-部分集合の分割（全数検証済み）

## 構造定理

- W_24 s=7 の極大 13-キャップ 30,912 個は、ドデカッド（Golay 重み 12 語、2,576 個）と
  外点 12 通りを使って **D∪{z} の形**に一意に書ける（各 cap はドデカッドをちょうど 1 個含む）。
- 極大 13-キャップの 11-部分集合 78 個は、
  **12 個がドデカッド 11-部分集合（d11、G=0）**、**66 個が非 d11（G=2）**。
- 非 d11 11-部分集合全体は 2,040,192 個で重複がなく、サイズ 11 の G=2 層と**集合一致**
  （各非 d11 11-cap は極大 13-cap をちょうど 1 個の親に持ち、極大 12-拡大を 6 個持つ）。

## 根拠

- 「高々 1 個」: 純粋証明（Golay コードの線形性と最小重み 8。evidence 参照）。
- 「ちょうど 1 個」と個数: 全数列挙（C(24,13) = 2,496,144 の直接走査 → 30,912、
  包含検査 30,912×2,576、非極大 0）。
- 66/12 分割と G 値: 全数 Grundy DP（2,040,192 個すべて G=2、d11 30,912 個すべて G=0）。
- 恒等式: 2,576×12 = 30,912（cap 数）、30,912×66 = 2,040,192（G=2 総数、K1342）、
  30,912×12 = 370,944（d11 側の 13-cap インシデンス総数）。

## 注意

- 「各ドデカッドは 12 個の 13-cap に含まれる」は純粋にも従う（符号語の交差は偶数 →
  オクタッドはドデカッドと ≤6 点で交わり、12 個の単一追加がすべて安全 13-cap）。
- s=7 でのドデカッド自身は子 12 個（すべて終端 13-cap）を持つため **G=1・非終端**
  （2,576 個全数確認）。K1348 の k=12 行の注記の訂正候補 — 詳細は
  `research/log/2026-11-28-w24-13cap-dodecad-structure.md`。
