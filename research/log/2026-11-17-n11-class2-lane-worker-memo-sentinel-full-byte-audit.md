# 2026-11-17 n11 class2-lane: worker memo sentinel comparisonの全byte域監査

## Context

最新 main は `23de976b618b3a22f0c41440689e6000558578a8`。
`AGENTS.md`、`research/knowledge/README.md`、K0023、K0863、K0868、K0907、K0909、およびcost73lのBigInt独立再検証ログを確認した。

K0909の境界保存4-worker測定では、worker間memo mergeの `255` を「boundなし」として扱う。一方、seed表と最終dumpの比較条件には、負境界の有限値が最終側で `255` に戻った場合も数値比較上は通ってしまう余地があった。今回のmain commit `23de976b` は `bound_at_least` を導入し、この意味を修正していた。

## 修正の意味

`255` は「深さ255の境界」ではなく「境界が存在しない」印である。したがって、seed側が `255` なら要求なしとして通すが、seed側が有限値で最終側が `255` なら、要求した情報が失われているため不合格にしなければならない。

正しい条件は次のとおり。

- required == 255: 条件なし（PASS）
- required が有限、value == 255: 要求境界が欠落（FAIL）
- 両方有限: value >= required のときだけPASS

これはmergeの `max_bound`（255を単位元とする有限値の最大）とは別の判定であり、比較時にsentinelを通常の整数として扱わないことが要点である。

## 実施

1. `worker_memo_merge.py`（blob `fe2c5411393f789757b6e9a85d1f3925d6d260bc`）と、更新後の `test_worker_memo_merge_sentinel_20261117.py`（blob `f2102728756f6af3cf1720bcd69ac4ecec9b608a`）をmainから取得。
2. 両ファイルを隔離実行環境の `/tmp` にバイト単位で配置し、`git hash-object` が上記blob SHAと完全一致することを確認。
3. 単体試験の対象を従来の0..64と255から、全byte値0..255へ拡張。有限値0..254すべてについて255の単位元性も確認。
4. Python 3.13.5で更新済みテストファイルを実行。

## 結果

- 7/7 tests PASS。
- `max_bound` の全256値に対する組合せ65,536件で可換性・冪等性・参照定義一致を確認。
- 全256^3 = 16,777,216組で結合性を確認。
- `bound_at_least` の全256^2 = 65,536組を参照定義と照合。
- 有限負境界0..254の全255値で255との左右両順の単位元性を確認。
- worker間のwin/nowin・lose/nolose矛盾検出、F5の有限負境界保持、既存verbatim値の不変性もPASS。
- 実行時間14.99秒、最大RSS 96,272 KiB。
- machine-readable結果: `output/worker-memo-merge-sentinel-domain-audit-20261117.json`。

## 境界・解釈

今回の単体試験は、取得したGit blobと完全一致するコピーを隔離環境で実行したもの。repo checkout上の `unittest discover` や全knowledge検査を実行したとは主張しない。また、巨大な4-worker測定自体は再実行していない。

K0909の実測verbatim engineではnowin/noloseが全レコード255であるため、今回の修正は既存の自然測定値・証明書bytes・勝敗verdictを変更しない。有限負境界を含む将来のcache/seed比較に対する検査の健全性を強めるもの。

新規WIN/LOSS verdictなし、証明書bytes変更なし、manifest行の開閉なし。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はすべてUNKNOWNのまま。

## 反映

- test拡張 commit: `d305c3d5034e60741b3e49c1a55fd39d9f87523e`
- machine-readable audit commit: `7222f51100d0ef0731f403ab44e5530b2d03f832`
- branch / PRなし。
