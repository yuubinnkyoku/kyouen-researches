---
id: K0798
title: "幅65の円点数の完全決定 P(65)=32 — 32点プラトーがw=49..65に拡大・P(w)は全幅6..65で決定済み・level 17の復活点は(65,83]・REST6 2フェーズ機の完走検証"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(65)=32（全称・等号付き）。帰結としてP(w)はw=6..65の全幅で決定済み（16プラトー12..21・跳躍22..25・24プラトー26..42・漸増43..48・32プラトー49..65）。level 17の復活点は(65,83]（K0785のP(83)≧34とK0790の34点最小幅83）。P(66)..P(82)はopen（P∈[32, 2⌈w/2⌉−4]）"
evidence: "数学的証明（K0790/K0794 streaming機のw=65版+REST6 2フェーズ枝刈り）。全3,296 maximal maskを完走（27チャンク・ノード計42,631,099・leaves=0・生残0・phase2必要mask 0件）。chunks 1-18はREST16（cap 1.2M）・chunks 19-27はREST6=[19,23,7,29,43,47]（cap 2.4M・word-ops観点で同コスト）で、survivors(REST6)⊇survivors(REST16)（実現可能標準形は全合同証明書を通過・w26 L12制御でS*ちょうど1生残）によりREST6生残0はREST16でも生残0確定。level 17全滅⟹d+s≦16⟹P≦32。g0≧2形はK0797のconvention B classMax（g2=8(法33)・g3=12(法22)・g4=5(法17)・全形<17・拡張法33法）。下界: 2210円の全32点（v-span 94≦2·64）。制御: w=26 L=12 S*ちょうど1生残（REST16/REST6両方で・K0782..K0794と一致）"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(65)=32 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11）+ bit-set DFS level 17 全滅（maximal mask 3,296の全走査・REST6 2フェーズ・ノード上限チャンク・lastDone冪等再開）+ K0797 g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: S*制御（REST16/REST6両方）・2210 witness再計数（w=49..67で全32点）・ノード会計のチャンク毎検証（42,631,099=31.2M+9.6M+1,831,099）・REST6健全性はpruning-audit実験の別実装
  note: "heavy bandは非単調（~1000で沈み~1190で再出現・1302以降沈下）で局在性があり、総ノード実績42.6Mは同密度外挿推定~130M..260M opsを大きく下回った。REST6 2フェーズの実コスト削減（word-ops 40..45%）はheavy bandに依存せず全帯で有効。g4類サイズ引数はw=65で⌈65/4⌉=17=Lに達するがK0797の拡張法33法（法17の素数冪級）でclassMax=5に精密化済み（会計はw=65..84で有効）"
relations:
- type: depends_on
  target: K0794
  note: w=64完了機の直接拡張（3ワード化）。32プラトーを w=64 から w=65 へ延長
- type: depends_on
  target: K0797
  note: g0会計のw=65有効性（拡張法33法・g4形classMax=5）・非標準形前提の正当化
- type: depends_on
  target: K0790
  note: streaming分類機・意味論・2210 witness
- type: supports
  target: K0785
  note: level 17復活点を (59,83] から (65,83] に狭窄
artifacts:
- path: research/experiments/width65-level-classification-20261113/scripts/width65_level_classify.ts
  role: verifier
  note: w=65用3ワードstreaming分類機（REST16・決定的・依存なし）
- path: research/experiments/width65-level-classification-20261113/output/width65_progress.json
  role: data
  note: 全27チャンクの機械出力（完了状態・ノード会計・heavy bandコスト曲線）
- path: research/experiments/width65-pruning-audit-20261113/scripts/width65_pruning_audit.ts
  role: verifier
  note: REST6 2フェーズ機（chunks 19-27で使用）・健全性の実測
- path: research/log/2026-11-13-width65-level-classification.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(65) = 32**（幅 w=65 の連続整数行・全 m ≥ 1・標準整数格子）。
   - 上界: level 17 全滅（全 3,296 maximal mask・27 チャンク・ノード計 42,631,099・
     leaves=0・生残 0）⟹ d+s ≤ 16 ⟹ P ≤ 32。
     g0 ≥ 2 形は K0797 classMax（g2=8・g3=12・g4=5・全形 < 17）。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 128）。
2. **帰結**: **P(w) は全幅 w = 6..65 で決定済み**
   （16 プラトー 12..21・跳躍 22..25・24 プラトー 26..42・漸増 43..48・**32 プラトー 49..65**）。
3. **level 17 の復活点は (65, 83]**（K0785 の 34 点最小幅 83 と合わせ）。

## 実行方式（REST6 2フェーズ）

- chunks 19-27 は REST6=[19,23,7,29,43,47]（cap 2.4M nodes/chunk）。
  健全性: survivors(REST6) ⊇ survivors(REST16)（実現可能標準形は全合同証明書を
  通過するため誤殺なし・w=26 L=12 制御で S* がちょうど 1 生残）。
  REST6 生残 0 の mask は REST16 でも生残 0 確定。**フェーズ 2 必要 mask は 0 件**。
- heavy band は非単調: mask ~772..975（71k..150k/mask・REST16）→ ~1000 で沈み
  （~11k/mask）→ ~1190 で再出現（57k..73k/mask）→ 1302 以降は沈下し
  残り約 2/3 は軽い帯（4.6k..7.1k/mask）。総ノード 42.6M は外挿推定を大きく下回る。

## 制御

- w=26 L=12 は S* ちょうど 1 生残（REST16・REST6 両方・K0782..K0794 と一致）。
- 2210 witness は w=49..67 で全 32 点。
- ノード会計: 31.2M（chunks 1-22・progress JSON 前々回）+ 9.6M（chunks 23-26）+
  1,831,099（chunk 27・最終 306 mask・capped なし完走）= 42,631,099。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- P(66)..P(82) は open（g0 会計は K0797 により w ≤ 84 で有効なので
  level 17 全滅掃引の実行コストが唯一の壁）。
