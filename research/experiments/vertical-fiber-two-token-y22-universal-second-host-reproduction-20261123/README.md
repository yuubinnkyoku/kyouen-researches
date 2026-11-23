# y=22 two-token 全称検証器の第二ホスト独立再現（vertical-fiber-two-token-y22-universal-second-host-reproduction-20261123）

実験日: 2026-11-23（毎時並走の高速レーン・兄弟実行）
対象: `research/experiments/vertical-fiber-two-token-y22-universal-proof-20261123/`
（機体item **K1257**・被昇格命題item **K1256**・単一オーナー宣言 `e1e60cd4`・
出版 commit A `6360bb32`・機体 SHA-256 `96d9787f…`・53,422B・単一機体14チェック版）。

本実験は、K1257 に出版時点で正直記録された制限
「**兄弟実行による独立再現は出版時点でまだ存在しない**（単一ホスト出版・
4実行byte-identical + fail-closed電池12種が昇格の根拠）」を解消する、
第二ホストでの独立再現である。**新しい全称主張は一切行わない。**
K1256 昇格の証拠基盤を1ホストから2ホストへ拡張する検証のみを行う。

## 何をしたか（要約）

1. **出版corpusの取得とpin検証**: 出版実験dir 12ファイルを commit-pinned raw URL
   で取得し、機体 `96d9787f…`・転写源 pins（y=21機 git blob `ca5e8284`
   53,269B・`cand21.py` blob `38613e92` ・`cand22.py` blob `fd50358e`）が
   すべて一致することを確認（git blob SHA は取得bytesから算出して照合）。
2. **出版bytesの第二ホスト段階再実行**: 転写検査→preflight→census
   （生成器+SHA pin体裁）→12チェック電池→フル14チェック電池を出版bytesの
   まま再実行し、**全7出版出力が byte 再現**した
   （census.txt 791,080B・SHA pin `3275cc74…` 再現・misses 11,469,227 /
   hits 22,466,349 の engine cache states も再現）。
3. **宣言レシピからの自前ビルド**: 出版 y=21 機+出版 cand corpus だけから、
   失敗閉鎖型変換表（rename 表・定数/文脈置換表・全置換の発生回数assert付き）
   で y=22 機を自前構築（46,170B・SHA-256 `88ce3ed1…`・決定論的2回再構築一致）。
   出版機体と**AST同一**（docstring/comment差のみ・`ast_compare.py` rc=0）。
4. **自前ビルドの全段階再実行と決定性**: 転写検査 PASS・preflight PASS
   （12,012+9,108点 bad 0）・census byte同一・**4実行 byte-identical**
   （3同一cwd + 1回は隔離tree/env -i/HOME=/isolated/PYTHONHASHSEED=random での
   全pipeline完全ゼロ再生成、engine states まで同一）。
   12チェック/フル14チェック監査は出版監査と
   **`verifier_sha256` フィールドのみ**異なる（機体bytes差 `88ce3ed1` vs
   `96d9787f` 由来。flat-key差集合の機械検証で確認）。全点数・全 bad 数は
   完全一致（総 6,956,320点・型 797,559・merge 887,200 / tail 191,158）。
5. **fail-closed tamper 電池（自前harness・スクラッチコピーのみ）**:
   12探針すべて rc=1 で捕捉、**観測 bad 数は出版電池の値と完全一致**
   （census欠落/行削除/重複注入の各FAIL-CLOSED・P/T改ざん各 bad 1・
   C11r tail反転 bad 3,920・アンカー誤結合 C1d bad 14,869・lowRずれ
   bad 9,108・merge境界 bad 59・clip窓 C4 bad 945・tail偶奇反転
   C1 4,898/C2 24,024・band偶奇改ざん C1 1,763/C2 24,451）。
   各探針後に正典bytes・出版bytes・scratch出力の完全性を再検証（全probe後OK）。

完全な数値・SHA表は `output/reproduction-record.txt`（machine-readable）・
電池の全記録は `output/battery-results-ALL.json`。

## 誠実記録（harness側の事故1件）

P04（P-set改ざん）の初回変異は、census集合表記がカンマの後に空白を
持たない（`P={1,3,...,43}`）ことに気づかず `, 43`（空白入り）を探索して
不成立→結果として要素削除でなく余計な波括弧を付加する無効変異だった。
この場合も機体は不正行をint解析失敗で fail-closed（rc=1）したが、変異自体が
意図と違うため harness 側の瑕疵として正直記録し、有効変異で即再probeした
（bad=1捕捉・`battery-results-ALL.json` の `P04-census-P-tamper`〔無効変異の記録〕
と `P04b-census-P-tamper-valid-reprobe`〔有効再probe〕の両方を保存）。
これは出版電池自身のmerge境界探針no-op事故（runlogに正直記録済み）と同型の
事故であり、同じ方式（正直記録+有効版での即再検出）で処理した。

## 再現コマンド

```sh
# 1) corpus取得+pin検証（commit-pinned raw URLで）
#    verify_y22_universal.py の SHA-256 が 96d9787f… であることを確認
# 2) 出版bytesの段階再実行
python3 scripts/check_transcriptions_y22.py        # PASS
python3 scripts/preflight_c1d_y22.py               # 12,012+9,108 pts bad 0
python3 census_rows.py                             # census.txt 3275cc74… (791,080B)
python3 verify_y22_universal.py                   # 12-check battery (5,664,680 pts)
python3 verify_y22_universal.py C11 C11r           # full 14-check (6,956,320 pts)
# 3) 自前ビルド（本dirのbuild_y22_own.py・出版y21機+出版cand corpusから）
python3 build_y22_own.py                           # 46,170B・88ce3ed1…
python3 ast_compare.py                            # AST-IDENTICAL, rc=0
# 4) fail-closed電池（スクラッチコピーのみで動作・正典bytesは無改変）
python3 battery.py                                 # 12探針すべて caught rc=1
```

## 解釈規約

本実験は既存の出版成果（K1256 proved 昇格・K1257 機体）の**独立再現**であり、
status の変更・新しい主張は行わない。標準11×11空盤・二石root {49,60}/{59,60}・
S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。3トークン以上・y>=23族・
固定幅・q点版安定化長は本レーンの範囲外。nodes数等を勝敗として読まない。

## 関連item / log

- K1257（機体item・本実験で「単一ホスト出版」の正直記録に第二ホスト再現を追記）
- K1256（被昇格命題item・昇格証拠基盤が2ホスト化）
- run log: `research/log/2026-11-23-two-token-y22-second-host-reproduction.md`
