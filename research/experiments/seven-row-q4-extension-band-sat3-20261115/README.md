# seven-row-q4-extension-band-sat3-20261115 — sat3 streaming census による (7,4) 構成的延伸帯 m=28..35 の SAT 再検証

Date: 2026-11-15
Lane: 高速レーン（seven-row-q4-q6-witness-frontier-20261115 の後続）
Status: COMPLETED

## 目的

`seven-row-q4-q6-witness-frontier-20261115` で記録された **sat2.js 全三つ組census の
メモリ壁**（7×28 q=4 で OOM rc 137、node heap 2560MB）を解消し、K0827 構成的延伸帯のうち
**tsVerify のみだった m=28..35 を SAT + 2系統検証に昇格**すること。

## 手法: sat3.js（streaming census）

sat2.js からの変更点は3点のみ（counter / totalizer / lexLeader / CLI は verbatim）:

1. **節のストリーム出力** — `enc.clauses[]` に全節を JS 配列で保持し
   `toDimacs()` で GB 級の結合文字列を組む sat2.js の設計（OOM の主因）を廃止。
   `<out>.body` にバイト列を chunk flush し、最後に header を前置して chunked copy。
   DIMACS は sat2.js と **byte-identical**。
2. **円の初遭遇処理** — circMap の挿入順 = 三つ組列挙順でその場で counter を emit。
   clause 順・変数番号とも sat2.js と同一。
3. **円の点走査を O(w) 化** — 全点走査の代わりに行ごとの2次方程式の整数根求解
   （row-major 昇順を保持、点集合は全点走査と同一）。
   冗長な co 配列を保持せず、正規化キー (A,B,C,D) の Set のみ。

### 検証（controls_sat3.json）

- **byte-identity**: 9対照 `(5,12,4) (5,15,4) (6,10,5) (7,12,4) def` /
  `cap+seq` / `cap+tot` / `lex=H,V,HV` / `rowY` / `(4,14,6)` で **9/9 cmp MATCH**。
- **公開recordとのmeta一致**: (7,22,4)=40543/437624/1458224、(7,23,4)=46141/497139/1656195、
  (7,23,5)=4438/89001/311126 — いずれも curves/vars/clauses 完全一致
  （sat2.js は本実験のコンテナでは 7×22 で既に OOM するため直接 byte-diff 不可。
  小規模 byte-identity + 本ファミリー幅での end-to-end 再現で代替）。
- **kissat較正**: (7,5) m=23 → **1,200 conflicts bit-exact**（公開recordと同一インスタンス）。
- **witness再現**: (7,4) m=22..27 再実行 → 全幅 0 conflicts・**デコード石配置 6/6 公開
  witness と一致**（CNF bit-identity の強力な間接証拠）。

## 結果: m=28..35 全幅 SAT — K0827 帯の4系統検証完了

| m | conflicts | 石数 | rows | jsVerify | pyVerify |
|---|---|---|---|---|---|
| 28 | 36 | 20 | [3,2,3,3,3,3,3] | PASS | PASS |
| 29 | 59 | 20 | [3,2,3,3,3,3,3] | PASS | PASS |
| 30 | 249 | 20 | [3,2,3,3,3,3,3] | PASS | PASS |
| 31 | 94 | 20 | [2,3,3,3,3,3,3] | PASS | PASS |
| 32 | 256 | 20 | [2,3,3,3,3,3,3] | PASS | PASS |
| 33 | 537 | 20 | [3,2,3,3,3,3,3] | PASS | PASS |
| 34 | 214 | 20 | [3,2,3,3,3,3,3] | PASS | PASS |
| 35 | 160 | 20 | [3,3,3,3,3,2,3] | PASS | PASS |

- 全 witness は sat.js verifyConfig（js）+ Python Fraction（py）の2系統で
  safe + maximal + 行欠損 PASS。CNF 生成 3.1〜5.2s、kissat 3.9〜16.3s
  （m=35: 5,510,073 clauses / CNF 103MB / gen 5.2s / sat 16.3s）。
- **行構造は全幅でマルチセット {3,3,3,3,3,3,2}（20石）** — K0827 構成的延伸の
  [3,3,3,3,3,3,2] と同一マルチセットで配置が異なる独立 certificate。
  m=22..27 では SAT witness は構成 witness と石配置まで完全一致していたのに対し、
  m=28..35 では配置が異なる（いずれも同じ事実の有効証明）。
- **lex 交差確認**: m=35 は `--lex=H,V,HV` 別符号化（1,657,786 vars / 5,514,228 clauses）
  でも SAT（314 conflicts・witness 20石 [2,3,3,3,3,3,3]・2系統検証 PASS）。

## スコープ

有限機械検証。m=28..35 の各幅で SAT witness のデコード+2系統検証に成功したことは、
**これらの幅における行欠損極大配置の存在の完全証明**である。
構成的延伸（tsVerify）と合わせ、**m=22..35 全帯が4系統検証済み**
（kissat SAT + jsVerify + pyVerify + tsVerify）。
m ≥ 36 は未実施（不在主張ではない）。(7,4) の前線は 7×36 のまま
（M ∈ [36, 1929]）。sat3 により (7,4) 帯の SAT 探索は m=36 以降も
（生成~6s/幅・CNF~110MB/幅）実行可能になった。UNSAT 主張には
各幅 200s cap を超える長時間実行または構造論証が必要。

## ファイル

- `scripts/sat3.js` — streaming census 生成器（sat2.js 互換・全モード対応）
- `scripts/leanband4.sh` — 1インスタンス実行パイプライン（sat3 + kissat + 2系統検証）
- `scripts/controls_sat3.json` — byte-identity 対照・較正の記録
- `output/records.jsonl` — m=28..35 の8レコード + m=35 lex 交差確認1レコード
- `output/calibration.jsonl` — m=22..27 q4 再現6レコード + (7,5) m=23 較正1レコード
- `witnesses/s7x28q4.witness.json` .. `s7x35q4.witness.json`（+lex版）— デコード済み witness
- `raw-logs/` — 代表5本の kissat ログ（model 行は容量削減のため除去。
  model は witnesses/ の石配置として保存）

records.jsonl / calibration.jsonl のレコードは leanband4.sh と同一のコマンド列
（ad-hoc loop 実行）で生成した。cnf_md5 は各 CNF の md5（CNF は実行後削除）。
