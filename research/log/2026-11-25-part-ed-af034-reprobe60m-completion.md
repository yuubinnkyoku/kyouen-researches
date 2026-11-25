# Part ED 完了: af034 (class 34908・EXHAUSTED@30M 残) 60M 再probe は fresh exact LOSS 32,012,059 に解決 (2026-11-25)

単一オーナー Part ED・publish-then-execute、全 wave 完了。wave 毎の
publish + fetch-back blob sha1 照合は以下のとおり全て一致した。

| wave | 内容 | commit |
|---|---|---|
| A | 宣言log | `8cc8ed0c` |
| A2 | amendment (detached 起動・cross-invocation 監視。予算・規約は不変) | `2a0c3318` |
| B | kit 23 files (blob sha1 23/23 一致) | `15e973e6` |
| C | outputs 15 files (blob sha1 15/15 一致) | `2b996b81` |
| D | README 最終化 + MANIFEST rev2 (両ファイル一致) | `25f636cd` |
| E | 本完了log | (本 commit) |

## 結果 (honest label・verdict 不消費)

- **af034 = (1152921504607911937, 68719476736) (stones=5・legal=95・
  s5 index 930660・class 34908 境界子) は BUDGET 60,000,000 条件で
  result=2 (LOSS)・nodes=32,012,059 (wall 176s / 180s)。two-pass
  fresh-cold node-exact。**
- 32,012,059 は予算区間 (30M, 60M] にあり、exhaustion 履歴は
  15M EXH → 30M EXH → 60M LOSS。宣言条件5どおり fresh 解決として
  記録する。将来 Part (Part EE 相当) の pinned loss-only adoption
  候補となる。
- **verdict は本 Part では不消費。** canonical cache (`cecc1a0f…`
  6,665行) への採用・class 34908 unknown 7→6 の反映は採用 Part が
  別途行う。
- **class 34908 は unknown 7 のまま。標準 11×11 空盤・19 central-reply
  roots・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 もすべて
  UNKNOWN のまま。** nodes は bookkeeping であり、勝敗・距離・
  coverage の主張ではない。

## 実行・検証記録 (詳細は実験dir README run record)

- val-gate 4/4 PASS (published baseline と全 replay 列一致。at2m 2行は
  byte 一致)。anchors 3/3 PASS (af001 LOSS 2,952,432・af029 WIN
  4,862,485 WIN-HALT rc45・af039 LOSS 19,234,232 = 30M 条件値と同一、
  budget-crossing 成立)。
- audit_ed.py (`6f76e8e5…`) 58/58 gates PASS (kit pin・fresh-increment
  gate・exhaustion 履歴・node-exact・honest label)。tamper battery:
  raw node 桁改変・verdict 桁改変は fail-closed で検出。status.nodes
  桁改変は label-agnostic 設計により audit 非検出 (宣言時点で結果
  未知のため設計どおり) のため、post-result に status.log = raw p1 =
  raw p2 = audit main_probe = drive.out の 5点機械照合で
  (2, 32,012,059) 一致を確認した。
- 実装上の記録: battery 中に audit stdout redirect 先を audit スクリプト
  自身の出力ファイルに誤指定して二重書き込みが発生 (起動側のミス・
  audit_ed.py は無実)。再生成し sha256 `5473eafb…` 8,139B で確定。
- 実験dir: `research/experiments/n11-centralreply-closure-class34908-af034-reprobe60m-20261125/`
  (README run record・MANIFEST rev2 = kit 21 + outputs 15)。

## 本 Part の位置づけ

- closure frontier 上位 (class 34269 WIN 11行・5804 WIN 4行・5343
  WIN 46行 ほか) はすべて不消費 WIN で C++ gate (`9193f5b6…`)
  待ちであり、本環境では実行不能 (コンパイラ不在は今回も再確認)。
  本 Part の af034 60M 再probe が 2026-11-25 時点で本環境から
  直接進められた frontier 唯一の probe 可能残作業であった。
- af034 の採用後の class 34908 unknown 6 の残りは不消費WIN 6行
  {af023, af029, af047, af048, af050, af053} となり、すべて C++ gate
  専権 (採用 Part の reaudit で確認する)。
