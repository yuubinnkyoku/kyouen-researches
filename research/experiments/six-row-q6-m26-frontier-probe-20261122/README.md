# six-row (6,6) 6×26 frontier probe — class{2} krow=2:4+minpos=11（2026-11-22）

## 主張

なし。本実験は cap 到達 honest negatives の記録のみを出版する。M_{6,6}∈[26,495]（K1217）は不変で、
6×26 の在・不在いずれの主張もしない。

## 経緯とスコープ

単一オーナー宣言: `research/log/2026-11-22-six-row-q6-m26-frontier-probe-single-owner-note.md`
（commit `05785cdf`・2026-11-22T01:55:27Z・宣言時 main HEAD `a37a4825`）。

K1217 が 6×25 witness（class{2} krow=2:4+minpos=11 分解・SAT 3,574,244 conflicts）で frontier を
6×26 に更新した直後に、同一 H-split の m=26 第1 datapoint を採った。宣言スコープは cap 260s の
単一 probe であったが、260s probe が 6×25 SAT の conflicts（3,574,244）に肉薄する
3,555,947 まで到達したため、壁の直後の SAT の可能性を排除するため同一インスタンスの延長
1200s cap を追加走査した（追加分は records.jsonl の note 明記・本 README/session log に経緯記録）。

## 走査結果（いずれも cap 到達 INDET・honest negative）

| run | cap | conflicts | process-time | 日時 (UTC) |
|---|---|---|---|---|
| probe | 260s | 3,555,947 | 259.52s | 01:55:38 → 01:59:59 |
| extended | 1200s | 14,704,926 | 1198.01s | 02:00:08 → 02:20:08 |

- CNF: 決定的再生成（`node scripts/sat3.js 6 26 6 --class=2 --krow=2:4 --minpos=11 <out>.cnf`）・
  sha256 `cc150fa0966226cfb26ea681ab11df24c708b8509324fe55968d469a26276a5c`・
  vars 58,722 / clauses 205,674（`enc/` の meta 参照）。
- 機材: K1215/K1217 出版正本 sat3.js（sha256 `e04581eb…` 照合）・kissat 4.0.4 官バイナリ
 （sha256 `21da5d98…` 照合）。

## 観察（設計メモ・不在主張ではない）

- 同一 H-split は 6×25 では 3.57M conflicts で SAT したが、6×26 では 3.56M（260s）でも
  14.70M（1200s・RSS 85 MB）でも cap 到達のまま。frontier 幅 6×26 の追い込みには、この分解より
  更に細かい分割（minpos 別点の掃引・krow 行位置の追加分割・class{1} 側 krow=1:1..1:3 系への
  並行拡張・6×25 witness からの bounded surgery 系）が必要な見込み。
- conflicts 数は勝敗ではなく、探索費用の概観である。

## 誠実性の文言

- INDET は cap 到達の有限計算記録であり、いかなるクラス・幅の不在も主張しない。
- 標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーン非接触で UNKNOWN のまま。
- 再現: 上記 CNF 生成コマンド（sha 一致を確認）+ kissat 4.0.4（生ログは `output/`・
  要約行は `output/records.jsonl`）。
