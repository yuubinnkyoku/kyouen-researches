---
id: K0802
title: "幅68の円点数の完全決定 P(68)=32 — 32点プラトーがw=49..68に拡大・P(w)は全幅6..68で決定済み・level 17の復活点は(68,83]・w=68キャンペーン完走（REST6 2フェーズ・40チャンク+独立全幅再実行・92.2M/96.6M nodes）"
kind: proposition
status: proved
topics: [rectangles, geometry, variants]
aliases: []
scope: "幅w固定・長さm可変（全m≧1）の標準整数格子の円の格子点数: P(68)=32（全称・等号付き）。帰結としてP(w)はw=6..68の全幅で決定済み（16プラトー12..21・跳躍22..25・24プラトー26..42・漸増43..48・32プラトー49..68）。level 17の復活点は(68,83]（K0785のP(83)≧34とK0791の34点最小幅83）。P(69)..P(82)はopen（P∈[32, 2⌈w/2⌉−4]・g0会計はK0797によりw≦84で有効）"
evidence: "数学的証明（K0801のREST6 2フェーズ機のw=68版）。全3,300 maximal maskを完走（sandbox chunks 1-24〔55.2M nodes〕+ネイティブNode chunks 25-40〔37,019,331 nodes〕+gap証明2件〔587,531 nodes〕・leaves=0・生残0・phase2必要mask 0件）。REST6=[19,23,7,29,43,47]・cap 2.4M nodes/chunk・lastDone冪等再開（resume_from=lastDoneを厳守・chunks 25-40の境界はfrom=直前lastDone verbatimでgap 0件）。survivors(REST6)⊇survivors(REST16)（実現可能標準形は全合同証明書を通過・w26 L12制御でS*ちょうど1生残）によりREST6生残0はREST16でも生残0確定。level 17全滅⟹d+s≦16⟹P≦32。g0≧2形はK0797のconvention B classMax（拡張法33法・全形<17・w≦84で有効）。下界: 2210円の全32点（v-span 94≦2·67=134）。独立確認: 完走後にネイティブNode.js（v22・repo scriptと同一アルゴリズム）でfrom=0の全幅再実行を単一連続42チャンク・96,626,896 nodes・28.6秒で実施しleaves=0・生残0・gap 0件を再現。交差制御: 再実行のchunks 1-6は境界位置とwordOpsがsandbox記録と完全一致・mask 788/807のclassifyOne node数（314,127/273,404）も完全一致・w26 L12制御でS*ちょうど1生残・harness制御（w64=3,288・w65=3,296・w66/67=3,300）完全再現"
solution:
  board: 幅w固定長m可変の標準整数格子
  level: strong
  outcome: conditional
  classification: [all-safe-grundy]
  coverage: P(68)=32 は全称・全 m≧1・全安全局面
  conditions: 連続整数行
  verification: [mathematical-proof]
  certificate: 窓マスク完備候補生成（mod 9×11・unique=maximal 3,300）+ bit-set DFS level 17 全滅（maximal mask 3,300の全走査・REST6 2フェーズ・ノード上限チャンク・lastDone冪等再開）+ K0797 g0≧2 convention-B classMax 会計 + 2210 witness 下界
  independent_check: ネイティブNode.js全幅再実行（from=0・単一連続・96,626,896 nodes・leaves=0・生残0）・交差制御3種（chunks 1-6 wordOps完全一致・classifyOne mask 788/807 node数完全一致・w26 L12 S* 1生残）・harness制御（w64/65/66/67のunique=maximal完全再現）・2210 witness下界（v-span 94・K0798で再計数済み）
  note: "heavy band構造: 第一帯~770..984（~46..480k/mask・最重要部は880..890の~480kで局在）→ ~1000沈み込み（~17k/mask）→ 第二帯~1190..1308（~31..240k/mask）。第二帯終点はw=67の1320を下回り右肩上がり則1302→1313→1320はw=68で反例（終点はmask位相で単調に右へずれるわけではない）。総ノードは2経路で92.8M（継続走査+gap証明）と96.6M（単一連続再実行）— 後者がgapなしの全走査。ネイティブNode実行はsandbox実行の約70倍高速（2.4M chunkあたり0.84秒）で以後のw掃引の実行コストの壁は実質的に消滅"
relations:
- type: depends_on
  target: K0801
  note: w=67完走機・REST6 2フェーズ方式の直接拡張。32プラトーを w=67 から w=68 へ延長
- type: depends_on
  target: K0797
  note: g0会計のw=68有効性（拡張法33法・w≦84）・非標準形前提の正当化
- type: depends_on
  target: K0803
  note: maximal mask数3,300はw=66..132の有限測定（本項の3,300と整合）
- type: supports
  target: K0785
  note: level 17復活点を (67,83] から (68,83] に狭窄
