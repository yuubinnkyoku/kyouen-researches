# 単一オーナー宣言： 残余23行 零triple-provider第四幾何（K1156）の pristine再実行による第三検証（2026-11-20）

- 宣言時刻： 2026-11-20T15:49:00Z
- 宣言者： n11長期レーン（第三検証系譜： K1153・K1155と同型）
- 対象： [K1156](../knowledge/items/K1156-n11-residual23-zero-triple-direct-fourth-geometry.md)
  （残余23行の3零行を行+2空き点直接生成で再導出する第四幾何。実験dir `n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/`・検証機 commit `3969a050`・出版監査 commit `7c21ad16`・出版監査 SHA-256 `c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f` 7,627 bytes・item commit `1d1b185a`・index bullet commit `65980eac`）
- 実施内容： GitHub上の出版byteのみから
  (1) 検証機 `verify_direct_fourth.py`（SHA-256 `850df34b…`）・入力3正本（provider input `51e7a465…`・K1148第三幾何監査 `526eada2…`・K1147外部第二検証監査 `17dbd6ab…`）・出版監査 `c4a55dbe…` をpinned commit `49e420fe` からraw CDNで再取得してpin照合、
  (2) 出版検証機を1 byteも改変せずpristine再実行4回（同一cwd 2回・隔離tree複写+隔離cwd+隔離HOME 1回・隔離+PYTHONHASHSEED=random 1回）し、全4回の出力SHA-256が出版監査 `c4e55dbe…` 7,627 bytes と byte-identical であることを確認、
  (3) 1 byte tamper（出版レーンが検査済みのoffset 100とは異なるoffsetを選ぶ）をSHA-256 pinがfail-closed捕捉することを確認、
  (4) 第三検証harness（stdlibのみ・決定的・fail-closed・時刻/乱数/環境依存出力なし）とその監査正本・入力snapshot一式を自己完結実験dirとして出版。
- 編成： 宣言 → part1（実験dir： README+harness+監査+入力snapshot）→ part2（K item+研究log）→ part3（knowledge README末尾bullet）。K番号はpush直前に3点確認（README grep `items/KNNNN-`・item path 404・list_commits）で確定する。
- 着手しない領域： K1147外部第二検証のpristine再実行第三検証（宣言 `887e594d` 15:23:39Z）・fold26 receipt fold（`23bffdd4e4`）・第5ラウンドrefsolve（`ace38772d9`）・WIN8-D10証明書抽出 root `00000000010000809002000040002001`（`63877ffd2e`）・K1149二重採番の解消（管轄外）はいずれも本宣言の範囲外。
- 解釈規約： 本検証は出版byteから機械と監査が独立に再現できることの決定性確認であり、行を1行も閉じない。第四幾何は被覆計画の簿記でありゲーム理論的証明書ではない。REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
