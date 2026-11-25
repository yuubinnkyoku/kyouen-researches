# Three-row q=4 enumeration closure（M_{3,4} レーン・2026-11-21・列挙閉包）

単一オーナー宣言: `research/log/2026-11-21-three-row-q4-enumeration-single-owner-note.md`
（2026-11-21T07:50Z・宣言時 HEAD `a8e4b0a6`）。
先行する SAT レーン（[three-row-q4-frontier-20261121](../three-row-q4-frontier-20261121/README.md)・
単一オーナー宣言 72fdd106）が行和63分割 + pinned kissat で確立した
witness band m=4..23 と P(24) に対し、**SAT 符号化に依存しない列挙閉包
（63プロファイル完全分割）**で m=24..27 を掃引した。
正本の知識項目は [K1183](../../knowledge/items/K1183-three-row-q4-witness-band.md)。

用語は K1183 と同一: P(m) ⟺「3×m の全極大安全配置がちょうど (q−1)·3 = 9 石」、
M_{3,4} = least m0 such that P(m) for all m ≥ m0。

## 主張（有限機械列挙の正確な範囲）

1. **63プロファイル完全分割による def-mode 列挙閉包**: 安全配置では水平線
   （禁止曲線）のため各前行の石数 ≤ 3。石数が 9 未満の極大配置は行プロファイル
   (r0,r1,r2) ∈ {0..3}³ ∖ {(3,3,3)}（63通り・min ≤ 2）のいずれかを持つ。
   63プロファイルを次の3類に exactly-once に分割する:

   | 類 | プロファイル数 | 定義 | 機械処理 |
   |---|---|---|---|
   | family | 9 | 2行が満杯・残る1行が a ∈ {0,1,2} 石（(3,3,a) の3行位置×3） | `wsearch34.js` 構造完全探索 |
   | fast | 13 | 1行のみ満杯で他の2行が {1,2} 石（(3,a,b) の12置換）+ (2,2,2) | `dx34.js fast` circle-class 列挙 |
   | lemma | 41 | 残り（すべて石数和 k ≤ 5） | crossing-supply 補題の算術キル |

2. **掃引結果（本セッション・fresh run・第二実行環境）**:
   - family: m=24,25,26,27 で Y ∈ {0,1,2} 全掃引（A集合 = C(m,3) 全域・
     `ia:[0,nSub]`）すべて **0 witness**（`output/family_sweep_23_27.jsonl`・
     F=full 2行の O0/U0/W(s)/P22/P11/ON/CX 円表の構造還元に基づく完全探索・
     消滅は (3,a,3) family 全域）。
   - fast: m=24,25,26,27 で13プロファイルすべて **count 0**
     （`output/dx_sweep_24_27.jsonl`・52/52）。
   - lemma: **m ≥ 22 で41プロファイルすべて算術キル**
     （`output/closure_check_13_27.jsonl`・補題は m について単調）。
   - **m ≥ 22 では def-mode 探索空間は family 9 + fast 13 の22プロファイル
     に簡約**される（それ以外は算術で消える）。

3. **結論**: 3×m・q=4 の def-mode（行欠損かつ極大な安全配置）は
   **m = 24, 25, 26, 27 のすべてで存在しない**（P(24), P(25), P(26), P(27)）。
   m=24 は先行の SAT 分割証明と**独立な第二方法で一致**（P(24) の二重裏付け）。
   m=25, 26, 27 は**本レーンの新規確定**。
   witness band は m=4..23 で終端（SAT レーン出版のまま・m=23 family witness
   は本レーンの構造探索でも再発見・下記対照）。
   **従って witness-free 幅は {24, 25, 26, 27}。**
   **M_{3,4} ∈ [24, 69] は不変**（下界 24 は witness band 23 終端由来・
   上界 69 は K0024 十分長さの引用。P の幅単調性は未証明であり、P(24..27) は
   M=24 の十分条件の一部でしかない）。**m ≥ 28 は未掃引で一切主張しない。**

4. **列挙系の構造観察**（`output/selftest/`・`output/dx_sweep_13_23.jsonl` の
   有限データ）: 非family プロファイルの観測上の生息幅は m ≤ 12 まで
   （m=10: (3,2,2)系 5種・m=11: 3種・m=12: (2,2,3)/(3,2,2) 各4個のみ）、
   **fast 13プロファイルは m=13..27 の全15幅で 0**（13..23 は通常掃引・
   24..27 は主張掃引・計 195/195）。すなわち m ≥ 13 の def-mode witness は
   (3,3,a) family 型のみ（m ≥ 22 では補題によりこれが機械保証付きで正当化される）。

