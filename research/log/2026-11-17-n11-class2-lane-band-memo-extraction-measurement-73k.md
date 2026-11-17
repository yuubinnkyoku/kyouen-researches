# 2026-11-17：cost73kバンド抽出のメモ容量・band-wide共有測定（73j測定の73k replication+拡張）

## 開始時点

開始時のmainは `c24eb538`（K0900 workflow audit step）を起点に確認し、最新main・`AGENTS.md`・`research/knowledge/README.md`・cost73k関連のknowledge・experiments・logを読んだ。cost73k（6石child `00000000000000801206000000000400`）は22本のWIN7-D10証明書（966,535行・155,946,109 extraction nodes・manifest blob `0892aed0`）が並走claim laneにより出版済みで、本レーンは前回（`7dd863aa`）に73k band内の状態共有率32.159%・confirmation再走査コスト10.569%・band間canon共有の測定を出版している。

同日、並走レーンがcost73j bandのメモ容量測定（`c206a4be`・`measure_band_memo_extraction_73j_20261117.py`）を出版し、「抽出コストの支配因子はメモ容量であってband状態共有ではない（fresh per-bit×MS=1<<24で-44.7%、band-wideは+2.24%非寄与・証明書bytes不変）」を確定した。そこで今回の主眼は、(a) この結論の22-bit 73kバンドでの再現、(b) メモ占有率（occupied slots）の計装による「なぜMS=1<<18が失敗するか」の定量化、(c) 同一容量でのband-wide共有ペナルティのper-root分解、である。

作業中も並走レーンが活発で、mainはK0900 audit・K0901 Grundy slice・cost66i head1473 rebaseと進み、push直前のheadは `1da42ce0`。本レーンの出版対象4ファイルはいずれも新規パスで、73j測定（`c206a4be`）・73ij sweep測定（`c7342405`）の既存ファイルとの衝突は 없い。

## 測定手順

入力はすべて公開pinから取得し、Git blob SHA-1で検証した（抽出器 `class4_child1_cert_extractor_exact.ts` blob `52bcaf50`、manifest blob `0892aed0`、`legal_candidates.py` blob `8e97082c`、公開証明書22本はmanifest md5と照合・19 splitはpart1+part2結合で照合）。

MS変種は抽出器の `const MS=1<<18, MM=MS-1;` 1行置換と `extractBatch` 直前への `clearRows()` / `memoStats()` export block挿入のみで生成し、block除去後にMS行置換のみと文字列完全一致することを検証した（探索挙動への影響なし・ドライバは記録のみ）。driver `measure_band_memo_extraction_73k.ts` はplan駆動で、各bitの抽出後に (i) 行集合をsnapshotして公開証明書とbyte比較（splitは結合）、(ii) `memoStats()` でメモ占有率を記録、(iii) `clearRows()` で行Mapをリセット、する。band-wide実行は22 bitをmanifest bit昇順に1プロセスで回し（メモとfbtはbit間で持続）、fresh電池は各bitを独立プロセスで回す。sensitivityは最大root（bit 117）をfreshプロセスでMS=1<<18,20,21,22,23,24の各容量で測る。

## 結果

| 実行 | 総ノード | baseline比 | 証明書照合 |
|---|---:|---:|---:|
| baseline（公開、fresh per-bit、MS=1<<18） | 155,946,109 | 1.000 | — |
| band-wide MS=1<<18（verbatim容量） | 205,129,712 | **1.3154（+31.5%）** | 22/22 byte-identical |
| band-wide MS=1<<22 | 142,171,197 | 0.9117（-8.8%） | 22/22 byte-identical |
| band-wide MS=1<<23 | 121,186,659 | 0.7771（-22.3%） | 22/22 byte-identical |
| fresh per-bit MS=1<<23 電池 | **108,499,241** | **0.6957（-30.4%）** | 22/22 byte-identical |
| band-wide MS=1<<24 | 106,861,135 | 0.6852（-31.5%） | 22/22 byte-identical |
| fresh per-bit MS=1<<24 電池 | **105,117,037** | **0.6741（-32.6%）** | 22/22 byte-identical |

