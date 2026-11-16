# 2026-11-16：cost64h 23 WIN7-D10証明書のPython第四独立検証 — 23/23 PASS（第三者検証6 bit全フィールド一致・lane bareiss-verify 21 bit move毎一致・116/120は初の完全独立検証）

開始時main: `ae7e5837`（本レーンのv15 cross-engine検証直後）。並走の第三者検証（Node BigInt 4×4 Bareiss・`verify_cost64h_certificate_bareiss_independent_20261116.mjs`）は出版時点の6証明書（bits 4, 6, 38, 49, 74, 91）のみをカバーし、lane自身の `bareiss-verify.json` は21/23（bit 116欠、bit 120欠・summaryも欠）だった。本セッションで**全23 WIN7-D10証明書を、アルゴリズムが既存3verifierのいずれとも異なる純Python第四verifierで完全再検証**した。

## 手法

- **正規化整数一般化円方程式**: 3石を通る円または直線を3×3 Cramer行列式（Python多倍長整数）で解き、`(A,B,C,D)` をgcd正規化・符号正規化した整数係数として保持。合法手判定は `A(x²+y²)+Bx+Cy+D==0` の整数テストのみ。Bareiss 4×4ともrepo 3×3余因子verifierとも手法が異なる。
- **内蔵self-test**: 400個の5点 sampled configuration（47,200点テスト）で円方程式の禁止マスクと直接4×4 Bareiss行列式が全一致することを確認（Bareissはself-test内でのみ使用）。
- **完全all-reply探索**: 第三者検証と同じ証明書契約（root 7石・safe・loser手番開始・winner手はstrategy表・loser手番のstrategy行禁止・terminalはodd depthでstuck loser・終局石数13-17・strategy行=消費winner状態の厳密一致・行は厳密昇順一意）を全て再実装。
- 23証明書を4並列で検証（最小bit91が2.9秒・全23件で約40秒）。

## 結果

- **23/23証明書が全チェックPASS**: union missing 0 / extra 0・terminal range union [13,17]・strategy行計 **804,783**・訪問状態計 **1,755,168**・loser応手辺計 **1,584,262**・terminal計 **280,569**。
- **第三者検証（Node Bareiss）との一致 6/6**: bits 4, 6, 38, 49, 74, 91 の全集計フィールド（mobility・rows・visited・winner/loser states・edges・terminals・range）がbit-exact一致。
- **lane bareiss-verify との一致 21/21**: bit毎の `loserMobility`・`stones` に加え、**subroot（rootのloser応手）毎の seen・terminals・opponentEdges・terminal range** が全move完全一致。
- **bits 116・120はlane検証記録（bareiss-verify/bigint/summary）の欠損bitだが、本検証で初めて完全独立検証された**（bit120は23枚中最大・strategy行・visited等はverification JSONに記載）。
- 証明書blob pinは第三者検証出版値と6/6一致（ダウンロードbyte-exact確認済み）。

## 意味

- cost64hの23 WIN7-D10証明書は、(1) repo 3×3余因子BigInt verifier、(2) sweep engineのNumber-Bareiss、(3) Node BigInt Bareiss第三者検証、(4) 本Python一般化円方程式検証、の**4実装（言語・アルゴリズム双方で独立）**で検証済みとなった。fold receipt（head 1452→1472投影・prereg `5074a8a0…`）が消费する23 WIN rootの証明基盤が最も厚い状態になった。

## 出版

- 検証script: `scripts/verify_cost64h_certificate_python4_20261116.py`（self-test内蔵・単一cert検証モード）。
- 検証JSON: `output/class2-lane-cost64h-certificate-python4-fourth-verification-20261116.json`（23 cert分の全統計・checks・第三者/lane一致結果・self-test記録・blob pins）。

## 信頼境界

- 本検証は個別7石rootの `original_first_WIN7 / second_to_move_LOSS` の再確認であり、6石manifest行のクローズはreceipt foldの再計算とcommitまで確定しない。REFUTED-D10はLOSS証明ではない。solvedはmanifest被覆の簿記。
- 標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4 はいずれも **UNKNOWN** のまま。

## 再現

```sh
python scripts/verify_cost64h_certificate_python4_20261116.py --selftest
for b in 4 6 8 33 38 42 44 49 68 74 76 77 78 79 83 89 91 101 109 113 114 116 120; do
  python scripts/verify_cost64h_certificate_python4_20261116.py \
    output/class2-lane-cost64h-certificates/bit$b-root-*.cert
done
```