## crossing-supply 補題（lemma 41プロファイルの算術キル）

def プロファイルで石数和 k ≤ 5 のとき、不足行（石数 ≤ 2 の行・nDef 個）の
空点はすべて極大性のために石数 ≥ q−1 = 3 の曲線上になければならない。

- 不足行の行直線は石数 ≤ 2 で block 不可。
- 非水平な直線は3行板の各行と1点で交わるため、不足行の空点を通る直線の
  石数は ≤ 2 で block 不可（crossing 補題）。
- よって block できるのは3石円のみ。安全配置の円は石数 ≤ 3 で、ブロック円は
  ちょうど3石。3点は円を高々1つ決定するのでブロック円の個数は ≤ C(k,3)。
- 円と水平行の格子点は ≤ 2 個なので、1円あたり不足行の空点を ≤ 2 個しか
  block できない。
- 需要は D(m) = Σ_{不足行} (m − rᵢ)、供給上界は 2·nDef·C(k,3)。
  **D(m) > 2·nDef·C(k,3) なら当該プロファイルの def-極大安全配置は存在しない。**

閾値（`output/closure_check_13_27.jsonl`）: m=21 では (3,2,0)型・(0,2,3)型・
(2,2,1)型など 9 プロファイルが D = supply で残るが（killed 32/41）、
**m=22 で41/41 すべてがキル**（(3,2,0)型: D=2m−2 > 40、(3,1,1)型: D=2m−2 > 40、
(2,2,1)型: D=3m−5 > 60 など・需要は m について線形増加）。
`closure_check.py validate` は補題キルが m=4..12 の全数列挙（dx34 direct・
brute 基準照合済み）と矛盾しないことを検査（補題が存在を主張する幅 0 検出・
反例 0）。

## 検証チェーン（全機械・`output/crossval_summary.json` overall PASS）

1. **dx34 direct（ground truth engine）≡ brute**: m=4..8 の全63プロファイル
   で `brute_3x{4..8}_4.json`（枝刈り全数列挙・frontier レーン出版の同一 byte・
   md5 `e21acd4c`…/`874abe7a`… 参照）の per-profile 計数・def 総数
   （182/674/1724/4607/11542）が完全一致。
2. **dx34 fast ≡ direct**: m=4..12 の selftest で対応13プロファイルすべて
   fastMismatch = 0（`output/selftest/selftest_{4..12}.json`）。
3. **wsearch34 ≡ brute family**: m=4..8 × Y ∈ {0,1,2} × a ∈ {0,1,2} の
   15実行すべてで per-(Y,a) 計数が brute の family プロファイル計数と完全一致
   （`output/wsearch_crossval/`）。
4. **m=23 陽性対照**: family witness は Y=0: 2件・Y=1: 4件・Y=2: 2件（V鏡像で
   Y=0 と Y=2 が同数）。各 witness は2系統検証
   （sat.js `verifyConfig` + `witness_check.py` 整数行列式幾何）で PASS。
   **Y=0 第2 witness は先行 SAT レーンの外側行 witness
   `wit_3x23_outer_4`（5:0,21:0,9:1,12:1,15:1,10:2,12:2,13:2）と石集合として
   byte-exact**（独立方法による witness 再発見・`output/m23_witness_check.txt`）。
5. **閉包台帳**: `closure_check.py check` が63プロファイルの類別と補題キルを
   m=13..27 で機械検査し、exactly-once 被覆（9+13+41 = 63）を確認。
6. **統合**: `crossval_summary.py` が 1..5 を再実行して
   `output/crossval_summary.json`（overall PASS）を出力。

## 器材 pin（`output/md5s.txt`）

sat.js `0cc6021a4e523a0d7f4d5ea0f5f5d40c`（frontier SAT レーン正本と同一 byte・
wsearch34 の依存）・wsearch34.js `526cf1c3b247726131746072730467f2`・
dx34.js `b02235a9a40593a324dffb17fcf51af2`・verify_witness.js
`06bead66001f0417f5ad715029b55089`・witness_check.py
`e48f9bf2176e72138bebb4f7a677b5ba`・closure_check.py
`cafc3978649dd1afbddd8cd9339adc2a`・crossval_summary.py
`8ae34f3da0b2675da02a1155570c4aba`。

## 再現手順（Node.js 18+・Python 3 標準ライブラリのみ・外部 solver 不要）

