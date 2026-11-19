# 2026-11-19 N11 cost-16 crosscheck: k=33対応拡張 — 値・構造・record・preread の全層で +26 checks（175 checks all pass・二重実行byte-identical・7,542 recordsの新record層・rank-33 prereadの機械再導入に加えてrank-32回帰欄×出版k32主計算の3系統比較を初めて閉結合）

k=33本計算出版（script+log `7ef6dcfd`・result JSON `b7ec3ebd`〔blob `3446e9a0aec2d4cc01cbb8f062db0a36d660a65a`〕・record JSONL `410008a3`〔blob `594ff7882931dc8535b892db4006920e66519b1e`〕・52 checks all pass）を受けて、検証サイドの総合crosscheck script `cost16_survival_k13_k14_crosscheck_20261118.py` を k=33 対応に拡張した（拡張版 72,989B・blob `c1fb83ef137669b411277e2f0a390a1fbb8ccc68`・sha256 `89bd198ab8a4eee5aacb49b814a1ef35b8d876e403c40e70cfff47fb7f31c579`・実験script importなし・純粋標準ライブラリ・k32版〔blob `2e139fb0…`〕からの機械変換はアンカー付き全置換・着地後にbackupからの再適用でbyte-identicalを確認）。**生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。**

## 拡張内容（旧版149 checks → 175 checks all pass）

1. **値層（既存checkのk=33への拡張）**: 参照JSONを k33 result JSON（pinned blob `3446e9a0…`）に切り替え、grand-total恒等・単調性（kill/A/B）・marginal chain k2..k33（出版 `survival.marginal` detail の `k33_minus_k32` = 27,118,636,261,489,686・`m33` = 120,083,817,332,086,665 と照合）・A/B分割恒等・reproduce anchors k16..k33（`reproduce_k1_32`）・cross-publication系列一致 k13..k33 が全て k33 点まで通る。kill(33) = 2,578,514,354,033,082,917（86.9226%）。
2. **構造層の機械再導入の拡張**: rank_root_fields（rank33_root (7,19)・root hex `00000000000000801302020000001000`・A/B分割正確整数 92,100,657,745,931,553 / 27,983,159,586,155,112）・新pair census 9 shared / 23 disjoint・full triple census C(33,3)=5,456 = 3,296/1,047/1,113・新quad census 1,827/2,987/146 がpinned aggregateから独立再導出で一致。**quint census層**: C(33,5)=237,336 = 10,833 b_only / 226,503 zero / 0 disjoint・二重行hist {15:1,930, 16:370, 18:6,008, 19:2,525}（行7不参加）・`quints_zero_synth_count` 33,924 = C(32,4) − 2,036・prev-layer恒等 10,833 = 8,797 + 2,036。**sextet census**: C(33,6)=1,107,568 all zero の独立再導入（I-E quint打ち切り10連続の機械保証を更新・行7の初二重化でも全zero维持）。
3. **record層（新規+11 checks）**: k33 JSONL（blob `594ff788…`）の 7,542 records 全件を独立分類器で再分類: kind別計数（pair 32 + triple 496 + quad 4,960 + quint 2,036 + anchor2 4 + anchor3 2 + anchor4 4 + cross 8 = 7,542）・anchor/cross全match・anchor4両lineage一致（k32 record層の disjoint quads (2,4,28,31)/(2,5,28,31) に再錨付け）・新pair/triple/quadの組合せ完全性・新b_only quint集合が classify2 による機械再導出集合と一致・quad record census一致・**I-E marginal恒等式（total/A/B 3本）**: m33 − Σ新j2 + Σ新j3 − Σ新j4 + Σ新j5B = 27,118,636,261,489,686 = kill(33) − kill(32) が record joints のみからの再加算で厳密成立（Σ新j2 = 122,125,381,349,233,614〔m33の101.7001%〕・Σ新j3 = 31,031,267,107,765,449・Σ新j4 = 1,886,166,450,105,609・Σ新j5B = 15,099,620,976,795。A型: −Σs4A含む、B型: +Σs5B含む。新pair disjoint 23本・平均joint 5,282,128,458,074,969 でdisjoint-partner法則の10回目連続的中も再確認）。
4. **preread層6（k=33・新規+11 checks）**: k33 preread JSON（commit `67068e07`・blob `e4346ddd7e08799b4406dcdba930de714e4f462c`・純Python正確整数）を機械再導入: (i) rank33 root (7,19)・行7のprior hit indices {[20]}（単一sharer）・行19の {[0,2,3,8,9,10,15,29]}（8 sharer）・membership/A/Bがaggregate正確整数と厳密一致し A+B==M 成立。(ii) 新層census 4種（pairは shared/disjoint schema・triple 304/67/125・quad 1,827/2,987/146・quint 2,036/33,924/0）。(iii) 新層b_only二重行hist 3種（tripleは行7が初参加8 record・quadは行7が11 record・quintは行7完全排除の {15:314, 16:66, 18:897, 19:759}=和2,036）。(iv) b_only quintの4-subset profile {3/2/0: 2,036}・disjoint quad 146本全てunionサイズ8・**累積966 = 機械再導出820（C(32,4)全走査）+146（新層）の追加恒等（ハードコード定数なし）**。(v) full triples（C(33,3)=5,456 counts+二重行hist）・full quints（==キャッシュ済quint機械census）・sextet（1,107,568 all zero）。(vi) rank-31/rank-32両回帰block（new_census 4層・3種hist・full_triples+hist・full_quints・sextet）の統一helper `regression_block_ok` による機械再導入。(vii) **3系統比較の閉結合（このrankで初めて可能に）**: prereadのrank-32回帰blockを、出版済みの k32 result JSON structure（root/rows・triple_census_k32・new_quad_census・quint_census_k32・二重行hist・sextet_census_k32・rank32_root大整数）とfield-by-fieldで直接照合。preread出版時点ではk32主計算が未出版のためk32 preread JSON比対しかできなかった回帰欄が、出版k32主計算と初めて直接接続した（k33preread_rank32_regression_matches_published_k32_result）。(viii) k33 result JSON側の preread_match.* 5 checkの存在・PASS・rank33_rootの正確整数。

