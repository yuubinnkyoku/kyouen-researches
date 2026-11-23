# min>=3 banded window extension: critical strip z in {2,3,4} (K1272)

- 作成: 2026-11-23（Vibe 高速レーン・定時自律実行）
- 宣言ノート（publish-then-execute）:
  `research/log/2026-11-23-min3-banded-strip-z2z4-single-owner-note.md`
  （commit `4be51cb6`、sha256 `7df23272…`）。**証明の全文は宣言ノート §2 にある。
  本 report は機械監査の記録であり証明そのものではない。**

## 1. 主張（要約）

残余ゲーム H(R;X;z)（K1138 再帰・K0832 単一トークン閉形式 v）について:

- **Lemma U**: H(2;{1}∪Y;0)=0（Y≠∅・min(Y)>=2）、H(2;{1};0)=1。
- **Lemma F**: F(s,z):=H(z+2;{1}∪Y;z)（Y は ΣY=s の 1..4 トークン>=3 分解・白紙可）
  は分解に依らず z∈{1..4} で閉形式表に一致する（宣言ノート §1 の表）。
- **Lemma R2**: H(z+3;{2}∪Y;z)=v(s+2,z,z+3) が z∈{0,1,2,3} で成立
  （z∈{2,3} が本実験の新規部分。z∈{0,1} は K1270）。
- **Lemma D**: D(s):=H(7;{2}∪Y;4) は D(0)=0・D(3)=1・D(4)=2・D(s>=5)=1。
  崩壊は丁度 Y=(4,) で破れる（D(4)=2 ≠ v(6,4,7)=1・D式からの算術帰結）。
- **Theorem T-B**: 全 m>=3・z∈{2,3,4}・min(X)=m で
  **H(z+m+1;X;z)=v(ΣX,z,z+m+1)**。
  K1270（z∈{0,1}）と併せ、m=3 ではバンド z<z*(3)=5 全域が確定し
  **K1268 予想 C1 の m=3 行が完全解決**する（m>=4 の上位帯 z>=5 は引き続き open）。

鋭さ: m=3・z=5 は前線 witness (4,3)@R*=9（親2 vs 単一0）で分離し T-B の
z<=4 は最適。m=2 拡張は偽（(2,2)@z=2・親2 vs 単一1）。min=1 は
T1/T2（K1267/K1269）により窓+1 で分離。

## 2. 機械監査（宣言 protocol 実行結果・2026-11-23）

機体 `verify_min3_banded_strip.py`（sha256
`009184eff1accbaa82cdea9eea5e81253252e6d3681e893b1fd30506d6acad9c`）。

| check | 内容 | 宣言点/比較 | 実測点/比較 | bad |
|---|---|---|---|---|
| D1 | Lemma U: トークン2..9多重集合 arity1..4 494形状 + {1} | 495 / 1,485 | 495 / 1,485 | 0 |
| D2 | Lemma F: z∈{1..4}・s∈{0}∪{3..40}・全分解 3,657/z | 14,628 / 43,884 | 14,628 / 43,884 | 0 |
| D3 | R2 z∈{0..3} 崩壊 + z=4 D式 + deviant集合=={(4,)} | 1,650 / 4,951 | 1,650 / 4,951 | 0 |
| D4 | T-B grid: m∈{3..8}×z∈{2,3,4}×222形状 | 3,996 / 11,988 | 3,996 / 11,988 | 0 |
| D5 | 固定seed 20261234・乱数深部 20形状/(m,z) | 360 / 1,080 | 360 / 1,080 | 0 |
| D6a | 出版 witness アンカー17（K1270 D0b と同一表・5比較/点） | 17 / 85 | 17 / 85 | 0 |
| D6b | 本定理アンカー23（R2(4) deviant・Dセル・C(3,4)・Uセル・F表14） | 23 / 69 | 23 / 69 | 0 |
| D7 | 選択肢集合検査 m∈{3..6}×z∈{2,3,4}×33形状 | 396 / 1,188 | 396 / 1,188 | 0 |
| **総計** | | **21,565 / 64,730** | **21,565 / 64,730** | **0** |