```sh
cd research/experiments/three-row-q4-enumeration-20261121
# 検証チェーン
for m in 4 5 6 7 8 9 10 11 12; do node scripts/dx34.js selftest $m > output/selftest/selftest_$m.json; done
for m in 4 5 6 7 8; do for Y in 0 1 2; do node scripts/wsearch34.js $m $Y --quiet > output/wsearch_crossval/ws_${m}_${Y}.json; done; done
# 陽性対照（witness 抽出 + 2系統検証）
node scripts/wsearch34.js 23 0 --examples=3
node scripts/verify_witness.js 3 23 4 '[[9,1],[12,1],[15,1],[10,2],[12,2],[13,2],[5,0],[21,0]]'
python3 scripts/witness_check.py 3 23 4 '[[9,1],[12,1],[15,1],[10,2],[12,2],[13,2],[5,0],[21,0]]'
# core sweeps（family: 実行時間 ~ (m/24)^3・m=27 で約110 s/Y）
for m in 24 25 26 27; do for Y in 0 1 2; do node scripts/wsearch34.js $m $Y --quiet; done; done
for m in 24 25 26 27; do for p in 3,2,2 2,3,2 2,2,3 3,2,1 3,1,2 2,3,1 1,3,2 2,1,3 1,2,3 3,1,1 1,3,1 1,1,3 2,2,2; do node scripts/dx34.js fast $m $p; done; done
# 閉包台帳 + 統合
python3 scripts/closure_check.py check 24 25 26 27
python3 scripts/closure_check.py validate
python3 scripts/crossval_summary.py   # crossval_summary.json（overall PASS）
```

## コスト観察と次の実行可能課題

- family 掃引は J 単位で全 C(m,3)² base-pair 設定を前段枝刈り（P22/P11 安全
  表）で走査し、実行時間は約 (m/24)³（m=24: 約45 s/Y・m=27: 約110 s/Y・
  `family_sweep_23_27.jsonl` の ms 値参照）。`--ia/--ib` で A 側 chunk 分割可能。
- fast 掃引は軽量（m=27 で (3,2,2) 約7 s・全体45 s/幅）。補題は m ≥ 22 で
  自動。**m=28 以降の1幅は family 3掃引 + fast 13掃引 + 補題で完了**
  （m=28 family は推定150 s/Y、m=30 は chunk 推奨）。
- 前線の近接目標: witness-free 帯を 28..68 に延伸できれば M_{3,4} = 24 が
  確定する（69 = K0024 の全称側と接続）。kissat 分割（frontier レーン task (a)）
  は m=25 を含む今回の範囲を独立確認する位置づけに変わる。

## 解釈規約

- 本レーンの主張は**有限完全列挙**（family/fast の構造還元は巡回円表の数学的
  記述に基づき、m=4..8 で brute 全数と計数一致で妥当性確認・m=23 で出版
  witness の byte-exact 再発見）と**算術補題**（証明つき・m=4..12 の全数列挙と
  の整合検査）による。無界な全称命題（一般 m の非存在）は主張しない。
- m=23 の family witness 群（Y=1 の (3,2,3) 型含む）は witness band のみの
  主張であり、m=23 の def-mode プロファイル全域の分類ではない。
- INDET プローブ・cap 下 conflicts 等の SAT 側参考値は本レーンに無関係。
- 標準 11×11 空盤等には無関係・UNKNOWN のまま。

## m≥28 掃引 ext28plus（2026-11-21 08:38Z 追設・witness-free 幅 {24..31}）

拡張の単一オーナー宣言: `research/log/2026-11-21-three-row-q4-enumeration-m28-single-owner-note.md`
（2026-11-21T08:38Z・宣言時 HEAD `f57060f8`・出版 commit `e9c3cd86`）。
part1-10 の同一 pin scripts 7 点（md5 変更なし・`output/md5s.txt` 参照）で
m=28..31 を掃引した。既存出版 output は 1 byte も変更しておらず、本拡張の
成果物は `output/ext28plus/` 配下の新規ファイルのみ。

### 掃引結果（全機械・raw は chunk 出力のまま出版）

- **family（wsearch34.js・(3,3,a) 9プロファイル相当の (m,Y) 全掃引）**:
  m=28（ia [0,3276) 全域・139-148s/Y）・m=29（[0,3654) 全域・191-202s/Y）は
  Y∈{0,1,2} 各1実行、m=30 は Y∈{0,1,2} × 2 chunk（[0,2030)/[2030,4060)）、
  m=31 は Y∈{0,1,2} × 3 chunk（[0,1499)/[1499,2998)/[2998,4495)）。
  集計 `family_sweep_28_31.jsonl`（(m,Y) 行: configs/safe/deep/a0/a1/a2 和・
  ia 区間リスト）で **全 (m,Y) で a0=a1=a2=0**。
