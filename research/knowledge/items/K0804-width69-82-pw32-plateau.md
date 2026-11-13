---
id: K0804
title: "幅69..82の円点数の完全決定 P(w)=32（全14幅） — 32点プラトーがw=49..82に拡大・P(w)は全幅6..82で決定済み・level 17の復活点はちょうど(82,83]・2独立REST6実装による二重走査（全幅leaves=0・生残0・uniqueMasks 14/14完全一致）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(w)=32 for w=69..82（全称・等号付き・14幅一括）。帰結としてP(w)はw=6..82の全幅で決定済み（16プラトー12..21・跳躍22..25・24プラトー26..42・漸増43..48・32プラトー49..82）。level 17の復活点はちょうど(82,83]（K0785のP(83)≧34・K0791の34点最小幅83と本項のP(82)=32が両端を確定）。w=83,84は既知witness（11050円34点）によりlevel 17が死なない正制御の対象"
evidence: "数学的証明（REST6 2フェーズ機〔K0802と同一アルゴリズム〕のパラメータ化版を2独立実装で実行）。各幅w=69..82で全maximal mask（全幅3,300・K0803の有限測定66..132と整合）を完走しleaves=0・生残0。 survivors(REST6)⊇survivors(REST16)（実現可能標準形は全合同証明書を通過・w26 L12制御でS*={0,1,3,4,7,10,15,18,21,22,24,25}ちょうど1生残）によりREST6生残0はREST16でも生残0確定。level 17全滅⟹d+s≦16⟹P≦32。g0≧2形はK0797 convention B classMax（拡張法33法・全形<17・w≦84で有効）。下界: 2210円の全32点（v-span 94≦2(w−1)・w≧49で有効）。2実装: (1) width_sweep.mjs（per-chunk状態永続化・停滞検出cap拡張・出力state_w69..w82）・(2) 独立実装sweep（チャンクcapを600M..4Gに取り単一連続走査・出力dual_run_independent_sweep.json）。両者はuniqueMasks 14/14完全一致（3300,3300,3300,3300,3313,3326,3339,3353,3367,3381,3400,3419,3438,3447）・leaves/生残は全幅0で一致。ノード総数はチャンクプロトコル依存（2.4M cap連続では中止チャンクの部分mask再探索が二重計上される）ため2実装で数値は異なるが結論判定は同一。回帰制御: 独立実装はw=68で96,626,896 nodes・leaves=0・生残0をK0802の独立全幅再実行とnode数まで完全再現・w=69..72のノード総数（122,980,751/160,083,797/202,737,214/255,040,369）もstate_w69..w72と完全一致"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(w)=32 (w=69..82) は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11）+ bit-set DFS level 17 全滅（maximal mask 3,300の全走査・REST6 2フェーズ・lastDone冪等再開）× 2独立実装 + K0797 g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: 2独立実装の二重走査（全幅leaves=0・生残0・uniqueMasks 14/14一致）・回帰制御（w=68 96,626,896 nodes完全再現・w=69..72ノード総数一致）・w=26 L12制御S* 1生残・K0803とのmaximal 3,300整合
  note: "総ノードは2実装・2プロトコルで4組の値が存在する（詳細はdual_run_independent_sweep.json）。独立実装の単一連続（clean）走査値: w69 122,980,751 / w70 160,083,797 / w71 202,737,214 / w72 255,040,369 / w73 278,993,737 / w74 343,218,984 / w75 416,763,974 / w76 509,510,835 / w77 615,580,292 / w78 747,684,447 / w79 915,374,175 / w80 1,103,319,150 / w81 1,318,611,397 / w82 1,593,581,640。2.4M cap連続値は各state_wXX.json参照。成長率~1.20..1.22/w。uniqueMasksはw≧73で3300を超えて増加（小パターン|P|≦6の|T|≧17参入）するがmaximalは全幅3300のまま（K0803支配補題と整合）"
relations:
- type: depends_on
  target: K0802
  note: 完走機（REST6 2フェーズ）のパラメータ化版。32プラトーを w=68 から w=82 まで一括延長
- type: depends_on
  target: K0797
  note: g0会計のw=69..82有効性（拡張法33法・w≦84）・非標準形前提の正当化
- type: depends_on
  target: K0803
  note: maximal mask数3,300（全幅で一致・小パターンはuniqueにのみ参入）
- type: supports
  target: K0785
  note: level 17復活点を (68,83] からちょうど (82,83] に狭窄・34点最小幅83の左端を確定
artifacts:
- path: research/experiments/width69-84-sweep-20261114/scripts/width_sweep.mjs
  role: verifier
  note: パラメータ化REST6掃引機（per-chunk状態永続化・停滞検出cap拡張・w=83/84正制御対応をheaderに明記）
