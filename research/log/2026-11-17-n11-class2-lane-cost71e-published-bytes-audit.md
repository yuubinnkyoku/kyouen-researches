# 2026-11-17：cost71eの13証明書を公開元から再取得し、全バイトを照合

## 起点と対象

監査時の最新 main は `a8ff1d814a64565491a8527a7489b97952ec9514`。作業前に `AGENTS.md`、`research/knowledge/README.md`、K0023・K0863・K0865・K0868、およびcost71eのclaim・certificate manifest・完了ログを確認した。

対象は cost71e の13本のWIN7-D10証明書。正本manifestは `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71e-certificates/class2-lane-cost71e-win7-certificates-20261117.json`（Git blob `a9ddec439e1931614679c2575e4adeb5fe770d2b`）。manifest記録は534,804行、抽出141,067,035節点、公開19,300,105 bytes。

## 方法

GitHub Contents APIとは別経路で、source commit `a8ff1d814a64565491a8527a7489b97952ec9514` の raw.githubusercontent.com から全データを再取得した。低負荷のリモートコンテナで `wget`・`wc -c`・`sha256sum`・`md5sum` を使用。分割10証明書はpart1of2→part2of2の順に連結し、各partのサイズと連結後の全体サイズ・SHA-256・MD5をmanifest値と照合した。単一ファイル3本も同じ全体照合を行った。取得物は一時領域に置き、実行後に削除した。

## 結果

- 13/13証明書で全体サイズ・SHA-256・MD5が一致。
- 分割20 partのサイズも20/20一致。
- whole 3本 + split 20 part = 23公開オブジェクト。
- 連結後の合計は19,300,105 bytesでmanifest総量と一致。
- 不一致0、取得失敗0。

bit別のサイズ・ハッシュは出力JSONに保存した。再現用shell scriptは同じcommit pin・期待値で再取得と照合を行う。

## 追加観察と境界

GitHub Contents APIの `fetch_file` はbit58の1,178,240-byte whole fileで本文を返さずblob SHAだけを返した。Git blob取得とraw CDN再取得で内容を回収でき、raw CDN上のSHA-256/MD5はmanifestと一致した。これは取得経路のサイズ制限であり、公開データの欠損ではない。

この監査は公開バイト列の完全性だけを確認する。証明書の意味的な正しさを再検証したものではない（各rootの独立検証はcost71e完了ログの既存記録）。receipt fold・frontier・勝敗判定は変更していない。main上ではcost72dの新規sweepが27/67 open bitsまで進んでいたが、本監査はその探索結果を利用・変更していない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。