- **fast（dx34.js・13プロファイル）**: m=28..31 × 13 = 52行全 **count 0**
  （`dx_sweep_28_31.jsonl`）。
- **lemma（crossing-supply 補題）**: m=28..31 で **41/41 算術キル**
  （`closure_check_28_31.jsonl`・`closure_check.py check`・補題は m≥22 単調）。
- **陽性対照（環境較正）**: 掃引開始前に pinned wsearch34.js で m=23 Y=0 を
  再実行し、出版済み witness 2件（a=2）・configs 3136441・safe 2352504 を
  byte 単位の同一出力で再発見（`control_m23_Y0.txt`・part4a 出版値と一致）。

### 集計器と検証（output/ext28plus/agg_chunks.py・stdlib のみ）

`agg_chunks.py` が次を全検査し `crossval_summary_ext28_31.json` を出力:

1. **分割完全性**: 各 (m,Y) の chunk ia 区間が [0, C(m,3)) を重複なく
   exactly-once に分割し、configs の和が C(m,3)² に一致
   （m=29: 13,351,716・m=30: 16,483,600・m=31: 20,205,025）。
2. family 12掃引の a 計数がすべて 0。
3. fast 52行すべて count 0。
4. 閉包台帳 m=28..31 の verdict が closed（41/41）。
5. m=23 対照が出版行と完全一致。

### 結論と範囲

- **P(28), P(29), P(30), P(31) を確定し witness-free 幅は {24,...,31}。**
  m=25..27 に続くこの 4 幅も SAT 非依存の列挙閉包単独の確定。
- **m ≥ 32 は未掃引であり一切主張しない。** pinned wsearch34.js の冒頭
  `require(4 <= m <= 31)` は 31-bit bitmask（`1 << x` が符号付き 32bit を
  想定）由来の上限で、m≥32 は治具拡張（BigInt / 2-word mask 化・交差検証は
  m=4..8 brute と m=23..31 出版掃引の再現で行う設計）が別途必要。
- **M_{3,4} ∈ [24,69] は不変**（下界 24 は witness band 23 終端由来・上界 69 は
  K0024 引用・P の幅単調性は未証明）。残る不確定幅は 32..68 の 37 幅。
- fast 13 プロファイルは m=13..31 の全幅で 0（掃引累計 247/247）。
  したがって観測上 m≥13 の def-mode witness は (3,3,a) family 型のみ
  （m≥22 では補題がこれを機械保証付きで正当化）。

### 再現（scripts は既存 pin のまま）

```sh
cd research/experiments/three-row-q4-enumeration-20261121
# family（1実行/Y は m=28,29・chunk は m=30,31）
for Y in 0 1 2; do node scripts/wsearch34.js 28 $Y --quiet; done
for Y in 0 1 2; do node scripts/wsearch34.js 29 $Y --quiet; done
for Y in 0 1 2; do node scripts/wsearch34.js 30 $Y --ia=0 --ib=2030; node scripts/wsearch34.js 30 $Y --ia=2030 --ib=4060; done
for Y in 0 1 2; do node scripts/wsearch34.js 31 $Y --ia=0 --ib=1499; node scripts/wsearch34.js 31 $Y --ia=1499 --ib=2998; node scripts/wsearch34.js 31 $Y --ia=2998 --ib=4495; done
# fast
for m in 28 29 30 31; do for p in 3,2,2 2,3,2 2,2,3 3,2,1 3,1,2 2,3,1 1,3,2 2,1,3 1,2,3 3,1,1 1,3,1 1,1,3 2,2,2; do node scripts/dx34.js fast $m $p; done; done
# 閉包台帳 + 集計検証
python3 scripts/closure_check.py check 28 29 30 31
python3 output/ext28plus/agg_chunks.py
```

run 名と wall time（`--ia` は wsearch34.js の A 側分割オプション）:
m=28 約139-148s/Y・m=29 約191-202s/Y・m=30 chunk 合計 約254-372s/Y・
m=31 chunk 合計 約333-439s/Y（2核環境・単一 foreground run で計測）。

### 運用教訓（本拡張セッション）

- heavy run（100s 超）は 1 bash call に 1 foreground process が安定。
  本環境（2 core）で同 call 内の背景並走は出力を残さず消える
  （1度喪失し、同一 chunk を foreground でやり直して補填）。
  call をまたいだ背景 node プロセスは次の call 開始時に殺される。
- `--ia/--ib` chunk 分割は A 側の冪等な空間分割であり、和による合成は
  集計器が区間検査込みで機械保証する（目視合成・手書き再構成は不使用）。