- 宣言総計と実測が完全一致（不一致なら rc=1 の fail-closed 設計）。
- D6c census（判定外・記録のみ）: m∈{4..7}×z=5×96形状 = 384点/768比較。
  engine 不一致 bad=0。崩壊観測 96/96・全4 m（**観察記録であり主張しない**。
  z=5 帯 m>=4 の崩壊は open のまま。C(4,5)〜C(7,5) grid のみ）。

### 変異電池 B1-B12（--tamper）: 12/12 捕捉

| 変異 | 捕捉 bad | 変異 | 捕捉 bad |
|---|---|---|---|
| B1 U値反転 | 494 | B7 m=2拡張 witness (2,2)@z=2 | 1 |
| B2 F(s,2) 0→2 | 218 | B8 z=5拡張 witness (4,3)@z=5 | 1 |
| B3 F(s,3) 2→0 | 217 | B9 engine C手XOR除去 | 53 |
| B4 F(s,4) 0→1 | 216 | B10 q_odd 腐敗 | 570 |
| B5 D(4) 2→1 | 1 | B11 中間枝 (R+z+1)%2 | 11,640 |
| B6 R2(4) 崩壊誤主張 | 1 | B12 D7 A値窓外 | 198 |

### 決定性

audit 4 実行（同一 cwd×2・隔離 tree×1・env -i 別 HOME + PYTHONHASHSEED=random）
で `output/audit.json` が byte-identical
（sha256 `c199946ad562fb7b20f20272a261a58d31cbebc61b7b6caba4c4335c83094af9`）。
audit.json に時刻・乱数（固定 seed 以外）を含まない。

## 3. Provenance（engine block）

`build_engine_from_published.py`（sha-gate）: 出版 K1264 検証器
`108fdd65…`・出版 K1268 機 `0ab66665…`・出版 K1271 機 `1ce7df23…` の
3 ソースから cut（K1264 は行デリミタ cut・他は ENGINE BLOCK マーカー cut・
末尾空行 strip）、3方 byte 一致 + engine pin `bd5f22e4…`（2,508 bytes）
照合で機体へ byte-exact 挿入手順を検証する（手転写ゼロ・fail-closed）。
実行結果: `PROVENANCE PASS`（3ソース pin OK・four-way byte-identical・
engine pin 一致）。機体のエンジン block cut は 3 出版源のそれと同一
sha256 `bd5f22e415a78368…`。

## 4. 誠実記録

- 宣言前の探査実行（手転写 engine による census_strip/census2/census3/
  census4 の4種・うち1度 sandbox OOM kill と1度の timeout 打ち切りを含む）は
  宣言ノート §6 に全開示済み。宣言点数・比較数・deviant 期待は protocol 定義
  からの算術計算であり、探査実行の数値を参照していない。
- 機体組立は placeholder への機械挿入（assemble 手順）で行い、転写事故なし。
  最終自己検証（挿入後の再 cut == engine block）で確認済み。
- 本監査は宣言ノート出版（commit `4be51cb6`）**後**に実行された。
  監査の所要は各実行約 19 秒。
- 有限機械監査は証明ではない。全称主張は宣言ノート §2 の紙面証明
  （有限 z-梯子 F/R2/D + 選択肢集合一致 + m に関する帰納）による。

## 5. 効能と残務

- **効能**: 予想 C1（K1268）の m=3 行が完全解決。K1270 の残部
  「z>=2 クリティカルストリップ」のうち z∈{2,3,4} を min>=3 で解決。
  F セル（{1}∪Y・混合 arming）が初めて閉形式に落ちた点が、min=1 行
  （K1271）との接続ポイント。
- **残務（open）**: m>=4 の帯上端 z*(m)-1>=5（E3(z) 梯子の z=5 延長が必要。
  D6c は grid 観測 384/384 崩壊・反例不在を記録するが証明しない）。
  D-cell の z>=5 構造（census では z>=5 で複数 deviant）。F/R2/D 梯子の
  一般化（m=2 行の z>=2 前線以遠）。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 はどの時点でも **UNKNOWN** のまま。nodes 数・wall 秒数を
  勝敗として読まない。

## 6. ファイル

- `verify_min3_banded_strip.py`: 機体（audit / tamper 両モード）
- `build_engine_from_published.py`: provenance sha-gate
- `output/audit.json`: 監査結果（機体 sha256 自己記録入り）
