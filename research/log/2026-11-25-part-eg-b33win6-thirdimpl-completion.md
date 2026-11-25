# Part EG 完了log: closure class 34908 b33-win-6 残 unconsumed WIN 6行 第三実装交叉検証 (E1-E9 全完了)

- 2026-11-25T11:30Z (完了log作成時刻; commit timestampはGitHub側)
- 宣言: `research/log/2026-11-25-part-eg-b33win6-thirdimpl-declaration.md` (commit `2a46008a`)
- 実験dir: `research/experiments/n11-centralreply-closure-b33win6-thirdimpl-20261125/`
- 結果: **E1-E9 すべて実施・ALL GATES PASS・hard-stop なし。verdict不消化 (6行は unconsumed WIN label のまま)。**

## 出版物と固定commit

- kit 53 files: `2a46008a → 5e7217c4 → 58750d83 → a9b5fd1d → cf74b547 → 403d8fd5 → 156f8a6f → bb661fbb`
  (scripts 7 / input 11 / sources 27 / val-gate 8)
- outputs 35 files: commit `7484f63d` "eg-9: publish Part EG third-impl cross-validation outputs
  (35 files, audit 213 gates PASS x3, byte-identical)"
- README.md + MANIFEST-sha256.txt (88 files pinned): commit `1f39b1ec`
  - README.md sha256 `90b1d78217ef2a8e99ceb3bd25c414bfadbb1df556f61bf2b3970cea87d74e6a`
  - MANIFEST-sha256.txt sha256 `ed568fc7733cba14af901b35a31ff4e8ae15b9a3315b03934afe56e0107641be`
- 本完了log: research/log/2026-11-25-part-eg-b33win6-thirdimpl-completion.md

fetch-back byte検証 (固定commit raw):

- outputs 35/35: `7484f63d` 固定で各 basename を取得し sha256 を pin と照合 → **35/35 一致**
  (push直前にも payload と作業コピーの byte 一致 35/35 をローカル bash で再検証済み。
  push時は fail-closed 設計: サンドボックス内で sha256 純JS実装 + 自己テスト → 全35ファイルの
  pin 照合 → 不一致なら throw/pushしない)。
- kit 53/53: `bb661fbb` 固定の raw 取得で 52/53 sha256 一致、唯一の不一致が `scripts/make_kit_eg.py`
  (後述)。今回の完了セッションで追検証: `bb661fbb` の tree 上で 53ファイル全ての git blob sha1 を
  ディレクトリ listing から取得し、ローカル作業コピー53ファイルの git blob sha1 と比較 →
  **53/53 完全一致** (make_kit_eg.py 含む)。
- README/MANIFEST 2/2: `1f39b1ec` 固定で取得し sha256 一致。

## make_kit_eg.py pin 誤差の誠実記録

- 宣言log (2a46008a) は `make_kit_eg.py` pin を `c2f4f88bd4c3283b47dd2f5bd77e7840b65e3c680c2257dd1ce4d9b955b4d0e9`
  と記録したが、published byte は
  `faee079a62fd28926c9686dada93f03da0b746cf2c40657ade915f2213e2f5c3` (宣言後・push前のローカル
  整形で生じた 3バイト差。audit_eg.py は maker を pin していないため機能影響なし)。
- fail-closed maker 再実行 (faee079a 版) G1-G7 ALL PASS・rows.json `799d9faf…` byte-exact 再生成で
  機能同等性を確認済み。**faee079a (published) を正とする。** MANIFEST-sha256.txt にも両shaを注記。

## E1-E8 実行結果 (要約・全文は output/ と audit-summary.json)

- E1 rules gate (`verify_tbl_eg.js` → `output/rules-gate.txt`):
  `replica quads 95670 mine quads 95670` / `triples checked 195044 mismatches 0`。
- E2 val-gate fresh 4本 (2M×2 + 15M×2): published baseline と node-exact
  (host `['2000000','0','2000000']`×2, `['15000000','2','3651923']`, `['15000000','2','5040200']`)。
