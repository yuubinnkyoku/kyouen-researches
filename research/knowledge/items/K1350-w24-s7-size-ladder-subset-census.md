---
id: K1350
title: "W_24 s=7 のサイズラダー全層はドデカッド/極大13-cap部分集合で完全分解 — dodecad は非極大（G=1）"
kind: computation
status: computed
topics: [grundy, geometry]
aliases:
- full subset census of dodecads and maximal 13-caps in the W_24 s=7 size ladder
- dodecads are non-maximal at s=7 (G=1), correcting the K1348 k=12 row
relations:
- type: related
  target: K1342
  note: W_24 s=7 のサイズ別分解（GSIZE 原表）。全 k の (k,G) を独立の全数 DP で再計算し完全一致を確認
- type: related
  target: K1343
  note: k≤8 のパリティ則。サンプル DP（100×8 + 構造クラス各 50）で補強
- type: related
  target: K1346
  note: dodecad 9-/11-部分集合 = G2/G0 層。本項の全数 DP でクラス単一値として再確認
- type: related
  target: K1347
  note: 極大 13-cap の 11-部分集合 66/12 分割。census の d11 索引（370,944 incident）で全数再確認
- type: related
  target: K1348
  note: ドデカッド 3 層（G=2/1/0、k=9,10,11）は本項の全数 DP で再確認。k=12 行「G=0 極大・終端」は誤りで本項が修正
- type: related
  target: K1349
  note: 層マップ。個数 9 行の突合監査 OK、d11 {13:12} プロファイルを全数化、dodecad の所属クラスを「12 非極大」に修正
- type: related
  target: K1293
  note: ドデカッド同定（Golay 重み 12 語）と board_w24.txt・ゲーム規約の出自
artifacts:
- path: research/experiments/w24-s7-size-ladder-20261128/output/correspondence.json
  role: data
  note: 統合対応表と監査（all_checks_pass が true）
- path: research/experiments/w24-s7-size-ladder-20261128/output/census_raw.json
  role: data
  note: 全数 census（D_k/T_k/交差/包含多重度ヒストグラム）
- path: research/experiments/w24-s7-size-ladder-20261128/output/dpverify_raw.json
  role: data
  note: サイズ 9-13 全 6,661,168 局面の全数 Grundy とクラス別集計
- path: research/experiments/w24-s7-size-ladder-20261128/output/d11ext.json
  role: data
  note: 全 30,912 d11 の 12-cap 拡大監査（13 個すべて非極大）
- path: research/experiments/w24-s7-size-ladder-20261128/output/max13caps.txt
  role: data
  note: 極大 13-cap 30,912 個のマスク一覧
- path: research/experiments/w24-s7-size-ladder-20261128/output/dodecads.txt
  role: data
  note: ドデカッド 2,576 個のマスク一覧
- path: research/experiments/w24-s7-size-ladder-20261128/scripts/census.c
  role: solver
  note: 全数 census（Golay 張・13-cap 列挙・2^24 マスク多重度マーク）
- path: research/experiments/w24-s7-size-ladder-20261128/scripts/dpverify.c
  role: solver
  note: 全数 Grundy DP（fullcheck.c と同一規約）+ k≤8 サンプル
- path: research/experiments/w24-s7-size-ladder-20261128/scripts/d11ext.c
  role: solver
  note: d11 拡大の極大性判定
- path: research/experiments/w24-s7-size-ladder-20261128/scripts/assemble.py
  role: verifier
  note: 公式 GSIZE/SIZE 行との突合と対応表生成
- path: research/experiments/w24-s7-size-ladder-20261128/README.md
  role: log
  note: 実験の方法・結果・再現手順
- path: research/log/2026-11-28-w24-size-ladder.md
  role: log
  note: 発見順・判断・次の一手
scope: W_24（S(5,8,24)）の s=7 ゲーム（局面 = 各 octad と高々 7 点）におけるサイズ k=0..13 の全 Grundy 層と、ドデカッド（Golay 重み 12 語 2,576 個）の k-部分集合・極大 13-cap（30,912 個）の k-部分集合・極大 12-cap（1,020,096 個）の全数対応。
evidence: census.c が 2,576 dodecad と 30,912 極大 13-cap（SIZE 13 と一致、極大性スポット検査付き）の全部分集合を 2^24 マスク配列に多重度付きでマーク（包含対総和の自己チェック全 k PASS、重複排除済み）。dpverify.c が fullcheck.c と同一の memoized DP でサイズ 9-13 の全 6,661,168 局面の Grundy を厳密計算し、(k,G) ヒストグラムが公式 GSIZE 行と全 k で完全一致、クラス別の G は単一値。k≤8 はサンプル（ランダム 100×8、構造クラス各 50）がすべてパリティどおり。d11ext.c が全 30,912 d11 の 12-cap 拡大 13 個がすべて非極大と判定。dodecad の Grundy は全 2,576 個の全数 DP で G=1。
---

# W_24 s=7 のサイズラダー全層の構造対応

