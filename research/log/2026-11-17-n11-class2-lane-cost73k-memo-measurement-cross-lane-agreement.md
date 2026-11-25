# 2026-11-17：cost73kメモ容量測定のcross-lane合意照合（重複出版検出からagreement checkへの転換）

## 開始時点

開始時のmainは `1da42ce0` を起点に確認し、最新main・`AGENTS.md`・`research/knowledge/README.md`・cost73k関連のknowledge・experiments・logを読んだ。前回実行のlong-termレーンはcost73kバンドのメモ容量・band-wide共有測定を完了寸前まで走らせたが環境リセットでワークスペースごと喪失しており、測定値だけがknowledgeに退避されていた。今回の実行は、(1) pubtestをrepo raw CDN pin `1da42ce0` から再構築し、(2) orchestratorを最初から再実行し、(3) knowledge退避値との完全一致を機械ゲートで検証する、という再現実験として実施した。

## 実行と、実行中の失敗（実験事実）

入力はすべて公開pinから取得しGit blob SHA-1で検証した（extractor `52bcaf509ea12fad4c936501d30d26b5b66c0085`、manifest `0892aed07d187ae2fb3b4b90a21c7adbc1002b62`、`legal_candidates.py` `8e97082c42838c7a4a4b6d2dd235276c8d43ab9a`、73k証明書41ファイルは結合md5をmanifestと22/22照合）。driverは本レーンで独立に実装したplan駆動版（出版済みの `measure_band_memo_extraction_73k.ts` とは別実装・同一engine pin）である。

- 初回orchestrator起動: band ms18（205,129,712ノード）は完走したが、band ms22が `ERR_MODULE_NOT_FOUND` で即失敗した。原因はorchestratorの `run_driver` がdriver変種のimport先となるengine変種（ms22/20/21/24）を未生成のまま起動していたこと。`run_driver` 冒頭への `make_variant(ms_shift)` 追加で修正し再起動した。band ms18の成果物はresume機構で再計算なく再利用され、以降のstepはすべて一度で完走した（計約50分、FAILURES: 0、全ゲート合格）。
- 2回目の通し実行: 全stepをresumeで再検証し、JSONは `resumed` / `wall_s` の実行時フィールド以外同一であることを確認した。

測定値そのもの（band ms18/22/23/24 = 205,129,712 / 142,171,197 / 121,186,659 / 106,861,135、fresh ms23 = 108,499,241〔-30.4%〕、fresh ms24 = 105,117,037〔-32.6%〕、band/fresh比 +11.69%〔load 0.85〕→ +1.66%〔load 0.64〕、bit117感度 6容量、bit95の全構成不変 11,857,737、union 682,861行/966,535〔70.6% distinct・md5 `2133564406306fd1657af7ac11be6f5d`〕、証明書bytes 132スナップショット全部byte-identical）は、本レーンの独立実装・独立実行による実測として確定した。

## 重複出版の検出とagreement checkへの転換

push直前の最新main再取得で、**並走セッションが同一測定を出版済み**だと判明した（commit `a3c27e9f` 05:55:55Z「n11 class2-lane cost73k: band memo extraction capacity measurement (fresh ms24 -32.6%...)」＋ `c170a4ef` prose修正）。本レーンが出版予定だった4パス（driver・orchestrator・測定JSON・log）はすべて並走出版と同名・同内容であり、重複出版は禁止（73j先例・73k claim事故の処置踏襲）のため出版を取りやめた。

代わりに、先例（`check_cost73j_reverification_cross_lane_agreement_20261117.py`、K0900 r=12 cross-lane agreement）に従い、**本セッションの独立再実行が出版済み測定と全数値で一致することを機械照合する記録**を出版することにした。2セッションの独立性は以下のとおり: 別セッション・別実行、2セッション目（本レーン）は環境リセット後にraw CDN pinからpubtest環境を再構築、orchestratorは別実装（同一engine pin）、構成ごとにfresh Node.jsプロセスで実行。

## 合意照合の内容（259項目・全一致）

`check_cost73k_memo_measurement_cross_lane_agreement_20261117.py` は、出版済み測定JSON（pin commit `a3c27e9f`、git blob `ce625db014e0269fad48c573d29389e6f803310b`）をraw CDNから取得しblob検証した上で、本セッションの再実行値（定数埋め込み）とフィールド単位で照合する。結果は **259/259 checks ok、verdict AGREEMENT**:

- baseline総ノード 155,946,109
- band-wide 4構成（ms18/22/23/24）の総ノード・最終occupied・byte-identity（22/22）・per-bit 22ノードずつ（88値）
- fresh ms23電池: 総ノード・vs_published・per-bit 22値、fresh ms24電池: status・総ノード・per-bit 22値
- ms23 sharing分解（band/fresh総ノード・penalty・per-bit band/fresh 44値）、ms24 band-vs-fresh（penalty +1.66%、load 64.4%、per-bit ratio 22値）
- bit117感度6容量（slots・nodes）、gates（failures []・all_expected_values_reproduced true）
- 派生値（vs_published、penalty、load、per-bit ratio）は本セッションの生の整数から再計算して出版側の丸め値と一致

すなわち、**並走が出版した測定の数値はすべて、本セッションの環境再構築からの独立実行で再現された**。特に並走出版で新規だった値（fresh ms24電池、band ms24、sensitivity ms20/21/22/24、per-bit sharing ratio）も含めて二重検証された。

**転写ミスの検出（実験事実として記録）**: 本checkerの定数表は当初、fresh ms24のper-bit 22値を手書きで転記したところ、初回実行で36項目の不一致（verdict DISAGREEMENT）が出た。原因は手書き定数の混線で、機械抽出（実測JSONからの `per_bit[].nodes` 抽出）に置き換えたところ259/259一致に変わった。合計値は偶然一致していたため合計だけの検証では検出できなかった種類の誤りであり、per-bit全数比較と機械抽出の両方が効いた事例として記録する。この経緲により、checkerは「定数転写ミスがあればDISAGREEMENTを返す」ことを実際に一度発動済みである。

## 出版物

- `scripts/check_cost73k_memo_measurement_cross_lane_agreement_20261117.py`: 合意照合checker。pin blob検証・259項目機械比較・verdict AGREE/Disagree・agreement JSON書き出し。デフォルトでraw CDN pinから出版JSONを取得する。
- `output/class2-lane-cost73k-memo-measurement-cross-lane-agreement-20261117.json`: 照合結果（259/259 ok、mismatches []、verdict AGREEMENT、本セッションのみの追加計測〔union・bit95・bit39 anchor・実行中失敗記録〕も記録）。

本レーンが再実行に使ったdriver/orchestrator/測定JSON/logの4ファイルは並走出版と同名パスのため出版しない（重複出版の禁止）。本レーンの実測値は上記checkerの定数表とagreement JSONに取り込まれている。

## 解釈と次の作業

この合意照合は**測定の再現性**の記録であり、新しい探索verdictは1つも作っておらず、manifestの行は1行も閉じておらず、証明書bytesも1バイトも変わっていない。73k receipt foldは76c/66i/66j/69j/71e/72d/73i folds完了まで並走管理のまま着手禁止。73i証明書は並走がclaim（`batches_run: 0`）のままsweep中であり、出版後に72d/73jパターンのBigInt bytes再検証が本レーンの次候補のまま変わらない。

WIN7-D10は個別7石rootの深さ10以内の先手勝ちであり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続きUNKNOWN。
