# 2026-11-17 長期レーン: 証明書band内・band間の状態共有とconfirmation再走査コストの測定（共有cache・転送再利用の定量的下界・11×11はUNKNOWNのまま）

## 何をしたか

優先事項(5)「測定に基づく改善」の一環として、main出版済みのWIN7-D10証明書3 band
（cost73j 16本・cost72d 11本・cost71e 13本・入力全ファイルをgit blob shaでpin）と
73i/73j sweep独立再実行verification JSONから、cache再利用ポテンシャルを**決定的な集合測定**で定量した。
script `measure_cert_state_sharing_and_conf_cost_20261117.py` + output JSON
`class2-lane-cert-state-sharing-and-conf-cost-measurement-20261117.json`（2回実行byte-identical・md5 `eb18698f`）。

## 測定結果

1. **band内状態共有（同一band内の別root証明書に現れる同一局面）**:
   - 73j: distinct 547,910 states中 **142,470 (26.00%)** が複数証明書（最大7本）に共有。**行ベースでは24.61%が重複**。
   - 71e: 22.52%共有・21.03%重複行。72d: 20.15%共有・19.04%重複行。
   - 3 bandすべてで**20-26%の一貫したband内共有**。現在の抽出（rootごと別プロセス）はこの共有を再利用していないため、
     **band内共有memo付き抽出は行数ベースで~19-25%の重複削減ポテンシャル**（node削減は行数と厳密には比例しないが、
     63dのper-process memo共有でnodes 14.4M→9.6M〔33%削減〕の先例と整合的）。
2. **band間状態共有**: **72d∩73j = 17,939 states（73jの3.27%・72dの4.24%・石数12-16に集中）**。
   一方**71e∩72d = 0・71e∩73j = 0・3-way共通 = 0**。つまりband間共有は**構造的に隣接するchild間
   （72d/73jは同一コア石を持つchild）でのみ発生**し、離れたchild（71e）とは深い位置でも全く共有しない。
   → 恒久cross-band cacheの価値は「隣接band対」に局所化される。73k（本日25 WIN）は73i/73j系childと
   同一コア構造のため、73k証明書抽出時には73i/73j/72d bandとの共有が見込まれる。
3. **confirmation bit（転送済み位置）の再走査コスト**: 73i sweepの2.13%（2,797,233 nodes）、
   73j sweepの**6.97%**（11,739,699 nodes・bit46が5.3M nodesと最大）が、census overlayで既にverdict転送済みの
   位置の再確認に使われている。転送を信頼するverdict cacheがあれば这部分が直接削減される
   （現行のalways-re-confirm方針の測定済みコスト）。
4. 以上はすべて**完全一致キーの測定下界**。D4正準化キー（対称性併合）は追加の上振れ要素で本測定では未量化。

## 解釈上の注意（interpretation guard）

- 効率測定のみで、いかなるmanifest行も閉じない。WIN7-D10証明書は**個別7石rootのdepth-10内先手勝ちのみ**を証明し、
  REFUTED-D10はLOSS証明ではない。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 の
  勝敗はいずれもUNKNOWNのまま**。

## レジューム

1. 73k証明書（並走claim laneが抽出・出版予定・25本）に対し、本測定のband内共有memo付き抽出
   （1プロセスで全root・状態keyed memo共有）がnode削減候補。ただし抽出はclaim laneの管轄のため、
   本レーンは測定・検証支援に回る。
2. 73i証明書のBigInt bytes再検証（並走の出版待ち・着手禁止）が本レーンの次の検証候補。
