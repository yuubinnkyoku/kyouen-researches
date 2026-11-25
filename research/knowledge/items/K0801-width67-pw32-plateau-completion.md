---
id: K0801
title: "幅67の円点数の完全決定 P(67)=32 — 32点プラトーがw=49..67に拡大・P(w)は全幅6..67で決定済み・level 17の復活点は(67,83]・w=67キャンペーン完走（REST6 2フェーズ・31チャンク・78.3M nodes）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(67)=32（全称・等号付き）。帰結としてP(w)はw=6..67の全幅で決定済み（16プラトー12..21・跳躍22..25・24プラトー26..42・漸増43..48・32プラトー49..67）。level 17の復活点は(67,83]（K0785のP(83)≧34とK0790の34点最小幅83）。P(68)..P(82)はopen（P∈[32, 2⌈w/2⌉−4]・g0会計はK0797によりw≦84で有効）"
evidence: "数学的証明（K0799のREST6 2フェーズ機のw=67版・最初からREST6使用）。全3,300 maximal maskを完走（31チャンク・ノード計78,319,651・leaves=0・生残0・phase2必要mask 0件）。REST6=[19,23,7,29,43,47]・cap 2.4M nodes/chunk・lastDone冪等再開（resume_from=lastDoneを厳守・chunk境界の未走査mask 0件）。survivors(REST6)⊇survivors(REST16)（実現可能標準形は全合同証明書を通過・w26 L12制御でS*ちょうど1生残）によりREST6生残0はREST16でも生残0確定。level 17全滅⟹d+s≦16⟹P≦32。g0≧2形はK0797のconvention B classMax（拡張法33法・全形<17・w≦84で有効）。下界: 2210円の全32点（v-span 94≦2·66=132）。制御: unique=maximal=3,300はharness制御（w64=3,288・w65=3,296・w66=3,300完全再現）および各チャンク実行で再確認・mask 0..487の前置区間はw=66と完全一致（word-ops 255673713/262407946）"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(67)=32 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11・unique=maximal 3,300）+ bit-set DFS level 17 全滅（maximal mask 3,300の全走査・REST6 2フェーズ・ノード上限チャンク・lastDone冪等再開）+ K0797 g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: harness制御（w64/65/66のunique=maximal完全再現）・w=66前置区間一致（chunks 1-2 word-ops完全一致）・ノード会計のチャンク毎検証（78,319,651=60,000,000〔chunks 1-23〕+16,800,000〔chunks 24-30〕+1,519,651〔chunk 31完走分〕）・2210 witness下界（v-span 94・K0798で再計数済み）
  note: "heavy band構造はw=65/66と同一位相だが第一帯入り口は約3倍重い（~343k/mask）: 第一帯~770..987 → dip ~987..1155（~14.3k/mask）→ 第二帯~1190..1320 → 以降軽い帯~7..13k/mask。第二帯終点は右肩上がり則1302→1313→1320を維持（窓位相は法9×11の構造で決まり終点はwとともに右へずれる）。総ノード78.3Mはw=66実績54.8Mの×1.43（成長則~1.35よりやや高く第一帯加重の反映）。resume_from=lastDone規約を厳守し境界gapは0件"
relations:
- type: depends_on
  target: K0799
  note: w=66完走機・REST6 2フェーズ方式の直接拡張。32プラトーを w=66 から w=67 へ延長
- type: depends_on
  target: K0797
  note: g0会計のw=67有効性（拡張法33法・w≦84）・非標準形前提の正当化
- type: depends_on
  target: K0790
  note: streaming分類機・意味論・2210 witness
- type: supports
  target: K0785
  note: level 17復活点を (66,83] から (67,83] に狭窄
artifacts:
- path: research/experiments/width67-level-classification-20261113/scripts/width67_level_classify.ts
  role: verifier
  note: w=67用REST6 2フェーズstreaming分類機（決定的・依存なし・完走済みCFG.from=3300）
- path: research/experiments/width67-level-classification-20261113/output/width67_progress.json
  role: data
  note: 全31チャンクの機械出力（完走状態・ノード会計・heavy bandコスト曲線）
- path: research/log/2026-11-13-width67-level-classification.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(67) = 32**（幅 w=67 の連続整数行・全 m ≥ 1・標準整数格子）。
   - 上界: level 17 全滅（全 3,300 maximal mask・31 チャンク・ノード計 78,319,651・
     leaves=0・生残 0・phase2 必要 mask 0 件）⟹ d+s ≤ 16 ⟹ P ≤ 32。
     g0 ≥ 2 形は K0797 classMax（全形 < 17・拡張法 33 法・w ≤ 84 で有効）。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 132 = 2·66）。
2. **帰結**: **P(w) は全幅 w = 6..67 で決定済み**
   （16 プラトー 12..21・跳躍 22..25・24 プラトー 26..42・漸増 43..48・**32 プラトー 49..67**）。
3. **level 17 の復活点は (67, 83]**（K0785 の 34 点最小幅 83 と合わせ）。

## 実行方式（REST6 2フェーズ・最初から）

- 全 31 チャンクを REST6=[19,23,7,29,43,47]（cap 2.4M nodes/chunk）で実行。
  健全性: survivors(REST6) ⊇ survivors(REST16)（実現可能標準形は全合同証明書を
  通過・w=26 L=12 制御で S* ちょうど 1 生残）。**フェーズ 2 必要 mask は 0 件**。
- chunks 24-31（完走セッション）: 1320→1662（343 mask・~7.0k/mask・
  **第二 heavy band は 1320 で終了**）→1954（292 mask・~8.2k）→2107（153 mask・~15.7k・
  中間バンプ）→2393（286 mask・~8.4k）→2620（227 mask・~10.6k）→2952（332 mask・~7.2k）→
  3140（188 mask・~12.8k）→**3300 完走（160 mask・1,519,651 nodes・capped なし・leaves=0）**。
- heavy band 位相: 第一帯 ~770..987（入り口 ~343k/mask・w=66 の約 3 倍）→
  dip ~987..1155 → 第二帯 ~1190..1320。第二帯終点は右肩上がり則
  1302（w=65）→1313（w=66）→1320（w=67）を維持。

## 制御

- harness 制御: w=64→3,288・w=65→3,296・w=66→3,300 を本機で完全再現
  （w=67 の 3,300 は偽でない）。各チャンク実行でも unique=maximal=3,300 を再確認。
- 前置区間制御: chunks 1-2 の word-ops は w=66 と完全一致
  （255673713 / 262407946）→ mask 0..487 は w=66 と同一挙動。
- 2210 witness は w=49..67 で全 32 点（K0798 で再計数済み・v-span 94）。
- ノード会計: 60,000,000（chunks 1-23）+ 16,800,000（chunks 24-30）+
  1,519,651（chunk 31）= 78,319,651。
- chunk 境界は連続（resume_from=lastDone 規約）で未走査 mask 0 件・
  gapCertifications は不要（境界個別証明 0 件）。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- P(68)..P(82) は open（g0 会計は w ≤ 84 で有効なので level 17 全滅掃引の
  実行コストが唯一の壁。推定 w68 ~105M ノード・成長則 ×1.35..1.43）。
- 11×11 空盤・二石 root {49,60} は本項目と無関係に UNKNOWN のまま。
