# 2026-11-19 N11 cost-16 crosscheck: k34版scriptの輸送欠損修理 + k=34→k=35対応拡張 — 修復版で出版203-check結果JSONとbyte-identical再現を初回で実証・k35拡張は28新規check込み231 checks all pass・二重実行byte-identical・rank-35 prereadの機械再導入とrecord 8,192件再錨付け・rank-34回帰欄×出版k34主計算の3系統閉結合（前回log「次段」どおり）

k=34 crosscheck 203 checks版（script commit `2331d99e`〔拡張版 87,336B・commit `d70014678` に2 closure check追記〕・機械可読結果 commit `236140cc8e`〔blob `2eb1fa8b8b46c34112589543509079fd429e070f`〕）と k=35本計算出版一式（script+log `141da801`・erratum `bde016c4`・result JSON `572b1365`〔blob `80a22ac77cdc0ba0a99643e3f1be13b71565a1b7`〕・record JSONL `b1c73b50`〔blob `89c15ec4fea859393dd673acde1654435f85bd01`〕・rank-35 preread `90fc51c991`〔blob `490fa3a00b8e0b19229c94aa6b1aba4a5604ec13`〕・preread第二系統検証 `41c4cf12b`）を受けて、crosscheck scriptの k=35対応拡張（record層9段目 + preread層8 + closure 2件）を行った。**その前に、main上のcrosscheck script本体が輸送欠損で破損していることを発見したため、修理を拡張と同コミットで反映した。** **生存曲線はban回避の代替最小cover計画の組合せ数であって、探索コストでもverdictでもない。標準11×11空盤はUNKNOWNのまま。**

## 修理（transport-truncated tail修復）

1. **破損の発見**: main上の `cost16_survival_k13_k14_crosscheck_20261118.py`（commit `2331d99e` 時点・91,614B・blob `49606fc61005f9c8652fbda4985e542f5e7ffe95`）は末尾が `if __name__ == "__main` の途中で切断しており、`sys.exit(main())` が欠落。手元で `py_compile` が SyntaxError で失敗することを確認済み。
2. **出版logとの突合作証**: k34 crosscheck log（`2026-11-19-n11-cost16-crosscheck-k34.md`）は拡張scriptを「91,614 bytes・blob `49606fc6…`・SHA-256 `4610d76c…`」と記録している。91,614B/blobはmainに着地した破損版そのものである一方、SHA-256 `4610d76c…` は出版者の意図した完全版（91,640B）の値である。切断で失われた末尾26 byte `__":` + 改行 + 4空白 + `sys.exit(main())` + 改行 を復元すると91,640Bとなり、**SHA-256がlog記載の `4610d76c…` と厳密一致する**（欠損はpush時の輸送切断、意図した内容は失われていなかったことの機械的裏付け）。
3. **修理の実証**: 修復版（`/tmp/cc_fixed.py` 91,640B・sha256 `4610d76c4dd56a2a5bd56973c941138384cbd6ccba2cbdaf5ebf3431637b80b7`）を `--local`（pinned入力全件・sha1検証込み）で実行し、**203 checks / 0 failures・rc=0、出版済み結果JSON（commit `236140cc8e`・45,185B・sha256 `9dde9f8a…`）とbyte-identical**であることを確認した。出版時の実行環境（network mode・別lineage）で生成されたJSONが、修復版script・別環境・`--local`入力で正確に再現されることで、(a) 修理がbyte単位で正確、(b) crosscheck出力の決定性が追加実証された。

## k=35拡張（203 checks → 231 checks all pass・28新規check）

機械変換は修復版（91,640B・203 checks）を起点に、アンカー付きrep 24件（全件単一出現count assertion・不一致は即時abort）+ 大型insert 3件（docstring layer 8 section・preread層8コード・closure 2件）で適用。主な変更: PINSにk35（`80a22ac7…`）・k35pre（`490fa3a0…`）追加・`JSONL_K35` 定数（blob `89c15ec4…`・anchor4はk34 record層のdisjoint quads (4,13,25,33)/(4,16,25,33) に再錨付け）・値層の参照JSONをk35 resultに切替（K=35・kill系列k1..35）・quint census loop・prev-layer恒等式・sextet census loopへの35追加・record層loopへ (35, JSONL_K35, 2) 追加・preread層8（rank35 + rank-33/rank-34回帰block）新設・closure 2件のk35版追加・reportのschema/出力名/source_main_commit差し替え（`a2814ea0f1f802df1cff0fed86950d5ee0358dba` + source_note）。

