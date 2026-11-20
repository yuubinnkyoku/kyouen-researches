# 残余23行 零triple-provider禁止円 D4軌道構造解析（16:41Z追加出版）のpristine再実行第三検証（2026-11-20）

## 経緯

- 最新 main 取得（HEAD `3ccde3e385137b1a51cd2821a078ede38a2b3dfb`・2026-11-20T16:41:05Z）。
  同 commit は K1156 第四幾何の後解析「禁止円の構造解析」（unsafe 10 出現を 2 つの D4 円軌道へ分類、
  実験dir `n11-residual23-zero-triple-forbidden-circle-structure-20261121`・K1156 item 追記・log 1 件）の
  出版だった。fold26 receipt fold・round-5 refsolve・WIN8-D10 root `00000000010000809002000040002001`
  証明書抽出はいずれも先行レーン宣言済みで未着地・着手不可。K1147/K1149/K1144/K1151/K1148/K1156 本体の
  第三検証は K1158/K1159/K1160/K1155/K1153/K1157 で出版済みで、16:41Z 出版の本追加解析が未検証の
  残りとして最も価値が高いと判断した。
- 単一オーナー宣言ノートを先行出版（commit `b7d2880cdf66b2a30ad3e5cc8ebe36481ea8eba3`・
  2026-11-20T16:56:15Z 着地）。並走の同対象宣言なし。
- 作業器材 `/home/user/work/k1161/`（pinned 取得・fresh runs・tamper・harness・実験dir）。

## 実行内容

1. **pin 4/4**: 出版byteを pinned commit `3ccde3e385…` から GitHub raw CDN で再取得して、
   検証器 `45e5d7d6…`（16,831 bytes）・出版監査 `0e16f29b…`（9,730 bytes）・K1156 fixture
   `51e7a465…`（3,105 bytes）・K1156 第四幾何監査 `c4e55dbe…`（7,627 bytes）の 4 SHA-256 が全一致。
2. **fresh-run 4/4**: runA/runB（同一cwd 2 回）・runC（複写隔離 tree・隔離 cwd・隔離 HOME・env -i 相当・
   入力複写）・runD（runC と同じ隔離+`PYTHONHASHSEED=random`）の全 4 回が出版監査正本
   `0e16f29b…` 9,730 bytes と byte-identical（returncode 0）。判定は bash sha256sum+cmp。
   1 実行は 1 秒未満（14 出現の D4 埋込み再導出と Fraction ガウス消去による円当てはめのみ。
   DFPN 探索と 6,555 根の再列挙は含まない）。
3. **tamper 2/2**: 出版社 README 検査済み offset 100 と別の offset で 1 byte XOR 0x01。
   - fixture offset 200 → 改変後 `f5c6a73d…`・returncode 1・出力未生成
   - K1156 監査 offset 150 → 改変後 `954843ee…`・returncode 1・出力未生成
   の 2 件とも fail-closed 捕捉。
4. **harness 決定性**: 第三検証harness `scripts/verify_reexec_third.py`（stdlib のみ・fail-closed・
   pin 4 点内蔵・fresh-run 4 回・tamper 2 件・監査JSON sorted keys 生成を 1 コマンドで実行）の
   監査正本 `f12abd19…`（3,321 bytes）が同一cwd 2 回＋隔離tree/cwd/HOME+`PYTHONHASHSEED=random`
   1 回の 3 実行で byte-identical。
5. **出版**: part1 commit `b10b57216509f87617d726f7c35a8b38fc764160`（実験dir 7 ファイル: README・
   harness・stage 4 出版byte複写・監査正本）。fetch-back 7/7 cmp byte-identical。
   part2 が本 item `K1161` + 本log。採番は push 直前 3 点確認（README grep `items/K1161-` 0 件・
   item path 404・コミットメッセージ K1161 0 件）。

## 新規実験事実

- 16:41Z 出版の後解析は新規 byte（検証器・監査とも K1157 対象外）で、追加解析単位でも
  第三検証が必要だった。本検証で「K1156 追加解析含む 5 実験（本体+追加解析）が出版byteのみで
  再生可能」になった。
- 出版社が tamper 検査した offset 100（fixture）のみならず、K1156 監査入力側の別 offset 150 も
  fail-closed で捕捉されることを確認（出版機の pin は入力 2 点ともカバー）。
- 検証器は 1 秒未満で完走するため、第三検証コストが本体幾何（約 5 秒・550,620 子局面）より
  さらに軽い後解析クラスであることを確認。

## 解釈規約

- 行は 1 行も閉じない。候補被覆の簿計でありゲーム理論的証明書ではない。
- safe 4 出現の除外は pin 済み REFUTED-D10 事実に依存する。REFUTED-D10 は LOSS 証明ではない。
- nodes 数・solved 数を勝敗として読まない。
- **標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

## 引き継ぎ

- fold26 receipt fold（先行レーン `23bffdd4e4`/`e53cc60c23`）・round-5 refsolve（`ace38772d9`）・
  WIN8-D10 root `00000000010000809002000040002001` 証明書抽出（`63877ffd2e`）は引き続き他レーン
  宣言済み・未着地。着地後の正本第二検証が次回最優先。
- 器材 `/home/user/work/k1161/` は環境リセットで消失可。全成果は repo 出版済み
  （宣言 `b7d2880c`・part1 `b10b5721`・part2 本commit）。
