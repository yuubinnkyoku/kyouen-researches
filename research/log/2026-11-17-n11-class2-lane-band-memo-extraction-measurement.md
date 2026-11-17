# 2026-11-17：cost73jバンド抽出のメモ容量測定（band-wide vs fresh、MS感度）

## 開始時点

開始時のmainは `41544af1` を起点に確認し、最新main・`AGENTS.md`・`research/knowledge/README.md`・cost73j関連のknowledge・experiments・logを読んだ。cost73j（6石child `00000000000000403800000408000000`）は16 WIN7-D10証明書と57 REFUTED-D10・capped 0のsweepが出版済みで、証明書manifest（blob `e88710b5a2d4848be77a03ae5104e46aefc1279a`）にper-bitのroot・md5・rows・extraction_nodesが記録されている。

前回のstate-sharing測定で、band内の状態共有率は20-26%にとどまることが分かっていた。そこで今回の主眼は、抽出器 `class4_child1_cert_extractor_exact.ts`（blob `52bcaf509ea12fad4c936501d30d26b5b66c0085`）のプロセスグローバルメモ（MS=1<<18スロット、64-probe線形探査、鎖切れ時は格納スキップ/不在扱いで健全だが再計算を生む）の**容量**が抽出コストの支配因子かどうかを分離することである。

## 測定手順

入力はすべて公開pinから取得し、Git blob SHA-1で検証した（extractor `52bcaf50`、manifest `e88710b5`、`legal_candidates.py` `8e97082c`、公開証明書16本はmanifest md5とbyte-exact照合）。MS変種は `const MS=1<<18, MM=MS-1;` の1行置換のみで生成し、他の行が変わらないことをdifflib検証した。driver `measure_band_memo_extraction_73j.ts` はrepo-verbatim抽出器を無改変でimportし、per-bitのノード数を記録するだけである。

## 結果

| 実行 | 総ノード | baseline比 | union行 | fbt_drops |
|---|---:|---:|---:|---:|
| baseline（公開、fresh per-bit、MS=1<<18） | 166,238,087 | 1.000 | 547,910 | 0 |
| Run A：verbatim MS=1<<18、band全体1プロセス | 229,836,337 | **1.3826（+38.3%）** | 547,910（byte-equal） | 0 |
| Run B：MS=1<<24、band全体1プロセス | 94,005,413 | 0.5655（-43.5%） | 547,910（byte-equal） | 0 |
| 帰属バッテリ：MS=1<<24、16 bit各々freshプロセス | 91,941,958 | **0.5531（-44.7%）** | 547,910 | 0 |

- **フィデリティ**: Run Aのbit 0（band先頭、メモ空状態）は9,260,973ノード・46,463行で公開値と完全一致。fresh verbatim bit 98は25,505,012ノード・64,451行、行集合は公開証明書のデータ行とbyte-identical。
- **Run Aが逆効果の原因**: メモがbit 0の探索中に飽和し、以降のbitがintra-bitメモを喪失（per-bit比1.2445〜2.0505）。band全体を1プロセスで回すこと自体に利点はなかった。
- **band共有は非寄与**: MS=1<<24でも、band-wide（94,005,413）はfresh per-bit合計（91,941,958）より+2.24%多い。状態共有の利得はノード削減に現れない。
- **帰属バッテリで16/16 bitすべての行集合が公開証明書とbyte-identical**。容量効果のみで、証明書のバイトは1つも変わらない。
- **感度（bit 98 fresh）**: 1<<18: 25,505,012 → 1<<20: 17,721,785 → 1<<21: 14,860,944 → 1<<22: 13,262,116 → 1<<23: 12,462,197 → 1<<24: 12,193,647 → 1<<25: 12,100,297。行数は常に64,451、md5も全MSで同一（`6db21986f3a67c35dde3d9d275acd29f`）。飽和は1<<23-1<<24。

## 処方

今後の証明書抽出は、**per-bit freshプロセス×MS>=1<<23（176-352 MB）**で回せば、verbatim MS=1<<18 baseline比で約44.7%のノード削減が得られ、証明書bytesは不変。band全体を1プロセスにする必要はない（むしろ+2.24%）。MS=1<<25以上の利得は1%未満で、メモリ対効果が悪化する。

sweep側（`class4_child1_runner_v17.ts`）にも同一のMS=1<<18メモがある。sweep側の測定は同日別エントリ（`2026-11-17-n11-class2-lane-sweep-memo-capacity-measurement.md`）で出版した。

## 出版物

- `scripts/measure_band_memo_extraction_73j_20261117.py`：再実行可能なorchestrator。入力pin検証、MS変種の1行生成検証、band/fresh実行、union比較、期待値定数の再検証を1本にまとめた（bit98 fresh ms18/ms24の実行検証済み）。
- `scripts/measure_band_memo_extraction_73j.ts`：測定driver。
- `output/class2-lane-band-memo-extraction-measurement-73j-20261117.json`：全測定値・pin・解釈ガード入り。

## 解釈と次の作業

今回確かめたのは**既に出版済みの16 WIN7-D10証明書の抽出コストの構成**だけである。新しい探索verdictは作っておらず、manifestの行は1行も閉じておらず、証明書bytesも不変である。fold headの変更もない。

WIN7-D10は個別7石rootの深さ10以内の先手勝ちであり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続きUNKNOWN。