1. **値層（k35参照・範囲拡張15件改名）**: grand-total恒等・単調性（kill/A/B）・marginal chain k2..k35（出版 `survival.marginal` の `k35_minus_k34` = 43,277,955,991,896,150・`m35` = 120,058,481,266,728,720 と照合）・A/B分割恒等・reproduce anchors（`reproduce_k1_34`）・cross-publication系列一致 k13..k35 が全て k35 点まで通る。kill(35) = 2,649,081,198,429,349,007（89.3014%）。
2. **構造層（+4 check）**: quint census C(35,5)=324,632 = 14,599 b_only / 310,033 zero / 0 disjoint の独立再導入（二重行hist {15:2421, 16:469, 18:8017, 19:3692}・`quints_zero_synth_count` 44,781 = C(34,4) − 1,595）・prev-layer恒等（14,599 = 13,004 + 1,595）・sextet C(35,6)=1,623,160 all zero（I-E quint打ち切り12連続の機械保証・行21の初被覆〔fresh row〕はいかなる層でも二重行化しない構造事実の再導入込み）。
3. **record層k=35（+10 check）**: k35 JSONL（blob `89c15ec4…`）の 8,192 records 全件を独立分類器で再分類: kind計数（pair 34 + triple 561 + quad 5,984 + quint 1,595 + anchor2 4 + anchor3 2 + anchor4 4 + cross 8 = 8,192）・anchor/cross全match・anchor4両lineage一致（k34 record層disjoint quads再錨付け・union rows再導出込み）・新layer組合せ完全性・新b_only quint集合一致（1,595）・quad record census一致・**I-E marginal恒等式（total/A/B 3本）**: m35 − Σ新j2 + Σ新j3 − Σ新j4 + Σ新j5B = 43,277,955,991,896,150 = kill(35) − kill(34) が record joints のみから厳密成立。
4. **preread層8（+11 check）**: rank-35 preread（blob `490fa3a0…`・純Python正確整数）を機械再導入: root (18,21)・行18 prior hits {[1,4,5,6,7,11,12,18,19,20,21,23,24,26,27,30]}（16 sharer）・行21 hits {[]}（zero prior sharers・初被覆）・membership/A/B = 120,058,481,266,728,720 / 92,036,253,749,417,268 / 28,022,227,517,311,452（A+B==M成立）・新層census 4種（pair 16 shared / 18 disjoint・triple 348/133/80・quad 1,612/4,289/83・quint 1,595/44,781/0）・新層二重行hist 3種（行21完全排除・行18主体）・b_only quint 4-subset profile {3/2/0: 1,595}・disjoint quad 83本全union=8・**累積1,195 = 機械再導出1,112（C(34,4)全走査）+ 83（ハードコード定数なし）**・full triples C(35,3)=6,545・full quints・sextet all zero・rank-33/rank-34両回帰block（`regression_block_ok` helper流用）・**3系統閉結合: preread内蔵rank-34回帰blockを出版済みk34 result JSON structureとfield-by-field直接照合**（preread自身のload時assert・k35主計算のpreread_match checks・本crosscheckの独立再導出という3系統が閉じる）・k35 result JSON側 preread_match.* 5 check存在/PASS・rank35_root正確整数一致。
5. **closure 2件（k35版・+2 check）**: `k35preread_embedded_rank33_rank34_blocks_match_prior_prereads`（k35 preread内蔵回帰欄を先行preread出版〔rank33→k33pre・rank34→k34pre〕とschema正規化比較）・`k35json_preread_structure_matches_published_result`（rank-35 preread全構造欄をk35本計算出版JSONのstructure欄と直接照合）。k34版2 closure checkはそのまま維持。

## 実行と検証

- 実行: `--local` mode（pinned入力全件fetch・sha1照合）で **231 checks / 0 failures**・rc=0。**二重実行 byte-identical**（result JSON 52,099B・blob `9e4989396d82b1890d6bd51bfe0b8dd0fdf70910`・sha256 `f4de97df76dd4c9704b1502ef793fea03dcd91d6c39fe13ced3fe1e2ffd073e9`）。約35s/回（sextet C(35,6)=1.62M件の独立再分類込み・純Python・1プロセス・CPU並列なし）。
- 拡張script: 109,615 bytes・blob `a2df5648038ea9b3cecfce6d52ca5f1f9f01e764`・sha256 `ee3032391085254a74923e6e06443b394ddc74e91edd0819ba49ed9086af7965`・`py_compile` PASS。
- 計算量: k34版の約3.6倍登上の構造再導出（quint ΣC(26..35,5) ≈ 1.72M・sextet ΣC(29..35,6) ≈ 5.72M・record層 8,192件×2回〔前段k34分+新規k35分〕・preread層8のrank-33/34回帰block機関再導入込み）。
- 機械可読結果: [cost16-k35-crosscheck-20261119.json](../experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/cost16-k35-crosscheck-20261119.json)・schema `n11-cost16-k35-crosscheck-20261119-v1`・source_main_commit `a2814ea0f1f802df1cff0fed86950d5ee0358dba`。
- 修理版によるk34結果再現は拡張版内包の prefix-compat 実行で別途確認（203 checks / byte-identical・上記「修理」節）。

## 運用メモ

1. **push時の輸送切断リスク**: 今回の破損はpush時の末尾欠損（26 byte）であり、k35 script出版時（`141da801`→`bde016c4`・trailing newline欠損）と同様の種類の輸送故障が3度目。**以後のscript pushでは着地後のraw CDN再fetch・blob/sha256照合・`py_compile` を必須手順とする**（本logの出版自体も同じ手順で着地確認する）。
2. 値層のk35参照切替に伴い、チェック名の範囲部分（`k16_k35_reproduce_anchors_all_pass` 等15件）は改名される。result JSONのcheck名集合はk34版の上位互換（範囲拡張を除き同一）。

## 次段（次回レーン候補）

- **k=36本計算**（並走がrank-36 prereadを出版済み: commit `67985e92c`・行22 first covered・33 checks all pass）。着手前に必ず最新mainで並走の進捗確認（k36本計算が出版済みならcrosscheck k=36拡張が本命）。
- crosscheck k=36拡張の設計は今回のpreread層8パターンの直接適用（PINS k36/k36pre + JSONL_K36 + record層 (36, …, 2) + preread層9〔rank36 + rank-34/rank-35回帰block〕+ closure 2件）。`regression_block_ok` はそのまま流用可能。

## 11×11 状態（interpretation guard）

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。本crosscheckの全checkはcover-plan組合せ数とその構造の検証であり、verdictを一切生成しない。kill(35) 89.30%・B_survive 2.09%台も「ban回避代替計画の組合せ論的飽和」の度量であって、探索進展や勝敗の尺度ではない。