D_k = ドデカッド k-部分集合（相異なる、2 つの dodecad の交差 ≤ 8 点なので
k ≥ 9 は自動的に一意、k ≤ 8 はマーク配列で重複排除）、
T_k = 極大 13-cap k-部分集合（相異なる）、neither = caps − (T∪D)。
全 k で **D_k ⊆ T_k**（交差列 both = D_k）。

| k | caps | G0 | G1 | G2 | D_k | T_k | neither | 層の説明（全数 DP で確認） |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0-6 | Σ C(24,k) | 偶数サイズ全て | 奇数サイズ全て | | C(24,k) 全て | C(24,k) 全て | 0 | パリティ `G = k mod 2` |
| 7 | 346,104 | | 346,104 | | 340,032 | 346,104 | 0 | パリティ |
| 8 | 734,712 | 734,712 | | | 637,560 | 734,712 | 0 | パリティ |
| 9 | 1,295,360 | | 728,640 | 566,720 | 566,720 | 1,295,360 | 0 | G2 = D（dodecad 9-部分集合）、G1 = T\D |
| 10 | 1,870,176 | 1,700,160 | 170,016 | | 170,016 | 1,870,176 | 0 | G1 = D（dodecad 10-部分集合）、G0 = T\D |
| 11 | 2,071,104 | 30,912 | | 2,040,192 | 30,912 | 2,071,104 | 0 | G0 = D（dodecad 11-部分集合）、G2 = T\D |
| 12 | 1,393,616 | 1,020,096 | 373,520 | | 2,576 | 373,520 | 1,020,096 | G1 = T（13-cap の 12-部分集合、dodecad 2,576 を含む）、G0 = neither（極大 12-cap） |
| 13 | 30,912 | 30,912 | | | 0 | 30,912 | 0 | 終端 |

- **サイズ ≤ 11 の全キャップは極大 13-cap に含まれる**（T_k = caps、k ≤ 11;
  k ≤ 7 は全部分集合、k=8 は全 8-cap）。サイズ 12 では T_12 = 非極大 12-cap
  373,520 とちょうど一致し、neither が極大 12-cap 1,020,096 になる。
- k=9,10,11 では G 層が D と T\D にちょうど分裂し、k=12 では T（非極大）と
  neither（極大）に分裂する。k ≤ 8 はパリティ層で D/T 所属は G を分裂させない。

## dodecad は s=7 では非極大（G=1）— K1348 k=12 行・K1342 evidence の修正

- dodecad-octad 交差は {2:132, 4:495, 6:132}（最大 6）なので任意の外部点追加が
  合法（12 個の合法手、子はすべて極大 13-cap）→ mex{0} = 1。
- 全数 DP で **2,576 個の dodecad すべてが G=1**、census でも全 dodecad が
  ちょうど 12 個の極大 13-cap に含まれる。
- したがって K1348 の k=12 行「2,576, 0（極大・終端）」と K1342 evidence の
  「G=0 1,020,096 は極大 12-cap（ドデカッド 2,576 を含む）」は誤り。
  極大 12-cap 1,020,096 に dodecad は含まれず、dodecad は非極大 G=1 側。
  （K1348 の k=9,10,11 行と K1349 の個数表は本全数計算で再確認・正しい。）

## d11 → 極大 13-cap 拡大一様性（全数）

- 各極大 13-cap は 12 個の d11 を含み、各 d11 は 12 個の極大 13-cap 拡大を持つ
  （両方向 hist {12: 30,912}、incident 総数 370,944 = 30,912×12）。
- 各 d11 の 12-cap 拡大は 13 個で**すべて非極大** → 極大拡大プロファイル
  **{13:12}** が全 30,912 d11 で確定（K1349 のサンプル主張を全数化）。
- 非ドデカッド 11-cap は極大 13-cap をちょうど 1 倍持つ（t 多重度 1 が全 2,040,192）。

## k ≤ 8 の構造

- D_k = C(24,k)（全部分集合）for k ≤ 6; D_7 = 340,032（欠け 6,072 = 759×8、
  octad の 7 点集合）; D_8 = 637,560（欠け 97,152 = 759×8×16、octad の
  7 点 + 外部 1 点）。8-点集合全体は 637,560 + 97,152 + 759（octad、非局面）に完全分割。
- 13-cap 包含多重度: k ≤ 5 で一様（dodecad 側 2576/1288/616/280/120/48、
  13-cap 側 30912/16744/8736/4368/2080/936）、k=6 は 2 軌道
  （dodecad 側 {16: octad-6 21,252, 18: 113,344}）、k=7 で dodecad 側一様 6、
  k=8 で dodecad 側一様 2（D とその補 dodecad）。

## 限界

- 極大 12-cap 拡大数（K1349 の {12:180} 等の 12 側プロファイル）は本項では未検証
  （サンプル主張のまま）。
- 「サイズ ≤ 11 の全キャップは極大 13-cap に含まれる」は有限計算で、数学的証明は未取得。
- k ≤ 8 の Grundy はパリティのままであり、D/T 構造は Grundy 分解に寄与しない
  （構造的事実としての記録）。
