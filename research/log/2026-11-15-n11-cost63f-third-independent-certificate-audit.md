# 2026-11-15 n11 cost-63f certificates: third independent replay

## 対象と作業範囲

cost-63f sweepは63候補をdepth 10で処理し、WIN7-D10がbit85/91の2件、REFUTED-D10が61件、capped 0、探索節点44,140,211。両WIN7証明書はmainに公開済みで、既存のBigInt検査器とNumber Bareiss検査器による二重検証も記録されている。

この回では、その2証明書を既存検査器・探索器・判定cacheをimportしない第三の幾何実装で再生した。証明書本体はGitHub blob APIから取得し、manifestのbytesとblob SHAに一致することを確認した。

## 独立幾何判定

3点が非共線なら、有理数の外心を分子・分母で表し、候補点が同じ円周上にある条件を整数式で判定する。3点が共線なら、候補点も同じ直線上にあるかを整数外積で判定する。浮動小数点は使わない。

座標は0..10、二乗距離は0..200。外積・外心分子・判定式の中間値は2^53を大きく下回るため、JavaScript Numberでも整数演算は厳密。

各rootについて、7石安全性、合法な相手初手、勝者の戦略手の合法性、敗者の全合法応手、終局時に敗者が手詰まりであることを検査した。相手初手ごとに探索木を分け、消費された勝者局面の和集合と証明書行集合の一致も確認した。

## 結果

| 指標 | bit85 | bit91 |
|---|---:|---:|
| 証明書行 | 40,154 | 29,305 |
| root合法応手 | 51 | 49 |
| sub-root | 51 | 49 |
| 訪問局面（sub-root合計） | 87,882 | 64,688 |
| 勝者手番局面（重複を含む） | 57,352 | 41,812 |
| 敗者手番局面（重複を含む） | 19,083 | 13,361 |
| 敗者の応手辺 | 84,887 | 59,739 |
| 終局 | 11,447 | 9,515 |
| 終局石数 | 13..17 | 13..17 |
| rootからの最大手数 | 10 | 10 |
| missing / extra | 0 / 0 | 0 / 0 |

両rootとも全sub-root PASS。証明書行はすべて到達可能で、到達した勝者局面に不足行はない。root合法応手数もmanifestの51/49と一致した。

2証明書の合計は69,459行、訪問局面152,570、敗者応手辺144,626、終局20,962。

## D4親局面の共有

7石rootから1石ずつ削除する14件の親liftをD4正準化した結果、**13個の異なるS6親軌道**になった。重複は一つだけで、共通のS6 child

`00000000000080809002000000000800`

である。bit85を削除した場合とbit91を削除した場合の両方が同じchildへ戻る。2つの7石root自体のD4正準形は異なる。

これは14辺を14軌道として二重計上しないための確認である。残る12親軌道がglobal frontierで開いているか閉じているかは、この監査では判定していない。

## 再現用成果物

- `scripts/audit_cost63f_certificates_rational_independent_20261115.mjs`
- `output/cost63f-rational-independent-certificate-audit-20261115.json`
- `.github/workflows/ci.yml` にNode 22での第三検査とJSON再生成比較を追加

スクリプトは証明書のMD5・SHA256・Git blob SHAも照合する。今回のin-session再生では、tree検査・件数・D4親lift、GitHub blob SHAとbytesを確認した。追加したCIの完了結果はこのログ作成時点で未取得なので、CI PASSとは記録しない。

## frontierと未解決性

cost-63fの2 receipt foldは、別の長期class2 laneがhead 1195でin-flight claim済み（commit `df33461de854cce1375381c8d61be4b614b7598d`）。同じfoldを重複起動していない。

したがって今回の監査によるglobal frontier寄与は0。現headは `1195/6652/524884/4922/388607` のまま。fold完了後に初めてreceipt被覆を計上する。

この2証明書が示すのは、個別の7石root bit85/91から10手以内の先手勝ちだけである。6石childのglobal閉鎖はfold待ちであり、標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class2、class4は引き続き **UNKNOWN**。
