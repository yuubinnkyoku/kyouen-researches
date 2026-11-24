# Part DP — batch-32 (class 8730) 54-LOSS canonical adoption (b32loss54)

2026-11-24。単一オーナー Part DP。**11×11 空盤は引き続き UNKNOWN**
(verdict 不消費・loss-only packet なので不消費 WIN 行も存在しない)。
本実験dirは batch-32 (closure class 8730) の54行 fresh LOSS を canonical
chain に接続した記録であり、勝敗の決着ではない。
宣言 `research/log/2026-11-24-part-dp-b32loss54-adoption-declaration.md`
(commit `4711600e`, 2026-11-24, publish-then-execute)。

## 何が確定したか (機械観測)

- canonical chain head (merged cache):
  `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-plus-b31loss51-plus-b30loss43-plus-b32loss54-20261124.cache`
  sha256 `1ded9a083feabc095dd998c92002b47efc05b8666adf030501bcffc2873a9dd6`
  (6,502行・269,441 bytes・WIN 158 / LOSS 6,344)。
  BASE = Part DN 6,448行 `7bdfa236…` + `output/increment-b32loss54-20261124.cache`
  `ca4af3e7…` (54行 fresh LOSS・nodes 223,769,637/pass・2-pass node-exact・
  全行 decisive budget 15M・published batch-32 kit (Part DM drive-1) raws)
  を fail-closed union merger (CU byte-clone `90711961…`) で併合
  (merge-audit ×3 同一 sha `5ebfdbfb…`)。
- batch-32 は probe-complete かつ **loss-only**: status.log 54行全て PASS
  result=2 (LOSS)。WIN 0 / EXHAUSTED 0 / MISMATCH 0 / TRUNCATED 0。
  increments-manifest (schema b32loss54-increments-manifest-v1・
  `3f906dc8…`) は `full_packet_eq_loss_only=true`・
  `win_scenario_exists=false`。したがって本 Part に verdict 不消費の
  残務はなく、WIN行採用の scrutiny gate (C++ 第二実装 `9193f5b6…`) は
  本 Part の scope 外のまま。
- **class 8730 (58子) は unknown から free_now へ遷移**
  (54採用 + BASE既知LOSS 4子 s5 {144458, 212464, 310606, 311726} = 58子全て
  exact LOSS・Board 子検証 fail-closed 39/39・rejected 0)。
  free_now 38 → 39、unknown 34,498 → 34,497。
  **free_now は Board-derived な scheduling bookkeeping であり、root 勝敗
  でも coverage 主張でもない。**
- closure 変化はちょうど {8730 (free化で離脱), 8811}: 表は 808→807行、
  left=[8730]・entered=空・完全 stable 27行・rank churn のみ 779行・
  groups_served 減少 churn 0。class 8811 は own採用 2 で unknown 54→52。
- per-root coverage (class-8730 が serve する4 group のみ):
  root 38 free 13→15 / uncovered 106→104・root 5 free 8→10 /
  uncovered 111→109。root 27 = 119/119 不変。unique_groups 2,119→2,115。
  joint greedy union 36,902→36,968 (best-option 集合からの離脱に伴う
  再選択 churn・coverage 後退ではない)。
- update8: resolved 185→187 (新規 s5 {285539, 311727}・ともに採用54内)、
  remaining 31,674→31,672、groups_free_now 131 静止・joint probe worklist
  64,665→64,609・per-root remainingのオフセット {5: -5, 25: -2, 38: -4}
  (いずれも scheduler bookkeeping)。
- decomp deltas: `output/decomp-deltas-b32loss54-adoption.json`
  (schema b32loss54-adoption-decomp-deltas-v1・extractor `4c16da6e…`):
  両 refresh script (BASE Part DN `d45832a6…` / SCEN 本Part
  `41bf706f…`) を scratch tree で byte-verbatim 再実行し出力が
  出版 pin と byte 一致 (worklists 含む BASE `006ccd78…` 相当・
  SCEN regen `87c2ebd6…`・byte再現2回)。
- **公式隔離 rerun (published bytes から)**: maker (increment
  `ca4af3e7…` 再現) → merger ×3 (merged `1ded9a08…` 3/3 byte一致・
  audit JSON は入力path表記のみ相違) → refresh (4/4 byte一致) →
  extractor (DECOMP OK changed=1 rank_churn=779 gs_churn=0 stable=27・
  deltas byte一致) を全工程再現。
- tamper battery (sandbox, 8項目): kit raw 改変 / status 改変 /
  status 行追加 / val-gate file 欠落 / BASE cache 改変 / WIN-LOSS
  conflict 注入 (merger 出力なし rc=1) / merged (SCEN) cache 改変 /
  quarantine 注入 (maker・refresh 両 gate) → 全て fail-closed ABORT rc=1、
  復旧後 sanity 再通過・battery 後の全出力は byte 同一
  (詳細は完了log `research/log/2026-11-24-part-dp-b32loss54-adoption-completion.md`)。

## honest な限界

- 再構築と公式隔離 rerun は単一 host 上の実行 (val-gate multi-host 出力は
  kit 出版物そのものを sha 照合したものであり、本 Part 実行の多 host 化を
  意味しない)。
- batch-32 raw 実行は 2-pass 逐次 (share_tt 不使用)・budget 15M
  (Part DM drive-1 の出版物・本 Part は読み込み専用で再実行せず)。
- free_now・coverage・joint greedy は全て scheduling bookkeeping で
  verdict ではない。class 8730 の free_now は「キャッシュ上で58子全て
  exact LOSS」を意味するだけで、11×11 の決着・二石root の決着・
  どの root の被覆完了も意味しない。
- **11×11 空盤は UNKNOWN。19 central-reply roots も全て UNKNOWN
  (root 27 baseline 119/119 不変)。二石root・S2 も UNKNOWN。**

次のレーン候補: closure 表上位の小 class (23101 unknown 1 / 1849 unknown 1 /
2251 残1 / 5804 残4 = 未消費 WIN 1) は本 Part 後も不変。
