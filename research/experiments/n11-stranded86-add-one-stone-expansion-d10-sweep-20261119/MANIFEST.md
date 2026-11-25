# n11-stranded86-add-one-stone-expansion-d10-sweep-20261119

標準11×11空盤レーン（head-1410系）の K1046 後続実験一式。

K1046 で117-rootプールがdepth-10完全判定され、残余86行がプール内strandedとなった。
本実験は (1) 86行のadd-one-stone候補拡張census、(2) 43 pair-witness掃引、
(3) 第9〜第12 WIN7-D10証明書の抽出と二重独立検証、(4) 4-receipt fold、
(5) 残余78行のカバー再解決（resolve5）までを1本に束ねた。

## 主結果（2026-11-19時点）

- census: universe 8,663（in_pool 98・known_refuted 7・known_win 0・fresh 8,558
  = safe 5,142 + unsafe 3,416）。既存WIN receiptは86行を0行被覆。
  pair完全被覆（maximum matching 43 → 86/86行）。witness 43。
- 掃引: 43 root × 両AND順序 = 86 probe、全件pilot_d6合格（loss=false・nodes=3,402）。
  **WIN 4 / REFUTED 39 / CAPPED 0 / 順序矛盾 0**、総nodes 173,165,148。
- 証明書: 第9〜第12 WIN7-D10を.n11テキスト正本で出版。BigInt 3×3余因子展開と
  4×4 Bareissの二重独立検証は全subroot PASS・union差分0・状態流量一致・終局[13,17]。
- fold: frontier 6,222行/492,688 → **6,213行/492,021**、solved S6 1,626→**1,635**、
  parent incidence 11,848→11,826。閉鎖9 S6行（target 8行＋tenthのextra 1行
  `00000000000000801082080400000000`）、closed_edge_cost 667。
  5親target **26→34/112（残余78行）**、fully-closed parent 0。
- resolve5: 残余78行はfresh-safe候補の39 pair witnessで完全被覆（matching 39・
  stranded 0）。39 witnessは次回掃引の条件付き計画であり証明書ではない。

## レイアウト

```
census/
  expand86.py                                  # 86行census + witness 43 決定スクリプト
  output/add-one-stone-expansion-86-rows-20261119.json
                                               # census正本（二回実行byte-identical・
                                               # SHA-256 6fe87d61ebf9676d3847c85b16982566a7d0c867e8746dbe6a87871cca153897）
sweep43/
  roots.json                                   # 43 witness（各2行pair）
  driver.py / assemble.py                       # 掃引driver・分類組立
  output/probe-records-w0.jsonl / w1.jsonl     # 86 probe生記録
  output/witness-43-root-depth10-sweep-20261119.json   # 分類正本
  output/worker0.log / worker1.log             # 実行ログ
  output/README.txt
cert-9th/  cert-10th/  cert-11th/  cert-12th/   # 各: .n11（証明書正本）+
                                                # bareiss-subroots / bareiss-union-audit /
                                                # extraction-progress / extraction-summary /
                                                # independent-verification / extract-stdout.log
                                                # ただし cert-9th の .n11 は 3,069,801 bytes のため
                                                # .n11.gz.b64（gzip+base64・561,188 bytes）として出版。
                                                # 復元: base64 -d <file>.gz.b64 | gunzip > <file>.n11
verify/
  win_legal_gen.json                           # 4 rootの法定手リスト（独立再導出）
  extract_root_rec_20261119.mjs                # 証明書抽出器（repo既存のv16系）
  verify_one.sh / qverify.sh
  verify-w0.log / verify-w1.log                # 二重実行検証ログ
  scripts/class4_child1_cert_extractor_exact_v16.ts
  scripts/verify_bit7_win7_cert.ts
  scripts/verify_win7_certificate_bigint_independent.mjs
fold/
  fold_ninth_twelfth.py                        # 4-receipt fold実装
  resolve5.py                                  # 残余78行カバー再解決
  output/ninth-twelfth-win7-receipt-fold-20261119.json
  output/post-twelfth-receipt-cover-resolve5-20261119.json
```

## 証明書SHA-256（.n11正本）

- 第9  `00000000000000801202000001040200` 84,928行  503ff9dadc7a0d52cba8d75fa185273c798811e2ca1a897eee98cbd2b6cce631
  （出版形態: `win7-root-00000000000000801202000001040200-20261119.n11.gz.b64` 561,188 bytes。
  `base64 -d`＋`gunzip` で復元した3,069,801 bytesのテキストが上記SHA-256と一致する）
- 第10 `00000000000000821082040200000000` 45,450行  6ba50576f3f9500d0b11ffa4a47231255e9968af40e6dcb0330c09a58fc6d426
- 第11 `00000000000000821092200000000000` 24,375行  c68e63752392d17002e4d2447b23f0f98da55348400b952c0f8dbff269a6b566
- 第12 `00000000001020003800000048000000` 26,756行  6513b7d57ace489764b7c863025487b2d14313e134153a1460a039578287e37a

抽出はすべて source_engine blob `cc8be6d6dc1df9ef87dd10aae4b9103035e82754`（extract-A/B/C/D.log 参照）。
raw maxbit child規約（canon_hex(child) 不使用・K1046の事故教訓を継承）。

## 主な入力pin（fold/resolve5 の source_blob_pins）

worklist 2fee1d0718547a62e346d35f5858d7913e37c097 / ledger e8785d509e8a11a37c0d03cc450455a14708c34d /
census 9c251da3… / cover49 a8eaf00b… / fold4 38715413… / fold56 134796a7… /
fold7 sha256 f1baf159… / fold8 sha256 afcf7d0a… / resolve4 sha256 2ad70afba… /
sweep35 sha256 8b7ba7d6… / extractor_v16 5518d375… / bigint verifier 62b5d941… /
bareiss verifier 2960afab… / runner_v17 c132cc64…

## 解釈規約

- WIN7-D10 = 両AND順序で未打切りのloss=true（順序矛盾0）。REFUTED-D10は7石rootの
  depth-10内先手勝ちなしを意味するだけで、LOSS証明や行閉鎖ではない。
- foldは行被覆の簿記。witness/resolve5の39 witnessは条件付き計画。
- verdict結合は明示pinned sourceのみ（379 REFUTED / 168 WIN・矛盾0）。
  8,964 verdict cache全体との結合ではない。
- 標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN。
