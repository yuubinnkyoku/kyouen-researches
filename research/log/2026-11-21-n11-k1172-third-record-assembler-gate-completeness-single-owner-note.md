# K1172第三検証record組立器のgate完全性検査を補強する単一オーナー宣言（2026-11-21）

- **担当レーン（単一オーナー）**: 本n11長期レーン。
- **宣言時点の最新main HEAD**: `eb228f62bd8c3a6014a24c298ac5c4cb54754ae4`（直近commit列を確認）。
- **対象**: K1172の `assemble_third_record.py` が各batteryのstage partを「存在し、含まれるgateがすべてpass」であることしか確認せず、part内のgate欠落・余分なgate・重複gateを最終監査正本と照合していない点。実際の43 gate audit正本はpin済みだが、partの完全性をauditへ結び付ける検査を追加する。
- **先行確認**: 最新mainのAGENTS.md・knowledge README・K1172 item・K1172実験README・record assembler・研究logを確認。GitHub code searchと直近commit列で同一のgate-partition hardening宣言・実験は見つからなかった。fold20 ext2、n9-ge19、他のWIN8証明書・receipt作業は対象外。
- **受入条件**:
  1. 出版auditの43 gateを実際のstage規則で5群（pin 1・k1136 13・k1137 13・k1139 13・tampers 3）へ分け、合計43・重複0・欠落0を確認する。
  2. 各batteryの5 partを結合したgate辞書が、pin済み `harness-audit.json` の `gates` と値まで完全一致することをfail-closedで検査する。auditのstatus・gate_count・gates_orderedも照合する。
  3. 正常な合成fixtureは通過し、両batteryから同じgateを1件ずつ削除したケース・値改変・余分なgate・重複gateはすべて拒否する回帰試験を同梱する。
  4. 実際の第三検証recordの既存20 gateを保ち、再構成器の変更が出力内容に不要な差を作らない場合は旧record SHAの維持を確認する。変更が必要なら新recordを別正本として明示し、旧正本を上書きしない。
  5. 実験README・K1172・研究logを更新し、実行した検査と未実施の全体CIを区別して出版する。
- **非目標・解釈ガード**: 新しいWIN/LOSS verdict・証明書・S6行閉鎖は作らない。K1172の対象範囲を拡張しない。WIN8-D10は当該8石root限定、REFUTED-D10はLOSS証明ではない。標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はUNKNOWNのまま。
- **出版方針**: branch/PRを作らずmainへ直接反映。変更は対象assembler・専用回帰試験・実験README・K1172 item・研究logに限定し、generated領域とroot READMEは直接編集しない。
