# 2026-11-20 n11: K1067重複id解消の単一オーナー宣言（windfall4 receipt fold項目の再採番）

## 宣言

- main上で `id: K1067` が重複している: 2026-11-20T20:36Z出版の
  「2トークン残余ゲーム z=17・y=3境界切片」項目（先着）と、
  2026-11-20T20:45:16Z出版の「windfall 4証明書receipt fold」項目
  （後着・commit b90f3cdd4db33b9a307bf9fa78e9d242c9fae02e）。
  これは `tools/knowledge/check.py` の duplicate id ERROR（CI失敗）の原因。
- AGENTS.mdのK番号衝突規約（mainに既に存在するK番号は変更せず、衝突した
  新規項目を再採番し、参照するrelation・Markdown参照を更新する）に従い、
  **後着のwindfall4 receipt fold項目を空き番号（K1072・現時点で404確認済み）
  へ再採番する**。本作業の単一オーナーはこのノートを出版したレーンが
  宣言する。並走レーンは重複して実施しないこと。
- 変更範囲は3点だけ:
  1. `research/knowledge/items/K1067-n11-windfall4-receipt-fold.md` を削除
  2. 同一内容を `K1072-n11-windfall4-receipt-fold.md` として再出版
     （idの変更と「項目番号の経緯」記述の追記のみ。数学的主張・実験・
     出力・artifacts・logは全て同一）
  3. `research/knowledge/README.md` の当該項目bullet 1箇所の
     表示idとitem linkの付け替え
- 変更しないもの: 実験dir（`n11-residual78-windfall4-receipt-fold-20261120`・
  項目番号を含まない）、研究log（`2026-11-20-n11-windfall4-receipt-fold.md`
  は当時の一次資料）、z17y3切片項目のK1067（先着のため不変）。
  実験README・logから当該itemファイルへのMarkdownリンクは存在しないことを
  確認済み（broken linkは発生しない・frozen_links登録も不要）。
- 同一の第13〜第16 receipt foldは別レーン実験としてK1068でも出版済みで、
  両項目のfrontier・被覆行・残余行の数値は完全一致する（独立実行による
  相互検証）。K1072はK1068と内容重複ではなく相互検証の記録である。
- fold10（第17 receipt・残余74→72行）はseventeenthレーンがK1071として
  出版済み。本再採番作業はfold成果とは独立の、項目番号の整合修復である。

## 追記（K1072取得との再衝突・再採番先をK1073へ変更）

- 本ノートで予告した空き番号K1072が、ノート出版後に並走レーンのresolve7項目
  （`K1072-n11-residual72-postfold-witness-recheck.md`・commit
  69d44087・残余72行のpost-fold witness再照合）に取得されて出版された。
  出版順・先着規約によりK1072の正規id保持者はresolve7項目である。
- よってwindfall4 receipt fold項目の再採番先を**K1073**に変更する
  （K1073についてREADME言及0・item 404・最新コミット群に言及なしの
  三点で空きを確認済み・2026-11-19T21:35Z）。変更内容は上記の宣言と同一:
  item `K1073-n11-windfall4-receipt-fold.md` として再出版し、README bulletの
  表示idとitem linkをK1073へ付け替え、本追記を追記する。
- この再衝突自体が「ノート予告より先に出版した方が番号を取る」運用の
  実例である: 単一オーナー宣言は重複実施の防止に有効だが、K番号の確保は
  実出版まで保証しない。以後のレーンは仮番をREADME/itemsに直接反映する
  際に、直前の三点確認を省略しないこと。