- **占有率計装（今回の新規要素・訂正版）**: bit 0の抽出だけでも、ハッシュの偏りによる挿入失敗で占有率は200,697/262,144（76.6%）で停滞する（bit 0のdistinct位置数はMS=1<<24・負荷4.8%での占有率801,870が最良推定で、262,144を大きく超える）。テーブルが文字通り満杯（262,144/262,144）になるのは第5bitのbit 35探索中で、以降のbitはintra-bitメモの挿入を完全に失い再計算が増える（band MS=1<<18のper-bit比1.0000〜1.7505・bit 39が最大）。（訂正: 初出版版は「bit 0だけで598,661位置を訪れbit 0探索中に飽和」と誤記。598,661はMS=1<<22でのbit 0占有率であり、出版後のfresh-checkout再実行でbit 0終了時76.6%・満杯到達はbit 35と確定したため修正した。）band-wide MS=1<<22は最終占有率96.98%（4,067,454/4,194,304）で依然飽和し後半bitが劣化、MS=1<<23は85.16%（7,144,086/8,388,608）、MS=1<<24は64.4%（10,804,024/16,777,216）で初めて余裕を持つ。MS=1<<23の占有率7.14Mは挿入失敗で打ち止められた下限であり、band-wide実行のdistinct位置数は最低10.8M（MS=1<<24 occupied）ある。容量設計の目安は「スロット数 > バンドdistinct位置数」で、73kバンド全体を1テーブルで回すならMS>=1<<24が必要。
- **band-wide共有ペナルティは負荷率依存であり、本質的に有害ではない**: 同一容量比較でband-wide MS=1<<23（121,186,659）はfresh per-bit MS=1<<23（108,499,241）比**+11.69%**（per-root比0.9466〜1.3380、負荷率0.68→0.85でbit順に悪化、利得はbit 39/41のみ）だが、band-wide MS=1<<24（106,861,135）はfresh per-bit MS=1<<24（105,117,037）比**+1.66%**に縮む（最終負荷率64.4%）。MS=1<<24ではbit 39/41/44/58/73/97がband共有でむしろ速く（比0.845〜0.978、cross-bit再利用）、汚染はバッテリー後半のbit 89/94/112/117に集中する（1.086〜1.159）。73jは負荷率~0.24で+2.24%だったので、ペナルティは最終負荷率の単調関数ではなく、高負荷（>=0.85）で汚染が支配する一方、中負荷ではbandごとのcross-root重複構造で符号が決まる。
- **メモ総量で比較するとband-wide単一テーブルが逆転勝ち**: band-wide MS=1<<24（16.78Mスロット1本・106,861,135 nodes）は、fresh per-bit MS=1<<23電池（8.39Mスロット×22本=184.6Mスロット・108,499,241 nodes）より11分の1のメモでノード数も少ない。全22 rootを1プロセスで回す抽出電池の設計としては、per-root freshテーブル22本（MS=1<<23）より共有1本（MS=1<<24）がメモ・ノード両面で優る。per-root独立プロセスの並列性を優先する場合はこの限りでない。
- **bit 95（root `00000000800000801206000000000400`・11,857,737 nodes）はmemo-state-invariant**: published（fresh MS=1<<18）、fresh MS=1<<23、band-wide 3容量の全構成で完全同一ノード数。このrootの探索は位置の再訪問を生まない構造で、メモが効かない。
- **bit 112の見かけの容量逆転はband/fresh比較混同だった**: fresh per-bitではbit 112の容量応答は単調（MS=1<<23: 4,767,520 > MS=1<<24: 4,620,105 nodes、fresh占有率は934,822/8.39Mと1,060,331/16.78Mで飽和まで遠い）。作業メモに残っていた「MS=1<<24で5,055,110に増える」という観察はband-wide MS=1<<24実行のbit 112（共有メモ蓄積占有率10,548,738・cross-bit汚染比1.094）をfreshと比較したもので、hash-mask sensitivityでも容量単調性違反でもない。
- **フィデリティ**: band MS=1<<18のbit 0（band先頭・メモ空状態）は6,442,831 nodes・53,456行で公開値と完全一致。anchor bit 39 fresh verbatimは2,597,243 nodesでmanifest extraction_nodesと完全一致・証明書byte-identical。fbt_dropsは全構成で0・fatal無し。全6構成×22 root = 132照合（band 18/22/23/24・fresh 23/24）すべてbyte-identical（19 splitはpart1+part2結合で照合）。sensitivity bit 117の6容量も全てbyte-identical。
- **sensitivity（bit 117 fresh・最大root）**: MS=1<<18: 10,635,766（=published値）→ MS=1<<20: 8,768,282 → MS=1<<21: 8,103,818 → MS=1<<22: 7,599,134 → MS=1<<23: 7,100,995 → MS=1<<24: 6,816,404（全容量で証明書byte-identical、飽和脱出後も鈍く減少し続ける）。

## 処方

73j処方のうち「抽出コストの支配因子はメモ容量」は73kでも成立（fresh容量増で-32.6%まで単調減・証明書bytes不変）。ただし「band-wideは不要」は修正が必要で、共有のペナルティは負荷率依存: 負荷率85%では+11.7%だが64%では+1.66%で、しかもband-wide MS=1<<24はfresh MS=1<<23電池よりメモ11分の1でノードも少ない。処方としては、(a) rootごとの並列独立プロセスを優先するならper-bit fresh×MS=1<<23（176 MB/root）、(b) 1プロセスでバンド全体を回すなら共有1本×MS=1<<24（352 MB・負荷率<=~65%）、の二択を目的に応じて使い分ける。worker間メモmergeは負荷率85%相当の高負荷では期待薄だが、merge後負荷率が64%程度に下がる容量設計ならほぼ中立になる。なお、公開済みの73k extraction_nodes（manifest）はMS=1<<18飽和下の値であり、真の最小コストではない（fresh MS=1<<23で-30.4%相当）が、証明書の内容・verdictには一切影響しない。

## 出版物

- `scripts/measure_band_memo_extraction_73k_20261117.py`：再実行可能なorchestrator（入力pin検証・変種生成検証・band/fresh/sensitivity実行・全snapshotのbyte-identity検証・期待値定数の再検証を1本にまとめ・resume対応・各step後にJSON逐次保存）。
- `scripts/measure_band_memo_extraction_73k.ts`：測定driver（plan駆動・snapshot+占有率記録）。
- `output/class2-lane-band-memo-extraction-measurement-73k-20261117.json`：全測定値・占有率曲線・pin・解釈ガード入り。

## 解釈と次の作業

今回確かめたのは**既に出版済みの22 WIN7-D10証明書の抽出コストの構成**だけである。新しい探索verdictは作っておらず、manifestの行は1行も閉じておらず、証明書bytesも不変である。fold headの変更もない。73i証明書の出版有無の再確認（出版済みならBigInt bytes再検証）は次回レーンで再確認する。

WIN7-D10は個別7石rootの深さ10以内の先手勝ちであり、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4は引き続きUNKNOWN。