- E3 negatives: ng1 `GATE_FAIL,"legal count mismatch: derived=87 declared=88"` /
  ng2 `GATE_FAIL,"stone count mismatch: bits=5 declared=6"`、ともに rc=1 で fail-closed 捕捉。
- E4 anchors: k02a exp=9,106,337 / ttH=4,991,527 / l1a exp=7,660,602 / ttH=3,951,175
  (a/b det-pair 一致・published pin と一致)。
- E5 replica (pinned 2-pass fresh-cold): af029=4,862,485 (15M と 30M af029-30m の両条件で同nodes・G2c)、
  af047=9,841,975、af050=7,311,834、af053=5,182,129、af048=17,816,616@30M、af023=28,933,179@30M。
  計 7キー14pass。全て published raw と result/nodes node-exact・p1==p2 determinism。
  なお af023 は bash の実行 300s 制限のため pass を分割実行し、`output/status.log` に行を
  runner 形式で追記した (生の runner 起動は同一入力・同一budget)。
- E6 third-impl 6キー×2 run (`run_thirdimpl.sh` --cap=300000000 --wallcap=240 --memo-power=22):
  全キー a/b det-pair 一致・reason=clean・verdict 6/6 WIN (third=replica=published=1)。
  expansions: af029=5,672,478 / af047=11,706,195 / af050=8,719,439 / af053=6,071,614 /
  af048=21,512,908 / af023=34,912,368 (pass-one total 88,595,002)。
  ttHits: 3,079,849 / 6,307,523 / 4,661,490 / 3,175,645 / 11,133,246 / 17,698,726。
- E7 audit ×3 (`audit_eg.py`): **ALL 213 gates PASS・3回 byte-identical**
  (`output/audit-summary.json` sha256 `73af060a4c139818e0e4625ed511945394169afca6ad704eec8c4c6b4bcfc7bf`)。
  audit-summary.run1-3.json は byte-identical のため main には audit-summary.json のみを出版した
  (3回実行の事実は status.log と本logが記録。要再現時は audit ×3 を実行して byte 比較)。
- E8 tamper battery (実 kit 上・計5件、全て期待 gate が rc=1 捕捉):
  t1 input csv 改竄 / t2 rows.json pin 緩和 / t3b replica nodes+1 / t4 targets verdict flip /
  t5 replica result flip。wall_s 系の改竄は設計どおり非検出 (runlimit は NOT a verdict)。
  battery後 pristine 再実行 ALL PASS。

## assertions (主張の限定・不変担保)

- **verdict 不消化**: 対象6行 (af029/af047/af050/af053/af023/af048) は honest unconsumed
  probe-level WIN label のままで、本Partでは一切採用していない。adoption は
  scrutiny owner C++ 第二実装 gate `9193f5b6…` 通過後・pinned merger `90711961…` 経由の
  別 adoption Part 専権。
- C++ 第二実装 gate は本 sandbox に g++ がなく未実施 (宣言log既記載の環境制約)。
  第三実装は JS (third_impl.js)。
- **標準11×11空盤・19 central-reply roots・二石root・S2・class 1/2/4/30345/34908 は
  本Partの前後を通じてすべて UNKNOWN のまま。** nodes/expansions/ttHits を勝敗や距離として
  読まないこと。closure class 34908 は 6 unconsumed WIN children を残したまま。
- 並走レーン (Part EF batch-38 / Part EH batch-39 / rooted-core pure-triple / K1316) が同時期に
  main を進めたが、本Partの実験dir と buffer 競合なし。outputs push 直前の EG dir HEAD は
  bb661fbb のまま (単一オーナー維持)。

## 次回レーンへの引き継ぎ候補 (本Part scope外)

- scrutiny owner の C++ gate 9193f5b6 実行環境がある場合の af029/af047/af050/af053/af023/af048
  個別検証は本訳ではなく C++ 第二実装レーンの判断。
- Part EG 派生の追加実験は新規実験dir + 新規宣言 log で行うこと (本dir は kit/outputs 固定)。
