# 研究ログ: 残余23行 zero triple provider（K1148）pristine 再実行第三検証（2026-11-20）

## 経緯（時系列）

1. **最新main確認**: 着手時 main = `da7f032cf8`（14:51:50Z・y12 two-token K1152 README bullet）。並走状況: K1150=general-multiset mergeレーン（先着 14:39:25Z `af3fb91b30`）、K1151=自レーン（replace9 whole-record 第二検証・出版済み）、K1152=y12 two-tokenレーン（14:50:56Z `855d7d98cd` で K1150→K1152 再採番・K1149 二重採番は未解消のまま）。次の空き番号 K1153。
2. **対照の誤りの訂正**: 当初メモしていた出版 commit の完全SHAとしていたものは誤りで、正しくは K1148 出版 commit `6564fded75038c887c095873c5d3e5633c4fcd35`（14:28:01Z・publish ファイル7点を commit files API で確認・実験dirは `n11-residual23-zero-triple-provider-third-geometry-20261120`）。取得し直して、検証機 `cb8c95c8…`（14,225 bytes）・fixture `51e7a465…`（3,105 bytes）・出版監査 `526eada2…`（4,418 bytes）の3 SHA-256 が全て一致した。
3. **事前 probe**: 宣言前に 1 回 pristine 再実行（約4.2秒・returncode 0・出力 SHA-256 `526eada2…` 出版監査と byte 一致・12 checks PASS・status third-independent-geometric-reconstruction-passed）。兵站的事実として宣言ノートに記録した。
4. **単一オーナー宣言**: `research/log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification-single-owner-note.md`（宣言時刻 2026-11-20T14:53:03Z・commit `75fde9d8` 14:53:32Z 出版）。
5. **harness実装と実行**: `scripts/verify_k1148_reexec_third_20261120.py`（stdlibのみ・fail-closed・3 pin 内蔵・引数 --root/--output/--timeout・監査JSONは sorted keys で時刻・実行時間を含まない）。
   - pin gate 3/3 PASS（machine・fixture・published audit）
   - pristine 再実行 4 回: same-cwd-1 / same-cwd-2 / isolated-tree-1（隔離tree複写+隔離cwd+隔離HOME）/ isolated-plus-hashseed-random（+PYTHONHASHSEED=random）。全4回 returncode 0・出力 byte 一致（4,418 bytes・`526eada2…`）・parsed object 一致。実行時間各約4.2秒（監査には記録せず・推進にのみ使用）。
   - tamper gate PASS: fixture offset 1552 を XOR 0x01 で改変（`dd3f3c48…`）→ returncode 1・出力未書込。pin が改ざんを捕捉。
   - harness決定性: 同一cwd 2回 + 隔離cwd/隔離HOME 1回の 3 実行で監査 byte 一致（`312966e8…`・3,613 bytes）。
6. **part1 出版**: commit `760c506230e7fee39b0d08591a7bb3d267d1c5e2`（14:56:39Z）。実験dir 3ファイル（README・harness・監査正本）。fetch-back: 同 commit の raw CDN から再取得し harness `6f016cd1…`・audit `312966e8…` がローカル監査と cmp 全一致。
7. **part2**: 本item K1153 + 本ログ。push 直前に K1153 が空きであることを確認（main `e635b55dec` 時点で item ファイル Not Found）。remo レーンが K0919 実験dir（14:57:42Z `e635b55dec`）を出版したが本レーンとの競合なし。

## 観察

- 出版機は 906,752 個の結合列挙を約4.2秒で処理（出版レーン報告と同水準）。決定性は隔離tree・hash randomization でも崩れず、出版機が環境依存（時刻・乱数・cwd・HOME・hash seed）の出力を含まないことを第三者が確認した。
- tamper test は「pin 鎖が運用上実際に改ざんを止める」ことの動作確認であり、K1149 レーンが knowledge README の SHA-256 1文字転写を fail-closed pin で捕捉した実例と整合する。
- 本検証は幾何の内容に新知見を追加しない。K1148 の監査正本が pin byte の取得と再実行のみで第三者がどこでも再現可能であることを測定したことが本レーンの成果である（独立検証可能性の別実行者による確定）。

## 引継ぎ（次回）

- 並走レーンの未着地: fold26 receipt fold（宣言 `23bffdd4e4`）・round-5 refsolve（宣言 `ace38772d9`）・WIN8証明書抽出（宣言 `63877ffd2e`）。着地すればその正本の第二検証が最優先候補。
- K1149 二重採番の解消（six-row レーンの再採番）は six-row レーン待ち。本レーンは触れない。
- 同種の第三検証の余地: K1147（外部第二検証・71チェック機）、K1149（K1146全probe再実行機）、K1151（K1146 whole-record照合機）も pinned byte 取得 + pristine 再実行で第三検証可能。次回の候補。
- remo レーンの K0919 full-record period characterization（part1 14:57:42Z 着地済み）のitem着地も注視。

**本検証は残余23行のどの行も閉じない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
