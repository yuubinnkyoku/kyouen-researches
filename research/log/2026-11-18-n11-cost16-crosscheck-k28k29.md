# 2026-11-18 N11 cost-16生存曲線crosscheck: k=28・k=29への拡張 — value・structure・record 3層84 checks 0 failure・k29 I-E marginal恒等式(総/A/B)をPublication byte列から独立再検証

本logは[独立crosscheck script](../experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost16_survival_k13_k14_crosscheck_20261118.py)をk=27-era版（28,089B）から**k=28・k=29を含むk=29-era版に機械拡張**（発生回数assert付き置換11ブロック・`py_compile`通過）し、GitHub mainに出版済みの実ファイル（jsdelivr/raw mirrorからblob sha1 pin検証付きでfetch）に対して実行したものである。**84 checks, 0 failures。生存曲線は組合せ値の照合であり、verdict生成ではない。標準11×11空盤はUNKNOWNのまま。**

## 拡張内容

1. **PINS追加**: k28 result JSON `99db3a9a48d044727b3a4d83fb7fc97daa7513d2`（commit `efc500fa`）・k29 result JSON `795665316c300a186979bafd2817b6961de2de60`（commit `29fb9f92`）。value layer参照seriesをk27→**k29**（K=29）に更新。
2. **record layer JSONL pin追加**: k28 JSONL `6316793b94fe7e95c3d91e283a4229cc7c7f5730`（3,652 record: pair 27 / triple 351 / quad 2,925 / quint 331 / anchor 10 / cross 8・commit `42182831`）・k29 JSONL `7b2afe8559de6d94a82a4b0d3f62208572b51910`（5,828 record: pair 28 / triple 378 / quad 3,276 / quint 2,128 / anchor 10 / cross 8・commit `40f74ef1`）。
3. **quint census era拡張**: `for n in (26, 27)` → `(26, 27, 28, 29)`。層接続checkをk27→k26単発から**chain化**： (27,26)・(28,27)・(29,28) の3本すべて「full(k) − 新層(C(k−1,4)) = full(k−1)」が成立。
4. **mirror robustness修正（新事実）**: jsdelivr CDNが本scriptの古いk13/k14-era版（6,410B）をstale serveしていたことが判明したため、`fetch_bytes`を「blob sha1不一致なら次mirrorへfall-through、全mirror失敗時のみ例外」に強化（sha fail-loud性は維持）。

## 検証結果（84 checks all PASS・実行37秒・network fetch）

- **value layer**: grand total 2,966,450,341,680,481,356 恒等・kill/A_survive/B_survive単調性k0〜k29・marginal chainがk13 published detailと全域一致・direct再計算anchor k4/8/10/11/12・全publication間kill series不変（k13〜k29の17 JSONがhistory rewriteなしで相互一致）。
- **structure layer**: rank16〜29 root被覆・membership/A/B分割・新pair census・全triple census・新quad censusをpinned aggregateから独立再導出し全一致。quint census k26=1,872/63,908/0・k27=2,181/78,549/0・k28=2,512/95,768/0・**k29=4,640/114,115/0**を機械再導出（二重行ヒストグラム k28 {15:455, 18:1,609, 19:448}・k29 {15:738, 16:172, 18:2,906, 19:824} 含む）。
- **record layer (k26〜k29)**: 4 JSONL計17,180 recordを独立分類器で全件再分類・`anchor4`双子lineage一致・新pair/triple/quadの組合せ完全性・新b_only quint集合が再導出集合と一致・**marginal I-E恒等式（総/A/B 3本×4era=12本）をrecord jointのみから再合成**:
  - k28: 総 59,627,615,102,262,832 / A 46,499,478,498,461,827 / B 13,128,136,603,801,005（=published kill差分・**rank-29本計算前に未完だったk28 anchor恒等式の完了**）
  - k29: 総 27,332,103,196,834,517 / A 21,489,874,806,440,114 / B 5,842,228,390,394,403（Kill差分と厳密一致）

k29の3恒等式は本レーンのfinalizeとは独立系統（実験script importなし・出版byte列のみ入力）による再検証であり、[k29出版](2026-11-18-n11-cost16-survival-k29.md)（script+log `f6966f18`・JSON `29fb9f92`・JSONL `40f74ef1`）の外部検証となった。

## 11×11空盤の現況（interpretation guard）

標準11×11空盤は**UNKNOWN**。空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4のいずれについても、本crosscheckは何のverdictも生成しない。生存曲線の一致は「出版数値の算術的整合」の証明であり、勝敗とは無関係である。
