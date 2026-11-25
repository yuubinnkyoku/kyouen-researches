# batch-28 (class 5343) 7-LOSS行 adoption 再監査 — Part CO (2026-11-23)

Part CO（publish-then-execute・単一オーナー）。宣言ノート
`research/log/2026-11-23-n11-centralreply-class5343-b28loss7-adoption-single-owner-note.md`
（commit `0ba87be4`、本文文字化け修正 commit `36827f18`）に従い、宣言後にこのhostで
公式実行した全成果物の実験dir。**verdict不消費・11×11はUNKNOWNのまま**。
閉鎖・被覆・secured・root勝敗の主張はしない。

## 何をしたか

**ADOPTED-CANONICAL = Part CH 正準BASE cache（6,294行・sha256 `3124461b…`）＋
batch-28 (class 5343) の7新規LOSS行** を、pinned byte-clone fail-closed union merger
（`scripts/s5_union_merge.py` sha256 `90711961…`）で統合採用した。

- 採用7行（2-pass node-exact・fresh LOSS only・nodes合計 38,784,669/pass）:
  | key | s5 | nodes |
  |---|---|---|
  | aa015 | 164462 | 6,152,494 |
  | aa017 | 170101 | 11,446,358 |
  | aa018 | 173654 | 214,968 |
  | aa023 | 193820 | 5,000,770 |
  | aa024 | 196053 | 5,003,631 |
  | aa029 | 199714 | 10,010,789 |
  | aa036 | 199721 | 955,659 |
- **aa003 は Part CH で採用済み・再送しない**（makerにBASE一貫ゲート:
  raw evidence (2, 4,070,373) ≡ BASE行）。
- **WIN 35行は不採用**（honest label。採用可否は scrutiny owner C++
  second-implementation gate pin `9193f5b6…` が唯一の経路。batch-14residual
  q042 / batch-26 l028 と同型の loss-only adoption）。
- **EXHAUSTED 11行は honest UNKNOWN**（両pass 15M枯渇・re-probe無し）。
- **class 5343 は解放されない**: 残46 unknown は 35 WIN + 11 EXHAUSTED の
  s5集合と完全一致することをextractorの機械ゲートで示す。
  closure表上は unknown 53→46、rank 19→4（純粋なランキング移動・flip 0・new free 0）。

## 公式実行記録（宣言 D1-D5・全ステップこのhostでbyte再現）

- D1 maker ×4 byte-stable: increment `bd5ef7d7…`（7行）・
  manifest `b47e07ca…`（schema `b28loss7-increments-manifest-v1`）。
  両drive kit 150+200ファイル全sha検証・全54キー2-pass node-exact・
  status.log絵図（drive-4 61行はdrive-5 109行のbyte-prefix・最終verdict行
  `2026-11-23T19:24:56Z aa054 WIN-HALT`・junk行 `"P1-FAIL "`ちょうど1行）・
  truncated sidecar 8不採用・aa003 BASE一貫ゲート。
- D2 merger selftest PASS → merge ×3 byte-identical:
  scenario cache 6,301行（WIN 158 / LOSS 6,143・259,886B）sha256 `854800f3…`、
  merge-audit 3通とも同一 sha256 `06f25f00…`。
  出力名はmerger tmp命名（出力名+".tmp"）と255B制限のため63B短縮名
  `merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-20261123.cache`（manifestに明記）。
- D3 refresh ×3 byte-identical ＋ 隔離実行（`env -i`・別tree・`PYTHONHASHSEED=random`）:
  refresh-summary `4727fb2b…`・closure-classes `9d3965d9…`（807→808行）・
  per-root-coverage `8e6fb981…`。probe-worklist（非出版・`1691027d…`）。
- D4 extractor ×4 byte-identical ＋ 隔離実行: 17 sha pin ＋ kit全350ファイル再検証・
  全54キー独立2-pass raw再検証・aa003 BASE一致・scen==base+7・
  holder算術（union 21・5343 own=7・他20クラスown=1）・closure pin・
  metrics pin・PRC IG movers pin → `output/decomp-deltas-b28loss7-adoption.json`
  sha256 `39b2802d…`（extractor script sha256 `67b2b3c5…`）。
  印刷行: flips=[] new_free=[] free_now 38→38 class5343_unknown 53→46 rank 19→4
  update8_resolved +7 joint_greedy 38295→38310 worklist 64746→64828
  kits=150+200 changed_rows=[] ig_movers=[central|16, central|4, central|49]
  closure_left=[12697] closure_entered=[5233, 5374]。
- D5 tamper battery（scratch tree・宣言の12種＋拡張）: round1 12種
  （pin層: increment/BASE改変・raw verdict flip・kit MANIFEST repin・keys改変・
  status junk除去・scenario cache改変 ＋ forged 8-row incrementの
  attacker-repin 非 LOSS混入・BASE append・class flip・manifest意味改変）
  全てfail-closed捕捉、復帰green ×2。round2 FULL-repin（正規表現機械repin・
  手打ちpin禁止）3種: BASE append+extractor repin → manifest BASE-cache意味ゲート、
  BASE append+maker repin → 6,295≠6,294行構造ゲート、class flip+keys/両kit
  MANIFEST repin → drive-4 row-audit header drift という交差検証ゲート。
  計15種すべて捕捉・0見逃し。
  - 注: round1での attacker-repin 意図の3件（P6/S2/S3/S7相当）は
    battery側のpin転写ミス（`9ebfdcc`を手打ちし1文字転写・機械検出済み）で
    repinが黙Failしたが、その場合でも原本pin層が全改変を捕捉。
    手打ちは禁止・正規表現機械repinで再実施（round2）した。
- 出版順: A scripts 4（commit `f2ab210d`）→ B increment+manifest+merge-audit×3
  （`071f3d8a`）→ C merged cache（`4d48d6a2`）→ D reaudit outputs + decomp-deltas
  （`ef0f34a7`）→ E README + MANIFEST-sha256（本案）。各push後にfetch-back
  sha256照合（B 5/5・C 1/1・D 4/4・Eは本MANIFEST）。

## 共有入力（published pins・非改変）

BASE cache 3124461b14e4f73a7248cbf5b96c7ff59ebfdcc05258adeb9c81791d86cc461e
（Part CH正準6,294行）・Part CH reaudit outputs（summary `76cad2a1…` /
closure `baa2db13…` / per-root-coverage `75e59441…`）・drive-4 kit MANIFEST
`1e4024f8…`（150ファイル）・drive-5 kit MANIFEST `e2d81055…`（200ファイル）・
batch-keys `af19208f…`・drive-5 status.log `ca1e98cc…`・drive-5 row-audit
（full-v2）`00c32383…`・drive-4 status.log `59817444…`・drive-4 row-audit `dcf078aa…`。

## UNKNOWN guarantee

本Partのどの時点でも、標準11×11空盤・19 central-reply roots・二石roots
{49,60}/{59,60}・S2 {59,60}・classes 1/2/4/10968/23964/5343
（aa001..aa054全キー含む）は **UNKNOWN のまま**。nodes数はbookkeepingであり
決してverdictではない。WIN 35行の採用判断には一切触れない
（scrutiny owner pin `9193f5b6…`専権）。verdictは不消費。