artifacts:
- path: research/experiments/width68-level-classification-20261113/scripts/width68_level_classify.ts
  role: verifier
  note: w=68用REST6 2フェーズstreaming分類機（決定的・依存なし・完走済みCFG.from=3300）
- path: research/experiments/width68-level-classification-20261113/output/width68_progress.json
  role: data
  note: 全40チャンクの機械出力（完走状態・ノード会計・heavy bandコスト曲線・交差制御）
- path: research/experiments/width68-level-classification-20261113/output/width68_native_completion.json
  role: data
  note: ネイティブNode.js独立全幅再実行（from=0・42チャンク・96,626,896 nodes）と交差制御の生出力
- path: research/log/2026-11-13-width68-level-classification.md
  role: log
  note: 判断・教訓・レジューム
---

## 命題（証明済み・全称・等号付き）

1. **P(68) = 32**（幅 w=68 の連続整数行・全 m ≥ 1・標準整数格子）。
   - 上界: level 17 全滅（全 3,300 maximal mask・leaves=0・生残 0・phase2 必要 mask 0 件）⟹ d+s ≤ 16 ⟹ P ≤ 32。
     g0 ≥ 2 形は K0797 classMax（全形 < 17・拡張法 33 法・w ≤ 84 で有効）。
   - 下界: 2210 円の全 32 点（v-span 94 ≤ 134 = 2·67）。
2. **帰結**: **P(w) は全幅 w = 6..68 で決定済み**
   （16 プラトー 12..21・跳躍 22..25・24 プラトー 26..42・漸増 43..48・**32 プラトー 49..68**）。
3. **level 17 の復活点は (68, 83]**（K0785 の 34 点最小幅 83 と合わせ）。

## 実行方式（REST6 2フェーズ・継続+独立全幅再実行）

- sandbox chunks 1-24（55.2M nodes・K0801 機の verbatim・これまでの進行記録）で
  mask 0..1222（gap 証明 2 件込み）を走査済み。
- chunks 25-40（ネイティブ Node.js v22・repo script と同一アルゴリズム・37,019,331 nodes）で
  mask 1223..3299 を完走（境界は from=直前 lastDone verbatim・gap 0 件・
  最終 chunk 40 は 97 mask・1,019,331 nodes・capped なし完走）。
- **独立全幅再実行**: 完走後、from=0 から単一連続 42 チャンク・96,626,896 nodes・28.6 秒で
  全 3,300 mask を隣接漏れなしに再走査（leaves=0・生残 0・gap 証明不要の単一実行）。
  これが第二の完全走査証拠であり、境界 off-by-one の歴史（mask 788/807）を
  含まない gap なしの走査として独立に P ≤ 32 を支える。

## 制御

- 交差環境決定性: 再実行の chunks 1-6 は境界位置と wordOps
  （245,724,873 / 255,867,318 / 258,146,326 / 257,509,173 / 229,646,635 / 225,603,695）
  が sandbox 記録と完全一致。
- classifyOne 交差制御: mask 788 → 314,127 nodes・mask 807 → 273,404 nodes が
  sandbox gap 証明の記録値と完全一致（leaves=0・生残 0）。
- w=26 L=12 制御: S*={0,1,3,4,7,10,15,18,21,22,24,25} ちょうど 1 生残（誤殺なし）。
- harness 制御: w=64→3,288・w=65→3,296・w=66/67→3,300 を完全再現
  （w=68 も 3,300・K0803 の飽和観察と整合）。
- 2210 witness は w=49..68 で全 32 点（v-span 94 ≤ 134）。

## 構造観察

- heavy band 位相: 第一帯入り口 ~770（窓位相不变則）・最重要部 880..890（~480k/mask・
  chunk12-13）→ ~1000 沈み込み（~17k/mask）→ 第二帯 ~1190..**1308**。
- **第二帯終点は w=67 の 1320 を下回った**（右肩上がり則 1302→1313→1320 は
  w=68 で反例。終点は w に対して単調ではない）。
- 総ノードは 96.6M（w=67 の 78.3M の ×1.23・成長則 ~1.35 を下回る）。
- **ネイティブ Node.js 実行は 2.4M チャンクあたり 0.84 秒**（sandbox の約 70 倍）。
  以後の w=69..84 掃引（K0797 会計の有効範囲）は実行コストの壁を実質的に失った
  （w=68 全幅で 28.6 秒）。本観察は K0797 の範囲内で P(w) を w=84 まで決定する
  可能性を開く（次の実行課題）。

## 限界

- 標準整数格子限定。任意間隔平行行には主張しない。
- P(69)..P(82) は open（level 17 全滅掃引は K0797 の会計のもとでそのまま
  P(w)=32 に昇格できる・w=83,84 は 34 点以上の witness が既知なので
  level 17 は死なないことが予想される）。
- 11×11 空盤・二石 root {49,60} は本項目と無関係に UNKNOWN のまま。
