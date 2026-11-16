# 2026-11-16：bit-79 orbit（65f bit-79 ≡ 63a bit-97）は証明書被覆済み — claim v5 certified:false由来の「両側無証明」観測はstale・抽出不要・11×11等はUNKNOWN

本レーンの独立検証記録。**65f bit-79 root `00000000000080809102000080000000` と 63a bit-97 root `00000002000000809102000800000000` は同一D4 orbit**（正準形 `00000000000080809102000080000000`・popcount 7・Python stdlib再導出と独立Node.js BigInt実装（d4check.js）の両方で一致）。65f側はWIN7-D10・63a側もWIN7-D10（63a sweep WIN bits [2,11,15,28,96,97,100,109,118,119]）でverdict一致・conflictなし。

## 証明書の実在確認（main再取得・join再検証）

- win13 manifest（blob `617d3d8d`・commit `64ff9c1d`）のbit 79欄: **39,574 rows・3,246,377抽出nodes・49 sub-roots・BigInt union 0/0 + Bareiss 49/49 PASS**。
- 出版パーツ `….cert.part1of2`（715,086 B・blob `809f2c57`）+ `part2of2`（715,054 B・blob `3a823f02`）をmain（`9f4684ad`）から再ダウンロードし**cat join 1,430,140 bytes・md5 `e94b722b45445f11156df7830c79f1b9` がmanifestのwhole_md5と一致**。
- 63a bit-97側は正準root（=証明書root）のD4像なので、対称性により**この出版証明書が同orbitの両表現を被覆**。新規抽出は不要。

## stale読みの訂正

claim v5（`class2-lane-cost65j-inflight-20261115.json`・schema `-v5`）の「thirteen cost-65f receipts … no published certificates（certified:false）」は**v5執筆時点では正確**だが、2026-11-16のwin13証明書完結（`64ff9c1d`）で失効済み。claim v5のcertified:false欄から導かれた「bit-79 orbitは両側無証明・最優先engine証明書target」という観測は**stale**であり、engine証明書抽出ワークロードから除外してよい。

## UNKNOWN guard

WIN7証明書は当該orbitの個別7石root（相手初手すべてに対するfirst-player win・depth 10以内）のみを証明する。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4はいずれもUNKNOWNのまま**。

## 成果物

- 検証JSON: [class2-lane-bit79-orbit-certificate-verification-20261116.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-bit79-orbit-certificate-verification-20261116.json)
- 被覆証明書: win13 manifest `617d3d8d` bit 79（parts blob `809f2c57`/`3a823f02`）
