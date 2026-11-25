# anchored-window-sat-frontiers-20261115

IN FLIGHT (claim) — 高速レーン。**anchored window-SAT**(既知witnessの凍結prefix付き
def-mode SAT)という新しい条件付けを導入し、3つの未決着前線
**(8,9) 8x29**(本レーンの主対象・他レーンの claim に含まれない)、
**(4,5) 4x21**、**(5,5) 5x24** に適用した。
SAT なら witness を js+py 2系統検証して下界を更新し、UNSAT は
「その凍結prefixを持つ witness は存在しない」という条件付き局所閉包として
honest に記録する。不在主張とはしない。

## 前線の所在と非重複方針

- (8,9) 8x29: `eight-row-strip-classification-20261115` はcensus構造のみで
  掃引をclaimしていない。本レーンの主対象。
- (4,5) 4x21: `four-six-row-q4-q5-band-extension-20261115` が
  「kissat def-mode / rowY 分割 / 構成的列延伸で掃引する」を IN FLIGHT 宣言済み。
- (5,5) 5x24: 同上に加え `five-row-q5-m24-class-split-20261115` が
  19 canonical class-split での掃引を IN FLIGHT 宣言(main fbc533bf 時点)。
- これら前線について本実験は**window-scan(凍結prefix条件付き局所閉包)のみ**を
  行い、全幅SAT探索・witness 探し・class-split そのもの・CSV の M 範囲変更は
  行わない。前線の決着は上記レーンに委ね、本レーンの結果は
  補助情報(局所閉包)として提供する。

## 手法

- 生成器: `sat2.js` encodeCore(安全: 全census曲線 ≤ q−1石をsequential counterで
  上限q−1...正確には「≥q石の禁止」+ 極大: 空セルは通る曲線のいずれかが
  ≥ q−1石 + 欠損: ある行 ≤ q−2石、のdef-mode)。依存 `sat.js`(all-triples census)。
  (8,9) m=29 のみ `genfast.js` fastCensus を使用(w8q9 で q=w+1、
  pigeonhole により half-integer center census が完全; m=9..40 の全32幅で
  公開値 `q9-sweep-m9-40.json` と完全一致を前段で確認済み)。
- window 条件付け: anchor witness(既知の m′<m witness)を列オフセット off で
  盤に置き、freeCols 以外の列の全セル(石・空の別)をunit節で凍結。
  残り列(1..10列)を自由にして fastsat.js(純JS CDCL)で解く。
- SAT: model → cell復号 → `sat.js` verifyConfig(census-free 全3点組列挙による
  安全+極大の独立検証) + `verify_witness.py`(Python Fraction・幾何独立)の
  2系統検証。両方okで初めて witness として記録。
- UNSAT: 「この凍結prefixを持つ m の witness は存在しない」の条件付き結果。
  事前に vacuity check(凍結部分のみでの安全違反、空セルの到達可能最大石数
  < q−1)を行い、自明に不可能な場合は VACUOUS として区別
  (今回の全实例は non-vacuous)。
- 前回の(8,9)作業から継承: m=27/28 witness の空列append(右・左)と1手surgeryは
  全失敗。診断: m=29 で右端セル (28,3) を通るcensus曲線はわずか5本
  (円4本・石数 {1,1,1,3} + 行3 の7石)。blocking circle(ちょうど8石)への
  到達には5石以上の大規模な再構成が必要で、1-2手surgeryでは構造的に不可能。

## 較正

- **正制御 3点全PASS**(`output/controls.jsonl`):
  - (4,5) w4x20 anchor・freeCols=[19] → SAT 64 conflicts、既知 w20 witness を
    bit再発見、js+py 2系統検証ok。
  - (5,5) w5x23 anchor・freeCols=[22] → SAT 94 conflicts、同様にok。
  - (4,5) w4x20 anchor を 4x21 盤に置き freeCols=[19,20] → UNSAT 61 conflicts
    (下記 m=21 scan と整合)。
- **再実行再現**: repo 収録版 scripts での全window記録は conflicts が
  bit-exact に再現(sec は wall-clock で僅差)。TIMEOUT 記録の conflicts は
  wall-clock 依存の参考値。
