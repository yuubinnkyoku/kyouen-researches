# 単一オーナー宣言: 残余23行 8根被覆判定（K1147外部第二検証）の pristine再实行による第三検証（2026-11-20）

- 宣言時刻: 2026-11-20T15:21:00Z
- 宣言者: n11長期レーン（第三検証系譜: K1153・K1155と同型）
- 対象: [K1147](../knowledge/items/K1147-n11-residual23-eight-root-cover-decision-external-second-verification.md)
  （残余23行 8根被覆判定の外部第二検証・commit `e8d6025745` 出版・实験dir `n11-residual23-eight-root-cover-decision-external-second-verification-20261120/`）
- 实施内容: GitHub上の出版byteのみから
  (1) 入力5正本（判定機 `da51063c…`・判定正本 `c5aaf83e…`・K1097再解決 `2896deb0…`・K1102第二検証 `d0b5d845…`・下界強化監査 `1310ef74…`）と外部検証機 `7bee45ec…`・出版監査 `17dbd6ab…` を再取得してpin照合、
  (2) 判定機をpristine再实行4回（同一cwd 2回・隔離tree/cwd/HOME入力別path 1回・隔離+`PYTHONHASHSEED=random` 1回）し全出力が出版正本 `c5aaf83e…` とbyte-identicalであることを確認、
  (3) 再实行出力4件を入力として外部検証機を再实行し監査が出版監査 `17dbd6ab…` とbyte-identical（71/71 check）であることを確認、
  (4) 1 byte tamperをfail-closed pinが捕捉することを確認、
  (5) 第三検証harnessとその監査正本・入力snapshot一式を自完結实験dirとして出版。
- 編成: 宣言 → part1（实験dir: README+harness+監査+入力snapshot）→ part2（K item+研究log）→ part3（knowledge README末尾bullet）。K番号はpush直前に3点確認（README grep `items/KNNNN-`・item path 404・list_commits）で確定する。
- 着手しない領域: fold26 receipt fold（先行レーン宣言 `23bffdd4e4`）・第5ラウンドrefsolve（`ace38772d9`）・WIN8-D10証明曨抽出 root `00000000010000809002000040002001`（`63877ffd2e`）・zero-triple direct fourth geometry（`b0db8dfec1` 15:11:59Z）・K1149二重採番の解消（管轄外）はいずれも本宣言の範囲外。
- 解釋規約: 本検証は出版記録の帳簿・幾何タcensusの交差検証の決定性確認であり、行を1行も閉じない。被覆数は候補root计划の簿記であり証明曨ではない。REFUTED-D10はLOSS証明ではなく、nodes数タsolved数を勝敗として読まない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
