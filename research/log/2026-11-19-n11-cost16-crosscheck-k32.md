# 2026-11-19 N11 cost-16 crosscheck: k=32対応拡張 — 値・構造・record・preread の全層で +26 checks（149 checks all pass・二重実行byte-identical・rank-32 preread純Python正確整数の機械再導入・累積disjoint quad 820=662+158の非ハードコード検証・rank-30/31回帰block機械再導入）

k=32本計算出版（script+log `62c29d080`・result JSON `595f0a2795`〔blob `6bf47e8745300ae6235180591978daf9d7fe09e5`〕・record JSONL `f8bd71fed1`〔blob `c4f06b23ad64ae97cb642b244f2d675cd0bf6903`〕）と、当レーンによる完全独立第二実行の全値一致（rerun log commit `713cc6dde`）を受けて、検証サイドの総合crosscheck script `cost16_survival_k13_k14_crosscheck_20261118.py` を k=32 対応に拡張した（拡張版 58,528B・blob `2e139fb078a81bcf7a05c2b6647e0f6d804059bf`・sha256 `abb5ab6705bd3299ee8af7693a5e7890aae868f4d855730b63df7c9f691afd5e`・実験script importなし・純粋標準ライブラリ）。**生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。**

## 拡張内容（旧版123 checks → 149 checks all pass）

1. **値層（既存checkのk=32への拡張）**: 参照JSONを k32 result JSON（pinned blob `6bf47e87…`）に切り替え、grand-total恒等・ 単調性・marginal chain k2..k32（出版 `survival.marginal` detail の `k32_minus_k31` = 25,276,899,310,145,517・`m32` = 120,146,272,057,315,812 と照合）・A/B分割恒等・reproduce anchors k16..k32・cross-publication系列一致 k13..k32 が全て k32 点まで通る。
2. **構造層の機械再導入の拡張**: rank_root_fields（rank32_root (15,23)・root hex `00000000000000801222000000081000`・A/B分割正確整数）・新pair census 7 shared / 24 disjoint・full triple census C(32,3)=4,960 = 2,992/980/988・新quad census 1,878/2,459/158 がpinned aggregateから独立再導出で一致。**quint census層**: C(32,5)=201,376 = 8,797 b_only / 192,579 zero / 0 disjoint・二重行hist {15:1616, 16:304, 18:5111, 19:1766}（行23不参加）・`quints_zero_synth_count` 29,455 = C(31,4) − 2,010・prev-layer恒等 8,797 = 6,787 + 2,010。**sextet census**: C(32,6)=906,192 all zero の独立再導入（I-E quint打ち切り9連続機械保証の更新）。
3. **record層（新規+11 checks）**: k32 JSONL（blob `c4f06b23…`）の 7,019 records 全件を独立分類器で再分類: kind別計数（pair 31 + triple 465 + quad 4,495 + quint 2,010 + anchor 10 + cross 8 = 7,019）・anchor/cross全match・anchor4両lineage一致（k31 record層の2 disjoint quadに再錨付け）・新pair/triple/quadの組合せ完全性・新b_only quint集合が classify2 による機械再導出集合と一致・quad record census一致・**I-E marginal恒等式（total/A/B 3本）**: m32 − Σs2 + Σs3 − Σs4 + Σs5B = 25,276,899,310,145,517 = kill(32) − kill(31) が record joints のみからの再加算で厳密成立（A型: −Σs4A含む、B型: +Σs5B含む）。
4. **preread層5（k=32・新規+11 checks）**: k32 preread JSON（commit `490a3e44`・blob `6d49ab5bea27c967e15b482b33e376510c62b857`・純Python正確整数）を機械再導入: (i) rank32 root・行15/23のprior hit indices {[0,13,14,16,17,22], [11]}・membership/A/Bがaggregate正確整数と厳密一致し A+B==M 成立（k31のNode丸めerratumの不発生を逆方向から機械保証）。(ii) 新層census 4種（pairは shared/disjoint schema・機械の classify では shared→b_only に対応する対応関係を明記）。(iii) 新層b_only二重行hist 3種（triple {15:130, 18:105, 19:21, 23:9 …}・quad {15:635, 18:847, 19:315, 23:12 …}・quint {18:962, 15:613, 19:370, 16:65}=和2,010、行23はquint層に不在）。(iv) b_only quintの4-subset profile {3/2/0: 2,010}・disjoint quad 158本全てunionサイズ8・**累積820 = 機械再導出662（C(31,4)全走査）+158（新層）の追加恒等（ハードコード定数なし）**。(v) full triples（C(32,3)=4,960 counts+二重行hist）・full quints（==キャッシュ済quint機械census）・sextet（906,192 all zero）。(vi) rank-30/rank-31両回帰block（new_census 4層・3種hist・full_triples+hist・full_quints・sextet）の統一helperによる機械再導入（full quint/sextetはキャッシュ済みC(n,5)/C(n,6)機械censusと一致）。(vii) k32 result JSON側の preread_match.* 5 checkの存在・PASS・rank32_rootの正確整数。

## 実行と検証

- 実行: `python3 crosscheck_k32.py --local xdir`、**149 checks / 0 failures**・rc=0（離脱検査なし・fetch時のblob検証も全pin一致）。ネットワークmode（jsdelivr/raw fallback）も選択可能。
- **二重実行 byte-identical**（run log sha256 `73d4bf05cd2297c230b6345ea849528b348c1427e8e036b14d0dfc3a2b0cc9c9`・両ラン完全一致）。
- 計算量: quint層 C(26..32,5) 合計 ~780k・sextet層 C(29..32,6) 合計 ~2.77M・その他の組合せ走査を含め純Pythonで1実行数分以内。
- grand total = 2,966,450,341,680,481,356（全点恒等不变）・kill(32)% = 86.0084。

## 運用メモ

1. 今回の拡張はk31拡張（crosscheck-k31-sextet-preread-layers）と同型だが、**prereadの大整数がNode丸めerratum対象外（純Python正確整数）である初のrank**であり、「erratum近似検証」ではなく「正確整数恒等検証」を実装した。以後のpreread（k33・k34も純Python化済み）は同じ型で拡張可能。
2. regression block helper（`regression_block_ok`）はrank-33+のpreread回帰blockにもそのまま流用可能な引数化（idx渡し）にした。

## 次段（次回レーン候補）

k33本計算（preread出版済: blob `e4346ddd…`・commit `67068e07`・rank-33 (7,19)・m33 = 120,083,817,332,086,665）着手前に必ず最新mainで「k33本計算の出版有無」を確認する。k34 prereadも出版済み（blob `8dbb1bcb…`〔commit `2a14f351`〕・rank-34 (9,19)・m34 = 120,079,520,746,539,458）。

## 11×11 状態（interpretation guard）

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。本crosscheckの全checkはcover-plan組合せ数とその構造の検証であり、verdictを一切生成しない。REFUTED-D10・STERILE は LOSS 証明ではない。