- **honest negative**: 純JS CDCL fastsat では (4,5) m=20 の既知SATクラス
  (class-split r=0/k=3・r=3/k=3)すら 60s で 42-51k conflicts に留まり SAT 未到達
  (kissat は 600k conflicts/36s で解)。全幅class-split掃引はこの環境
  (kissat無し)の外。window条件付けの強さ(< 200 conflicts/实例)との対比として記録。

## 結果(2026-11-15)

1. **(8,9) 8x29: 8 window 全UNSAT・全non-vacuous**(`output/w8q9-m29-windows.jsonl`,
   vacuity `output/w8q9-m29-vacuity.jsonl`)。w28 anchor (m=28 rowY=3 witness)、
   off∈{0,−1,+1}、free 1..8列。
   - `w28_o0_f27`: 8x29 witness で w28 の列0..27 をそのまま持つものは不存在
     (col 28 自由でも)。純粋な「+1列append + col28内の任意配置」も含む。
   - `w28_om1_f20`: w28 を1列左シフトした場合の列0..19(シフト後27列中)を
     持つ witness は不存在(残り8列自由)。
   - `w28_o0_f23`: w28 の列0..23 を持つ witness は不存在(残り5列自由)。
   - いずれも ~130-160 conflicts で解決。witness 構造診断
     (`output/w8q9-witness-structure.txt`): w26/27/28 witness は18-20個の
     8石円で欠損行の空セルをほぼ一意(1セル1円)に被覆。
   - **8x29 の決着(SAT/UNSAT)は未解決のまま。** frontier 8x29。
2. **(4,5) 4x21: 75 window 全UNSAT**(`output/w4q5-m21-windows.jsonl`)。
   anchors w16..w20(+V/H鏡像)、off∈{−2..+1}、free 1..10列、両側window含む。
   - 最強: `w20_om1_f11`(w20 左1シフト・凍結11列・自由10列=40セル)、
     `w20_o0_f13`(w20 の列0..12 の13列を凍結・自由8列)、
     `w19_om2_f13`(w19 左2シフト・凍結13列)など。
   - 既知 witness との prefix 一致は高々12列程度 → 4x21 witness が存在するとしても
     既知盆地からは大きく離れている(または不存在)。
3. **(5,5) 5x24: 60 window 全UNSAT**(`output/w5q5-m24-windows.jsonl`)。
   anchors w22/w23(+V鏡像)、off∈{0,−1,+1}、free 1..6列。
   - 最強: `a23_o0_f18`(w23 の列0..17 の18列を凍結・残り6列自由)など。
   - 既知 witness との prefix 一致は高々17列程度。

いずれも M の下界・上界は不変(CSV は更新しない)。

## 制限

- window UNSAT は条件付き局所閉包であり、幅全体の witness 不存在とは異なる。
- fastsat TIMEOUT は cap 到達であり不在を意味しない。
- (4,5)/(5,5) の window scan は `four-six-row-q4-q5-band-extension-20261115`
  の掃引対象前線への補助情報。同レーンの SAT 結果と独立に成立する。

## 次の一手(本レーン継続分)

- (8,9) 8x29: SA witness search(K0811系 `sa_machine_incremental.js` の q=9 移植)、
  w27/w26 anchor の window(def-mode base)、鏡像anchor × 両側window の拡張。

## 依存・再現

- `scripts/`: `sat.js`(md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c)、`sat2.js`
  (282ae832efa0080127c6c153e65e1c3c)、`genfast.js`(c5e6b5fe9c22f1bf80f34d2a64009363)、
  `fastsat.js`(05a3d7d8fa8b58903fa3b955e6dd1a4c)、`verify_witness.py`
  (0530d166572987988a01ec40dee12d4c)— いずれも
  `seven-row-q7-witness-search-20261114/scripts/` と同一bytes。
  新規: `window2.js`(汎用window-SAT)、`classsplit.js`((r,k)級分解)、
  `window89.js`/`vacuous89.js`/`extend89.js`/`diag89.js`/`struct89.js`
  ((8,9)専用)。
- 入力: `output/anchors/`(出典は各実験dir・`ANCHORS.md` 参照)、
  `output/jobs-*.json`(实例定義)。
- 出力: `output/*.jsonl`(1实例1行)、`output/w8q9-witness-structure.txt`、
  `output/w8q9-m29-extension-diagnosis.txt`(w27/w28 anchor のappend失敗診断)。
  CNF・model は中間生成物として収録しない(jobs + genfast/sat2 から再生成可能)。
