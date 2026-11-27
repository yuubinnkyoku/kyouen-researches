# seven-row-q6-m32-two-edit-surgery-20261127

高速レーン・単一オーナー。宣言:
[2026-11-27-seven-row-q6-m32-two-edit-surgery-declaration](../../../log/2026-11-27-seven-row-q6-m32-two-edit-surgery-declaration.md)
(2026-11-27T08:01Z・宣言時 HEAD `d108bae0`・出版 `6070fb03`)。
publish-then-execute の下で実行。

## Headline result

- **(7,6) 前線 7×32 の完全 two-edit surgery は負**: m=31 witness
(34 石 rows [5,5,5,4,5,5,5]・出版 `m31.witness.stones.json` byte-clone)を種に
T=(31,3) 遮断を課した最終状態完全列挙は
**2,224,675 一意候補・safe かつ maximal 0 件**。
- m=31 witness の ≤2 編集 (≤2 除去・≤2 追加・最終 ≤34 石) 近傍には
7×32 witness は存在しない (**局所的負・不在主張ではない**)。
m=29→30 と同じ one-stone-short 負パターン (m=30 witness は 2 編集外で
後に class {3} SAT が発見した前例どおり、近傍外の witness の可能性は残る)。
- **M_{7,6} ∈ [32, 862] 不変** (witness 帯 m=6..31・上界 K0318 U=862)。
- T=(31,3) 曲線センサス: c4 = 1 (直線 y=3・seed 4 石 (12,3),(23,3),(27,3),(29,3)・
空セル 27)・c3 = 10。c5 T 曲線なし (T は seed で未遮断)。

## 手法

- `scripts/surgery_m32.py` = 出版 `surgery_m31.py`
(seven-row-q6-m31-frontier-20261115・完全最終状態場合分け T 占有 /
c4・t=0 1 追加 / c4・t=1・c3 2 追加・統一曲線 bookkeeping
|C∩S'| = |st_on−R| + |A∩full|)の構造 clone。
相違は盤幅 31→32・T=(30,3)→(31,3)・種 c3.stones.json→m31.witness.stones.json
・出力名のみ (diff 5 行・機械検証)。Exact Fraction 演算・census 不使用・
自己テスト組み込み。
- 列挙の完全性: 除去のみでは T を遮断できず (c5 T 曲線が存在しないため
削除で 5 に達する曲線がない)、c2 以下の T 曲線は ≤2 追加で 5 に届かない。
(m=31 レーンの証明済み場合分けと同一構造。)

## 較正・検証 (全て本 host で実施)

1. **m=31 陽性対照 (機械正再生)**: 出版 `surgery_m31.py` を byte-clone し
seed に出版 c3.stones.json (m=30 witness) を与えて 7×31 で再実行 →
出力 JSON が出版 `surgery-m31.json` と **byte-identical**
(候補 2,140,633・safe 1・witness 1・T 曲線 c4=2/c3=11)。同一機構が
m=31 では witness を再発見し m=32 では 0 件。
2. **決定性**: surgery_m32.py 2 走 → 出力 JSON byte 同一
(sha256 `5867e7de…`)。
3. **probe 較正**: 出版 `probe_free_column.py` で m=31 unblocked 0・
m=32 は (31,3) のみ (出版記載と一致)。
4. **det 検証器較正**: 出版 `verify_witness_det.js` で m=31 witness
ok/uncovered 0・rows [5,5,5,4,5,5,5]。
5. **CNF 較正**: sat3.js で (7,31,6) class {3} CNF md5
`48eb715f…` byte-exact 再生 (出版 m31 kit record と一致)。

## SAT probe 補助記録 (honest negative・不在主張ではない)

sandbox の bash call 上限 (~290s・bg process は call 終了で kill) のため
深い単一実行は不可能。以下の短 cap probe を実施した:

- (7,31,6) class {3} krow=3:4 (SAT 既知): **INDET** 1,279,251 conflicts / 250s
(cal31k4.txt)。m=31 plain は出版どおり INDET 4.37M@896s。
- (7,32,6) class {3} krow=3:4 minpos=0: **INDET** 1,240,713 conflicts / 260s
(m32k4p0.txt)。
- (7,32,6) class {3} plain CNF (156,185 変数 / 547,944 節・md5 `bc10c516…`)
を生成・出版 (深い実行は次レーン・長時間 cap 環境へ)。
- いずれも INDET は cap 到達であって不在主張ではない。

## Not claimed

- 7×32 全域の不在 (≤2 編集近傍外・多欠損クラス・他 seed は未走査)。
- 7×33 以降、(7,q≠6) 家族、Grundy 値、11×11 関連 (全時点 UNKNOWN・
verdict 不消費・nodes/conflicts は bookkeeping)。
- `results/fixed-width/mwq_stabilization.csv` の bounds 不変
((7,6) 行 note に本結果を追記)。