- path: research/experiments/width69-84-sweep-20261114/output/state_w69.json
  role: data
  note: w=69完走状態（2.4M capプロトコル・totalNodes 122,980,751・leaves=0・生残0）
- path: research/experiments/width69-84-sweep-20261114/output/state_w82.json
  role: data
  note: w=82完走状態（2.4M capプロトコル・totalNodes 1,949,902,072・capEsc 57・leaves=0・生残0）。w70..81のstate_w70..w81.jsonも同形式
- path: research/experiments/width69-84-sweep-20261114/output/dual_run_independent_sweep.json
  role: data
  note: 独立実装による二重走査記録（clean単一連続ノード総数・14幅uniqueMasks一致表・回帰制御）
- path: research/log/2026-11-14-width69-82-dual-run-integration.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(w) = 32 for w = 69..82**（幅 w の連続整数行・全 m ≥ 1・標準整数格子・14幅一括）。
   - 上界: 各幅で level 17 全滅（全 3,300 maximal mask・leaves=0・生残 0）⟹ d+s ≤ 16 ⟹ P ≤ 32。
     g0 ≥ 2 形は K0797 classMax（全形 < 17・拡張法 33 法・w ≤ 84 で有効）。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 2(w−1)・w ≥ 49 で有効）。
2. **帰結**: **P(w) は全幅 w = 6..82 で決定済み**
   （16 プラトー 12..21・跳躍 22..25・24 プラトー 26..42・漸増 43..48・**32 プラトー 49..82**）。
3. **level 17 の復活点はちょうど (82, 83]**: K0785 の P(83) ≥ 34 と
   K0791 の 34 点最小幅 83 が右端・本項の P(82)=32 が左端。

## 実行方式（REST6 2フェーズ・2独立実装の二重走査）

- 実装1（並走レーン・repo掲載）: width_sweep.mjs。
  cap 2.4M/chunk の連続チャンク（中止チャンクの部分 mask 再探索を含む計上）で
  w=69..82 を完走（state_w69..w82・全幅 done=true・leaves=0・生残 0・
  停滞時は dynCap 8 倍拡張〔capEsc 最大 57 = w=82〕）。
- 実装2（本項・独立書き下ろし）: 同一アルゴリズムの独立実装を
  cap 600M..4G で単一連続走査（clean計上・部分mask再探索なし）。
  全 14 幅で leaves=0・生残 0。
- **一致**: uniqueMasks 14/14 完全一致
  （w69..72=3300・w73=3313・w74=3326・w75=3339・w76=3353・w77=3367・
  w78=3381・w79=3400・w80=3419・w81=3438・w82=3447）・
  maximal 3,300（全幅）・leaves=0・生残 0。
  ノード総数はチャンクプロトコル依存のため両者で異なる（dual_run_independent_sweep.json）。

## 制御

- 回帰: 独立実装は w=68 で **96,626,896 nodes・leaves=0・生残 0** を
  K0802 のネイティブ独立全幅再実行と node 数まで完全再現。
- w=69..72 のノード総数は state_w69..w72 と完全一致
  （両実装とも cap 2.4M プロトコルで走査した幅）。
- w=26 L=12 制御: S*={0,1,3,4,7,10,15,18,21,22,24,25} ちょうど 1 生残（誤殺なし）。
- K0785/K0791 の witness（11050 円・34 点・最小幅 83）と整合:
  本掃引は w ≤ 82 で全滅・w=83 では生残が出ることが期待される（正制御・未実行）。

## 構造観察

- 総ノード成長率 ~1.20..1.22/w（w=68 の 96.6M → w=82 の 1.59G〔clean〕）。
  w=65..68 の成長則 ~1.35 を下回る（heavy band の局在性の影響）。
- uniqueMasks は w ≥ 73 で 3,300 を超えて単調増加（+13/+13/+13/+14/+14/+14/+19/+19/+19/+9）
  — 小パターン（|P| ≤ 6）の T(w) が |T| ≥ 17 に達して参入。
  **maximal は全幅 3,300 のまま**（K0803 の支配補題の実測による裏付け:
  参入した小パターンは全て非 maximal）。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- **w=83, 84 は本項の対象外**（K0797 会計は w ≤ 84 まで有効だが
  34 点 witness が既知のため level 17 掃引は P ≤ 32 を与えない。
  期待される正の生残は掃引機の生存検出感度の制御になる）。
- P(83) の正確な値（≥34）と M_{83,q} の確定は open のまま。
- 11×11 空盤・二石 root {49,60} は本項目と無関係に UNKNOWN のまま。
