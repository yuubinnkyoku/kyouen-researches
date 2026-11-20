# 研究ログ: 残余72行 replace9 whole-record第二検証（K1151）pristine 再実行第三検証（2026-11-20）

## 経緯（時系列）

1. **最新main確認・着手判断**: 着手時の採番状況は K1150（general-multiset mergeレーン・先着）・K1151（自レーン・replace9 whole-record第二検証）・K1152（y12 two-token再採番）・K1153（自レーン・zero triple provider reexec・出版済み）・K1154（remo K0919周期特徴付け・remoが宣言時仮番号K1153から後着規則で自ら再採番）まで埋まり。K1155 を自レーンの次成果に割り当てた。
2. **対照の前提**: K1151（出版 commit `f7aa541f342d67b33f34fee2df5e31c262cb0691`・14:41:19Z）の実験dir `n11-residual72-replace9-whole-record-second-verification-20261120/` は13ファイル（検証機 `e92fb755…`・出版監査 `5888afb3…` 115,002 bytes・10入力snapshot）が単一dirに自己完結し、引数なし・1実行0.2秒未満。出版監査はpin+入力のみから新規再生成可能な設計。
3. **staging**: pinned commit の raw CDN から検証機・出版監査・10入力snapshot（`.input-k1085/k1086/k1089/k1091/k1095/k1097/cover-decision/probe-records-replace9/k1147-external-audit.json` + `.input-probe-records-replace9.jsonl`）を取得。検証機内部のfail-closed pinが全入力を照合。
4. **事前 probe**: 宣言前に 1 回 pristine 再実行（0.16秒・returncode 0・334 gate PASS・出力 byte 一致）。兵站的事実として宣言ノートに記録。
5. **単一オーナー宣言**: `research/log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification-single-owner-note.md`（宣言時刻 2026-11-20T15:06:08Z・commit `f3097440c0ca5021018c0f4fdbb55cb2fb2fee09` 出版）。
6. **harness実装**: `verify_k1151_reexec_third_20261120.py`（stdlibのみ・fail-closed・検証機/出版監査2 pin内蔵・監査JSON sorted keys・時刻・実行時間を含まない）。初期実装の clone_tree に makedirs バグを発見し修正（修正後 SHA-256 `cf1ae8ba…`・11,144 bytes）。
7. **全gate実行**:
   - pin gate 2/2 PASS + 10入力sha記録
   - pristine 再実行 4 回: same-cwd-1 / same-cwd-2 / isolated-tree-1（隔離tree複写+隔離cwd+隔離HOME）/ isolated-plus-hashseed-random（+PYTHONHASHSEED=random）。各実行前に監査を除いた新規生成。全4回 returncode 0・334 gate all_pass=True・出力 byte 一致（115,002 bytes・`5888afb3…`）。1実行あたり0.2秒未満。
   - tamper gate PASS: `.input-replace9.json` offset 7701 を XOR 0x01 で改変（改変後 `74e25aa4…`）→ returncode 1・出力未書込。
   - harness決定性: 同一cwd 2回 + 隔離cwd/隔離HOME 1回の 3 実行で監査 byte 一致（`6e06f12a…`・5,024 bytes・status k1151-reexec-third-verification-passed）。
8. **part1 出版**: commit `d6832fc58524e97dde889efe0d20f7cec71e91df`（15:07:32Z）。実験dir 3ファイル（README・harness・監査正本）。K1155 空きを raw CDN 404 で再確認後に出版。
9. **part1 fetch-back**: 同 commit の raw CDN から再取得し、harness `cf1ae8ba…`（11,144 bytes）・監査 `6e06f12a…`（5,024 bytes）が staging 正本と curl + sha256sum で全一致（cmp 等価）。run_typescript 内の自作 sha256 実装はサロゲートペア処理で数bytesの計数差を出したため、権威ある検証は curl + sha256sum で実施した。
10. **part2**: 本item K1155 + 本ログ。push 直前に K1155 item が main に存在しないことを再確認。

## 観察

- 出版正本 115,002 bytes が、GitHub からの pinned byte 取得のみ（輸送・転写・ローカル記憶を介さない）で 0.2秒未満/回・4環境（PYTHONHASHSEED=random 含む）で新規再生成・byte一致することを出版レーン外の立場で確定した。K1151 実験dirの自己完結設計（入力snapshot同梱）が第三検証のコストを数秒に抑えた。
- tamper test は「pin 鎖が運用上実際に改ざんを止める」ことの動作確認。squeeze 対象の `replace9` 入力そのものの1 byte 改変を確実に捕捉した。
- 本検証はgame-theoretic内容に新知見を追加しない。334 gate は出版s5/s4記録の整合照合の再実行であり、残余72行のどの行も閉じない。

## 引継ぎ（次回）

- 並走レーンの未着地: fold26 receipt fold（宣言 `23bffdd4e4`）・round-5 refsolve（宣言 `ace38772d9`）・WIN8証明書抽出（宣言 `63877ffd2e`・root `00000000010000809002000040002001`）。着地すればその正本の第二検証が最優先。
- 同種第三検証の残り候補: K1147（8根被覆判定外部第二検証・71チェック機・入力5正本が別dir散在）・K1149（18 probe再実行機・runner_v17.ts git blob必要）。
- K1149 二重採番（replace9 reexec先着 14:30:20Z vs six-row後着 14:31:45Z）は未解消のまま管轄外。

**本検証は残余72行のどの行も閉じない。標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
