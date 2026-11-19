# 2026-11-19 head-1410 witness 第5・第6 WIN7-D10 証明書（環境消失からの決定的再現を含む）

## 出発点

- 根拠main: aa69a487…（K1035出版後）を起点に recon、出版時のheadは cc8be6d6dc1df9ef87dd10aae4b9103035e82754（z=12 y=3 K1021 backfill直後）。
- K1033の `five-parent-refuted-excluded-cover-resolve-20261119.json`（blob 600b23d39888ea0e693742da4b2ae937a9faf0）が選定した28-root witness（53行）のうち、K1035（root C `00000000000000801202060001000000`）の2 REFUTED候補を除く未試験25候補の中から、epoch-1（前実行）でWIN7-D10と判定された2 root について証明書を出版する。
- 本ログの実行では、epoch-1の計算成果（証明書・検証成果物・driver一式）が出版前に**実行環境消失（アップグレード環境のリセット）で失われた**。再開時点で手元に残ったのは K1035の .n11.gz 副本（tool-resultsに残存、blob a9030a51… と一致確認）とsha256記録値のみだった。以下はepoch-2の再実行記録である。

## 合法応手の再導出

- 生存手規約（root stonesの任意3点と共円・共線になる空点は違法）で3 rootの合法初手を再生成し、規約コード内蔵の独立recheckと突き合わせた。
- 数は 53（root C）/ 54（第5root `00000000000000805202080001000000`）/ 55（第6root `00000000040000801202000080100000`）で、epoch-1記録と一致。`witness-win-roots-legal-move-lists-20261119.json` として出版。

## 抽出（epoch-2の再実行）

- engine: `class4_child1_cert_extractor_exact_v16.ts`（git blob 5518d375fc6b4a7a14c22a1a65586f0c1c5731c0、repoから直接取得してblob一致確認）。driverは epoch-1 と同一論理（昇順応手、extractBatch(child, bit, {}, [move])、resumable progress行、fbt_drops==0要求）。
- 第5root: child `00000000000000005202080001000000` + bit 71。54/54応手完走、5,121,073 nodes、55,857行、終局石数13〜17。1 moveあたり数十〜数百ms程度で、全体も数分。
- 第6root: child `00000000000000801202000080100000` + bit 90。55/55応手完走、931,581 nodes、30,984行、終局石数13〜17。
- 証明書 SHA-256: 第5 `69589e76e5d2e5f22e6992929f38d9fd67f07ce1bd9fe9e3f971d32bdd635a49`、第6 `5289f152e88072d716f22d42414222162facb7486d07fd024b61fdc50ddef885`。
- **epoch-1の記録値とSHA-256完全一致。gzip -n -9 指紋も一致**（第5 247,265 bytes/`aeafc6a4…`、第6 139,336 bytes/`592dd6aa…`）。決定的パイプラインが環境をまたいでbyte再現した初の体系的確認（engineの時刻依存性なし・Map走査順依存なし）。

## 二重独立検証

`verify_win_roots_rec_20261119.mjs` が BigInt 3×3余因子展開（cacheなし）と4×4 Bareiss（engine importなし）を各rootで実行:

- 第5root: 54/54 subroots、union差分 0/0、状態流量 127,080 states・16,170 terminals・124,176 opponent edges（両検証器一致）、union監査 consumed 82,983 records→55,857 unique、証明書正確一致。
- 第6root: 55/55 subroots、union差分 0/0、状態流量 66,292・10,905・59,089、consumed 42,537→30,984。
- 終局石数は両root 13〜17。root安全（共円4点なし）・root mobility は合法初手数と一致。

## 出版手順と binary push の限界

1. 成果物をまずpush（15ファイル: summary manifest、per-root progress/summary/verification/bareiss、legal list、scripts3本）— commit 52f59144。
2. 証明書本文（.n11 テキスト）を64KBページ読みで復号しpush。GitHub blob sha が epoch-1記録値と一致（第6: 02ea43b3…、第5: b072170a…）でbyte完全性確認。
3. gzipのbinary pushを試験したところ、**push transportで破損**（139,336 bytesが207,344 bytesにUTF-8膨張、blob不一致）。破損gzは直ちに削除し、以降 .gz は出版しない方針とした。証明書は .n11 テキストがrepo上の正本。gzip指紋は summary manifest に記録し、誰でも `gzip -n -9` で再現照合できる。

## 境界と残課題

- **receipt foldは未実施**。K1033のfrontier簿記（frontier 6,229行/493,184・solved S6 1,619・5親target累計21/112行・残91行）は本項目では不変。第5・第6rootの証明書行のD4像が5親targetのどの行を閉じうるかは次のfold実行で確認する。
- 同一28-root witnessの残り候補（K1035で2 REFUTED、本項目で2 WIN、他は未判定）の勝敗は UNKNOWN。本項目はroot C・第5・第6rootのWIN7-D10のみを主張する。
- 標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は UNKNOWN。REFUTED-D10 は LOSS証明ではない。
- 教訓（運用）: 長時間計算の成果は検証が通り次第、**小さい単位で速やかにrepoへ出版する**。本日は出版前の環境消失で数時間分の成果を失い、決定的再現（幸いbyte完全一致）で回復した。再現不能な局所状態に重要証拠を置かないという規約の重要性の実証例。
