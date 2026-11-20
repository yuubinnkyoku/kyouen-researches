# K1166 fold29外部第二検証の第三環境再実行（2026-11-21）

## 着手時点

最新mainは `4eb2205e7fcb30e34fcbb8bdd658ad82c27c513e`。`AGENTS.md`、`research/knowledge/README.md`、`research/knowledge/SCHEMA.md)、K1166・K1167・K1168・K1170と関連実験・研究ログを確認した。K1171まで採番済みで、K1172の項目・参照は存在しないことを確認した。

対象は先行する単一オーナー宣言（`ec24b235f806822086680fee4075820679c78acf`）が本長期レーンに割り当てたK1166第三検証である。fold20の外部第二検証、fold23/fold25/fold26、round-5 refsolve、WIN8候補抽出、既刊証明書の行共有監査など、別レーンの宣言対象には着手していない。

## 既出版実験の照合

main上の実験 `research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/` を読み、README・reproduction.log・third-verification.json・2 batteryの監査正本を照合した。

- 出版byte 5点のSHA-256 pinが一致。
- 上流pin commit `28d223a2dd254b8a85cc342dff3f4bd801d1b31f` から61ファイルを再構成し、Git blob pin 61/61一致。
- 通常環境と隔離環境（隔離cwd/HOME・`PYTHONHASHSEED=random`）の2 batteryで、各43 gate全PASS。
- 両batteryの監査正本は出版正本（15,549 bytes・SHA-256 `cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f`）とbyte-identical。5分割記録もbattery間でbyte-identical。
- 内蔵tamper 3件は両batteryでfail-closed。追加のoffset 8888負の制御もrecord未書込で捕捉。
- 第三検証recordは20 gate全PASS、4,363 bytes、SHA-256 `a6a3e0489411cd7f48fa53c2679505344f06389b8458b64c2b34e21fdf1fb18c`。既定seed 2回とrandom seed 1回の3出力がbyte-identical。

この出版物は第三検証の実験dir・実行記録を含む。今回の作業では長いbatteryを重複実行せず、既出版の正本とその再現記録を照合して、未登録だった知識項目と研究ログへ接続した。追加の探索や勝敗判定は行っていない。

## 出版

- knowledge item: `research/knowledge/items/K1172-n11-k1166-fold29-ext2-pristine-third-verification.md`
- 本ログ: `research/log/2026-11-21-n11-k1166-fold29-ext2-pristine-third-verification.md`
- knowledge README末尾にK1172の索引項目を追加。generated領域とroot READMEは直接編集しない。

## 限界

第三検証はK1166の外部第二検証の再現性を検査するもので、独立した第四の証明器ではない。S6行閉鎖0、WIN/LOSS verdict追加0、残余20行・候補pool 120,416根は不変。WIN8-D10は各8石rootのゲーム木に限り、REFUTED-D10はLOSS証明ではない。

標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はUNKNOWNのまま。
