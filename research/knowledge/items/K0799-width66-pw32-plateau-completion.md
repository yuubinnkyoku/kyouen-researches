---
id: K0799
title: "幅66の円点数の完全決定 P(66)=32 — 32点プラトーがw=49..66に拡大・P(w)は全幅6..66で決定済み・level 17の復活点は(66,83]・w=66キャンペーン完走（REST6 2フェーズ・23チャンク・54.8M nodes）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(66)=32（全称・等号付き）。帰結としてP(w)はw=6..66の全幅で決定済み（16プラトー12..21・跳躍22..25・24プラトー26..42・漸増43..48・32プラトー49..66）。level 17の復活点は(66,83]（K0785のP(83)≧34とK0790の34点最小幅83）。P(67)..P(82)はopen（P∈[32, 2⌈w/2⌉−4]・g0会計はK0797によりw≦84で有効）"
evidence: "数学的証明（K0798のREST6 2フェーズ機のw=66版・最初からREST6使用）。全3,300 maximal maskを完走（23チャンク・ノード計54,811,799・leaves=0・生残0・phase2必要mask 0件）。REST6=[19,23,7,29,43,47]・cap 2.4M nodes/chunk・lastDone冪等再開（resume_from=lastDoneを厳守・chunk境界の未走査mask 0件）。survivors(REST6)⊇survivors(REST16)（実現可能標準形は全合同証明書を通過・w26 L12制御でS*ちょうど1生残）によりREST6生残0はREST16でも生残0確定。level 17全滅⟹d+s≦16⟹P≦32。g0≧2形はK0797のconvention B classMax（g2=8・g3=12・g4=5・全形<17・拡張法33法・w≦84で有効）。下界: 2210円の全32点（v-span 94≦2·65=130）。制御: w=26 L=12 S*ちょうど1生残（K0782..K0798と一致）・mask200再実行整合・gap mask 488/773/794/820個別証明"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(66)=32 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11・unique=maximal 3,300）+ bit-set DFS level 17 全滅（maximal mask 3,300の全走査・REST6 2フェーズ・ノード上限チャンク・lastDone冪等再開）+ K0797 g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: S*制御（w26 L12・width65-pruning-audit実装）・2210 witness下界（v-span 94）・ノード会計のチャンク毎検証（54,811,799=34,019,316〔chunks 1-14〕+20,792,483〔chunks 15-23〕）・unique=maximal=3,300は各チャンク実行で再確認
  note: "heavy bandはw=65と同じ非単調構造でほぼ同じ位置: 第一帯~772..999・~1000 dip・第二帯~1190..1313（w=65は1190..1302）→1314以降は軽い帯（5.8k..7.5k/mask）が残り約3/5を占めた。総ノード54.8Mはw=65実績42.6Mの×1.29（成長則~1.35と整合）で外挿~55Mと一致。resume_from=lastDone規約（+1するとmaskを飛ばす）を厳守し境界gapは0件"
relations:
- type: depends_on
  target: K0798
  note: w=65完走機・REST6 2フェーズ方式の直接拡張。32プラトーを w=65 から w=66 へ延長
- type: depends_on
  target: K0797
  note: g0会計のw=66有効性（拡張法33法・g4形classMax=5・w≦84）・非標準形前提の正当化
- type: depends_on
  target: K0790
  note: streaming分類機・意味論・2210 witness
- type: supports
  target: K0785
  note: level 17復活点を (65,83] から (66,83] に狭窄
artifacts:
- path: research/experiments/width66-level-classification-20261113/scripts/width66_level_classify.ts
  role: verifier
  note: w=66用REST6 2フェーズstreaming分類機（決定的・依存なし・完走済みCFG.from=3300）
- path: research/experiments/width66-level-classification-20261113/output/width66_progress.json
  role: data
  note: 全23チャンクの機械出力（完了状態・ノード会計・heavy bandコスト曲線・gapCertifications）
- path: research/log/2026-11-13-width66-level-classification.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(66) = 32**（幅 w=66 の連続整数行・全 m ≥ 1・標準整数格子）。
   - 上界: level 17 全滅（全 3,300 maximal mask・23 チャンク・ノード計 54,811,799・
     leaves=0・生残 0・phase2 必要 mask 0 件）⟹ d+s ≤ 16 ⟹ P ≤ 32。
     g0 ≥ 2 形は K0797 classMax（g2=8・g3=12・g4=5・全形 < 17・w ≤ 84 で有効）。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 130 = 2·65）。
2. **帰結**: **P(w) は全幅 w = 6..66 で決定済み**
   （16 プラトー 12..21・跳躍 22..25・24 プラトー 26..42・漸増 43..48・**32 プラトー 49..66**）。
3. **level 17 の復活点は (66, 83]**（K0785 の 34 点最小幅 83 と合わせ）。

## 実行方式（REST6 2フェーズ・最初から）

- 全 23 チャンクを REST6=[19,23,7,29,43,47]（cap 2.4M nodes/chunk）で実行。
  健全性: survivors(REST6) ⊇ survivors(REST16)（実現可能標準形は全合同証明書を
  通過・w=26 L=12 制御で S* ちょうど 1 生残）。**フェーズ 2 必要 mask は 0 件**。
- chunks 15-23（完走セッション）: 1234→1258（~100k/mask）→1287（~83k）→1314（~89k・
  第二 heavy band は ~1313 で終了）→1657（343 mask・~7.0k）→1990（333 mask・~7.2k）→
  2309（319 mask・~7.5k）→2648（339 mask・~7.1k）→3065（417 mask・~5.8k）→
  **3300 完走（235 mask・1,592,483 nodes・capped なし・leaves=0）**。
- heavy band の位置は w=65 とほぼ同一（第二帯終点 1313 vs 1302）—
  heavy band の mask 位相は w よりむしろ法 9×11 の窓構造で決まるという
  K0798 の観察をさらに支持。

## 制御

- w=26 L=12 は S* ちょうど 1 生残（K0782..K0798 と一致・width65-pruning-audit 実装）。
- 2210 witness は w=49..67 で全 32 点（K0798 で再計数済み・v-span 94）。
- ノード会計: 34,019,316（chunks 1-14・第1-2セッション）+ 20,792,483（chunks 15-23・
  完走セッション）= 54,811,799。
- chunk 境界は連続（resume_from=lastDone 規約）で未走査 mask 0 件・
  gapCertifications は第1-2セッションの 4 件のみ。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- P(67)..P(82) は open（g0 会計は w ≤ 84 で有効なので level 17 全滅掃引の
  実行コストが唯一の壁。推定 w67 ~74M・w68 ~100M ノード・成長則 ~1.35）。
- 11×11 空盤・二石 root {49,60} は本項目と無関係に UNKNOWN のまま。