## 実行と検証

- 実行: `--local xdir`（全31ピン取得・fetch時blob検証全pin一致）**175 checks / 0 failures**・rc=0・約6.5s/回。ネットワークmode（jsdelivr/raw fallback）も10.3s/回で同一出力。
- **二重実行 byte-identical**（local・network両モード・run log sha256 `2e8a1db349d199247ce6db415fd631da7d31b61552c874ff576d9301e7eb3f93`・4走査全て完全一致）。
- 計算量: quint層 C(26..33,5) 合計 ~1.01M・sextet層 C(29..33,6) 合計 ~3.88M・record層 7,542再分類込み、全て純Pythonで1実行10秒程度。
- grand total = 2,966,450,341,680,481,356（全点恒等不变）・kill(33)% = 86.9226。

## 運用メモ

1. 機械変換はk32拡張版（blob `2e139fb0…`）をbaseに、アンカー付き置換26件（全件count assertion）で適用し、出版後にbackup再適用でbyte-identicalを確認した。`regression_block_ok` helperはrank-34+のpreread回帰blockにもそのまま流用可能。
2. k33のfull triple二重行histは {15,16,18,19} 族に加え rank-32/33 root由来の行23・行7系と低行（1,4,5,11,14,24,30等）の既存二重化が増え、機械再導出histは出版欄と完全一致（新規の族不変・既存構造の再確認）。

## 次段（次回レーン候補）

k34本計算（preread出版済: script blob `be46c300`・JSON blob `8dbb1bcb`〔commit `2a14f351`〕・rank-34 (9,19)・m34 = 120,079,520,746,539,458）着手前に必ず最新mainで「k34本計算の出版有無」を確認する。k34本計算出版後は本crosscheckへrecord層+preread層7（rank34+rank33/32回帰・k33prereadのrank-33回帰欄はk33主計算出版済みのため3系統閉結合は rank-34 preread で初回から可能）を追加。

## 11×11 状態（interpretation guard）

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。本crosscheckの全checkはcover-plan組合せ数とその構造の検証であり、verdictを一切生成しない。REFUTED-D10・STERILE は LOSS 証明ではない。
