# 2026-11-18 N11 検証側amendment: cost-16 shared-memo出版のcensus入力pin splice修正とhead-1476最小cover計数の訂正注記

## 背景

セッション開始時のmainは `45b1266f186cf1b8ea6d78047f2cc20ca6ea35c8`。AGENTS.md、research/knowledge/README.md、head-1476 parent census・class-2 cover・rank-1再照合・cost-16 phase A/B（shared-memo crosscheck出版 `5bdc86f1`/`1bcd4658`/`cef2ef40`/`45b1266f`）を確認した。

## 発見1: cost-16 shared-memo crosscheck出版のcensus入力pin欠陥（reproducibility blocker・数値への影響なし）

並走が出版した `crosscheck_cost16_parent_shared_memo_20261118.py` のcensus入力pinは `9c251da3138c5cb0516e097be5e5d35ab4f26a5d` だった。このSHA-1はrepo内のどのファイルのblobとも一致しない。機械的に特定した結果、**K0865 censusファイル（`n11-head1410-receipt-unclosability-census-20261116.json`）のblob SHA-1 `9c251da3138c5cb0516e097be5e5d0427dfaf5f0` の先頭29文字と、K0863 knowledge item（`K0863-sterile-row-depth10-unclosability.md`）のblob SHA-1 `c2ae353cab4a7dbcd28ec53b0f57d35ab4f26a5d` の末尾11文字のsplice** である。censusファイルはmain上で単一コミット履歴（`5ada304a`）で不変であり、正pinは全ての既刊レーン出版物（`count_minimum_cover_root_membership_20261118.py` 等）が同じ値を用いている。

出版scriptはこの誤pinのままではrepo checkout上でcensus pin検証により中断する。残り4入力（worklist/ledger/cover/phase_a）のpinは全て正しい。

対応:

- `crosscheck_cost16_parent_shared_memo_20261118.py` のcensus pinを正値へin-place修正（repo慣行のpin in-place修正に従う）。
- 出版済みoutput JSON `cost16-shared-memo-crosscheck-20261118.json` にadditive amendment `amendment_20261118_census_pin_correction` を追加（元fieldは全てverbatim保存・textual insert）。A16/B16/totalの数値は不変（checkpoint `d2901d15` とも一致しており、pin欠陥は転写上の問題のみ）。

## 発見2: head-1476 census recordの `all_minimum_cover_sets: 337020` ラベル誤りの伝播継続

検証側の既刊クロスチェック（`crosscheck-head1476-parent-census-and-class2-cover-20261118.json`・blob `fdee94df`・finding F1）で確定済みの計数誤り（分割型のみ計上・重なり型22,590の取りこぼし・正しい総数は359,610）が、本日のcost-16 shared-memo logでも「最小6 root cover 337,020通り」として引用され続けている。record本体（`head1476-parent-census-and-class2-cover-20261118.json`）がSSOTとして337,020のままなので、利用点で修正が見えない構造になっていた。

cost76c amendment（`c4ab2189`）と同一の手続きで、検証側がrecordにadditive amendment `amendment_20261118_minimum_cover_count` を追加した（corrected_total 359,610 = 337,020 + 22,590・minimum size 6と計画は不変・元fieldは全てverbatim保存）。あわせて、head-1476 recordを入力pinしている3つの既刊script（`count_minimum_cover_root_membership` / `analyze_minimum_cover_elimination_structure` / `crosscheck_head1476_census_and_class2_cover`）のpinをamendment後blobへ更新した（additive amendmentなので両scriptの意味論は不変）。

## 検証（verify_cost16_pin_and_mincover_amendments_20261118.py・30 checks all PASS・二重実行byte-identical）

- census入力ファイルの実blob == 正pin（`9c251da3…0427dfaf5f0`）かつ splice pinと不一致。
- splice分解の機械検証: spliced == census_blob[:29] + k0863_item_blob[29:]。
- 両amendment recordについて、amendment block除去で**前状態をbyte-exactに再構成**し元blob（`8e870809` / `b70689ea`）でpin検証、全非amendment fieldのdeep-equal、amendment値の照合。
- 修正scriptの全5 pinが実ファイルblobと一致（census正pin 1回・splice 0回）。3 repin scriptがamendment後blobを1回ずつ持ち旧blobを保持しない。
- **11行class-2 coverの独立再計算**: pinned worklist/census/ledgerからD4親包含で11行を再抽出し（11行・806候補・757 root・被覆ヒストグラム708/49）、重み付きperfect matching計数で分割型 A=337,020・重なり型 B=22,590・総数 359,610 を再現。per-row singleton pm（11値）が出版membership outputのways10と11/11一致。

## 成果物

- amended: `head1476-parent-census-and-class2-cover-20261118.json`（blob `28a0993d7192e599a95ab93becb5dc0d983a8d35`・pre-amendment `8e870809`）
- amended: `cost16-shared-memo-crosscheck-20261118.json`（blob `41d37ed863a85c8a9bdadaf0f39bb6d1a452c60d`・pre-amendment `b70689ea`）
- fixed: `crosscheck_cost16_parent_shared_memo_20261118.py`（blob `e5a47f7a10354add46ab9577358e1fb98bd81e51`）
- repinned: `count_minimum_cover_root_membership_20261118.py`（`b8e378c7`）・`analyze_minimum_cover_elimination_structure_20261118.py`（`fa810590`）・`crosscheck_head1476_census_and_class2_cover_20261118.py`（`c6ebb06c`）
- verifier: `verify_cost16_pin_and_mincover_amendments_20261118.py`、output `cost16-pin-and-mincover-amendments-verification-20261118.json`（blob `c2ee6224363bea018127cf46d4bfcbccb915a974`・sha256 `94e8fc8ecfb4e0f5824584e4a9d29aea77c5b85fd8167688a7a70d11de5a47e8`）

## 解釈境界

有限の簿記・組合せ検証のみ。engine実行なし・verdictなし・S5 parentの閉鎖なし。amendmentはpin転写欠陥の修正とcover計数ラベルの注記であり、いかなるゲーム理論的値も変えていない。REFUTED-D10とSTERILEはLOSS証明ではない。

標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべて**UNKNOWN**のまま。
