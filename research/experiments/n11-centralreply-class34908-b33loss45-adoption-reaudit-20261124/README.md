# Part DT — batch-33 (class 34908) 45-LOSS canonical adoption (b33loss45)

2026-11-24。単一オーナー Part DT。**11×11 空盤は引き続き UNKNOWN**
(verdict 不消費・mixed packet)。
本実験dirは batch-33 (closure class 34908) の45行 fresh LOSS を canonical
chain に接続した記録であり、勝敗の決着ではない。class 34908 は本 Part で
**free化も excluded化もしていない** (9 verdict-pending/unknown 子が残る)。
宣言 `research/log/2026-11-24-part-dt-b33loss45-adoption-declaration.md`
(observed HEAD `ff3e99c1` 時点の宣言・publish-then-execute・本dirの出版が
同宣言の wave B〜D)。

## 何が確定したか (機械観測)

- canonical chain head (merged cache):
  `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-plus-b33loss45-20261124.cache`
  sha256 `973bcd19309eae1d73b26c40c3d6839a2f35baa74658e0794f19da6f9412ca5b`
  (6,547行・271,884 bytes・WIN 158 / LOSS 6,389)。
  BASE = Part DP 6,502行 `1ded9a08…` + `output/increment-b33loss45-20261124.cache`
  `255d54f5…` (45行 fresh LOSS・nodes 281,411,183/pass・2-pass node-exact・
  全行 decisive budget 15M・published batch-33 kit (Part DQ/DR/DS drive-1+2+3)
  raws) を fail-closed union merger (CU byte-clone `90711961…`) で併合
  (merge-audit ×3 同一 sha `13c97395…`)。
- batch-33 は probe-complete だが **mixed packet**: status.log 66行 =
  54 PASS verdict行 {45 LOSS・4 WIN (WIN-HALT marker af029/af047/af050/af053)
  ・5 EXHAUSTED (af003/af023/af034/af039/af048)} + 上記 marker + 3 resolved
  P2-TRUNCATED-RETRY marker {af008, af039, af048}・MISMATCH 0。
  increments-manifest (schema b33loss45-increments-manifest-v1・`4b0a9f0f…`) は
  `full_packet_eq_loss_only=false`・`win_scenario_exists=true`。
  **採用されたのは45 LOSS行のみ。4 WIN行は本 Part で一切消費されず**
  (scrutiny-owner C++ 第二実実装 gate pin `9193f5b6…` 通過後の別 adoption
  Part 待ち)・**5 EXHAUSTED行は honest UNKNOWN のまま** (高budget再probeは
  別宣言条件)。9行とも BASE に無く canonical cache にも入っていない。
- **class 34908 (56子 = BASE既知LOSS 2子 s5 {955954, 958114} + 54 batch key)
  は unknown のまま**: 45採用で unknown children 54→9・
  free_now 39→39・unknown 34,497→34,497・excluded_now 23→23・excluded 390→390・
  Board 子検証 39/39 (rejected 0)。**free_now/coverage は Board-derived な
  scheduling bookkeeping であり、root 勝敗でも coverage 主張でもない。**
- closure 表: 807→807行 (left=[]・entered=[]・行数不変)。class 34908行は
  rank 36→5・unknown_now 54→9・groups_served_count 4→5 のみ変化
  (Board子境界上 own採用 45 と一致)。class 34269 は groups_served_count
  5→4 (rank 5→6・unknown不変) の純 scheduling churn。
  完全 stable 775行・rank churn のみ 30行・unknown_now 変化クラスは
  class 34908 以外なし。
- per-root coverage: free/uncovered thirds は**全rootで不変** (classが
  freeでないため)。individual greedy union 減少は root 0 (3,054→3,009)・
  root 1 (6,353→6,352)・root 12 (2,986→2,984)・root 13 (6,175→6,174) のみ
  (再選択 churn)。root 27 = 119/119 不変。unique_groups 2,115→2,115。
  joint greedy union 36,968→36,849・worklist 64,609→64,564 (-45)・
  per-root remainingのオフセット {0: -3, 12: -2}
  (いずれも scheduler bookkeeping)。
- update8: resolved 187→188 (新規 s5 {962471}・採用45内)、
  remaining 31,672→31,671、groups_free_now 131 静止・
  known_universe 681→726・cache_rows_in_universe 658→703。
- decomp deltas: `output/decomp-deltas-b33loss45-adoption.json`
  (schema b33loss45-adoption-decomp-deltas-v1・extractor `70219793…`):
  両 refresh script (BASE Part DP `41bf706f…` / SCEN 本Part
  `5533b3f9…`) を scratch tree で byte-verbatim 再実行し出力が
  出版 pin と byte一致 (worklists 含む BASE `87c2ebd6…`・SCEN regen
  `5881d7b3…`・byte再現2回)。
- **公式隔離 rerun (published bytes から)**: maker (increment
  `255d54f5…` 再現) → merger ×3 (merged `973bcd19…` 3/3 byte一致) →
  refresh (3/3 byte一致 + worklist) → extractor (DECOMP OK changed=0
  rank_churn=30 gs_dec=1 stable=775・deltas byte一致) を全工程再現。
- tamper battery (sandbox・8項目): kit raw 改変 / status 改変 /
  status 行追加 (両方とも kit MANIFEST file-sha gate で捕捉) / val-gate
  file 欠落 / BASE cache 改変 / WIN-LOSS conflict 注入 (merger 出力なし
  rc=1) / merged (SCEN) cache 改変 / quarantine 注入 → 全て fail-closed
  ABORT rc=1、復旧後 sanity 再通過・battery 後の全出力は byte 同一
  (詳細は完了log `research/log/2026-11-24-part-dt-b33loss45-adoption-completion.md`)。

## honest な限界

- 再構築と公式隔離 rerun は単一 host 上の実行 (val-gate multi-host 出力は
  kit 出版物そのものを sha 照合したものであり、本 Part 実行の多 host 化を
  意味しない)。
- batch-33 raw 実行は 2-pass 逐次 (share_tt 不使用)・budget 15M
  (Part DQ/DR/DS drive の出版物・本 Part は読み込み専用で再実行せず)。
- free_now・coverage・joint greedy は全て scheduling bookkeeping で
  verdict ではない。class 34908 の unknown children 54→9 は「キャッシュ上で
  47子 exact LOSS・9子未決」を意味するだけで、11×11 の決着・二石root の
  決着・どの root の被覆完了も意味しない。
- **11×11 空盤は UNKNOWN。19 central-reply roots も全て UNKNOWN
  (root 27 baseline 119/119 不変)。二石root・S2 も UNKNOWN。**
  WIN 4行 (af029/af047/af050/af053) は verdict として不消費
  (probe-level WIN label のままで scrutiny gate 待ち)。EXHAUSTED 5行は
  honest UNKNOWN。

次のレーン候補: closure 表上位の小 class (23101 unknown 1 / 1849 unknown 1 /
2251 残1 / 5804 残4 = 未消費 WIN 1) は本 Part 後も不変。class 11490
(unknown 55・Part DS 時点 runner-up) の batch 選定、EXHAUSTED 5行の
高budget (>=60M) 再probe宣言、WIN 4行の scrutiny-owner C++ gate 実施が
後続 Part の候補。
