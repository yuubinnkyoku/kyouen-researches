# run log: 低z banded 窓+2/窓+3 行の全称崩壊定理群（K1278 仮採番・z=0/z=1 窓拡張）

- 作成: 2026-11-24（Vibe 高速レーン・定時自律実行）
- 関連: 宣言ノート
  `research/log/2026-11-24-lowz-window2-banded-single-owner-note.md`
  （commit `4185ed7767694cb5db7957a4d76a3832bc03716f`・publish-then-execute）
  ・実験 dir `research/experiments/lowz-window2-banded-20261124/`
  ・K item `research/knowledge/items/K1278-lowz-window2-banded-rows.md`

## 1. 選定

- K1270（lowz banded window extension・2026-11-23 出版）report の残部 open
  「z=0 では窓+2 までの拡張候補がさらに存在する可能性・次課題」を最初の
  候補として選定。
- 当該帯は z∈{0,1} のみでストリップレーン（K1272-K1277・z10 以降）と
  非接触・証明も短時間で閉じる見通し（選択肢集合一致型 + 底の吸収）で、
  高速レーンの基準（短〜中時間・厳密・完結可能）に合致。
- 事前に GitHub API で K1277 までの出版と対抗宣言を確認し K1278 を
  仮採番（z10 レーンが先行取得した場合は後着再採番の規約）。

## 2. 宣言前探査（全開示規約）

- `probe_w2_predecl.py`（sha256 `586c2246ae3561a2d1af296c388885c56a3520a83d152c6ce1914c1810a8940d`）
  ・出力 `probe_w2_predecl_out.json`（sha256 `3326e4d9509f2d628484e2668143efd3193c310242942bd9304cd5df4705315b`）。
- P1 Z1 grid 3,108点・P2 Z0 grid 518点・P3 T_A 固定 632点・P4 T_B 固定 584点・
  P5 T_A 乱数 456点・P6 T_B 乱数 432点・P8 窓+3 z=0 観測 292点・
  P9 窓+3 z=1 観測 264点、全 bad 0（engine pin `bd5f22e4…` 一致）。
- 宣言ノート §6 に全開示（宣言前探査の値は主張の seed としてではなく
  falsifiability 確認として使用）。

## 3. 宣言出版（publish-then-execute）

- 宣言ノート（主張 3 定理 + 2 補題・証明全文 §2・protocol D0-D9 の事前登録・
  受入条件 4・観測 HEAD-before-push `7e079e6a`）を commit `4185ed77` で
  出版（2026-11-24T02:56:23Z）。
- fetch-back byte 照合 sha256
  `14bdd4da6615d7a5d6c60aba088f0403e89c83be269bbdb360c68abe79dbb1f8` 一致。

## 4. 機体組立

- `verify_lowz_window2.py`（30,272B・sha256 `ea114de3ef0e7b6e965af5c43aa2939d95681604bb46a640e74c96dedebc5703`）。
- engine block（2,508B・pin `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`）は
  `build_engine_from_published.py`（sha256 `26b81a0bdc85c326dc9e741ff3a2745acbc29d8c5ee16445055970607c27b64f`）で
  出版 10 ソース（K1264 検証器・K1268/K1270/K1271/K1272/K1273/K1274/K1275/K1276/K1277 機）
  + 自機の **11 方 byte 照合**（PROVENANCE PASS・手転写ゼロ）。
- 誠実記録: build_engine_from_published.py 初稿の SRC8_PIN 定数表記が
  K1276 機の sha（`cdc47219…`）ではなく K1268 機の sha と同一視される
  誤り（実 sha 計算と照合し出版前に修正・照合ロジック・engine byte は
  不変）。修正後の機体 byte について 11 方照合 PASS。

## 5. 公式監査（宣言出版後）

- 公式実行 rc=0・**OVERALL PASS・39,148点 / 65,265比較 / bad 0**。
  D0 単一アンカー 26,117/52,234・D1 Z1 3,108・D2 Z0 518・D3 T_A 1,170・
  D4 T_B 1,100・D5 T_A3 1,100・D6 構造検査 5,170・D7 出版アンカー 51・
  D8 深部乱数+sampling 814。
- **宣言総計（宣言ノート §4）と実測が総計・全 check とも完全一致**。
- D9 境界記録（判定外・総計外）: m=1 z=0 窓+3 3分離・m=2 z=0 窓+3
  10行全分離・m=2 z=1 窓+2 8/10分離・窓+4 z=0 / 窓+3 z=1 各 225点 0分離
  （観測のみ・主張しない）。

受入条件の成立（宣言 §5 の 4 条件すべて成立）:

1. 公式実行 rc=0・OVERALL PASS・宣言総計と完全一致。
2. 決定性: 4 実行（同一 cwd×2・隔離 tree/env -i・別 HOME・
   PYTHONHASHSEED=random）で audit.json（5,434B）sha256
   `18f35044cef257d8ad6cecd4b9b58d9832aefb955b5ce8cfa339bc88329cfc57`
   が全実行で一致。
3. tamper 電池: 8 変異（M1-M8）すべて捕捉 rc=0（M1: 516・M2: 2・
   M3: 3,096・M4/M5/M6: 各 46・M7: 16・M8: 2 bad）。
4. provenance: 11 方 byte 照合 PROVENANCE PASS・engine pin
   `bd5f22e4…` 一致。

## 6. 出版（この実行）

1. 実験キット 6 ファイル（report.md・verify_lowz_window2.py・
   build_engine_from_published.py・probe_w2_predecl.py・
   probe_w2_predecl_out.json・output/audit.json）を
   `research/experiments/lowz-window2-banded-20261124/` に 1 コミット出版
   （commit `16bb60f`）。
2. 出版直後の curl fetch-back sha256 照合で 6/6 ファイルがローカル検証済み
   原著と byte 一致（report `bb029a3d…`・verify `ea114de3…`・build
   `26b81a0b…`・probe py `586c2246…`・probe json `3326e4d9…`・audit
   `18f35044…`）。
3. K item + 本 run log を 1 コミットで出版（このコミット）。
4. knowledge README への K1278 bullet 純 append（別コミット・latest main
   再取得後）。

## 7. 規約

- branch / PR は作成せず main に直接反映。push 前に最新 main を再取得し
  K 番号・パスの衝突がないことを確認（出版時点の items Dir は K1277 まで・
  K1278 実験 dir / K item / log はいずれも不在を直接パス probes で確認）。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。検証点数を勝敗として読まない。
- z>=2 の窓+1 梯子（K1272-K1277）・K1268 C1 バンドの z>=2 帯・z10
  ストリップレーンには一切非接触。残部 open（窓+4 z=0 / 窓+3 z=1 の底分類・
  z>=2 の窓+2 行・min=1 行の窓+2 一般則）は K item scope に登録済み。
