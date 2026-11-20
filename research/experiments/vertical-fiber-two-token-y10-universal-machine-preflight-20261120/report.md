# y=10 two-token 汎用証明機械 — 予備検査（machine pre-flight）

単一オーナー宣言（[y=10 skeleton single-owner note](../../log/2026-11-20-y10-two-token-skeleton-single-owner-note.md)）に基づく
y=10 族第2段階。[K1141](../../knowledge/items/K1141-two-token-y10-parametric-closed-form-fit.md)（cand10 有限 fitting,
status: observed）の次段階である正本検証器 `verify_y10_universal.py`（12チェック・両 raw エンジン・census・
3回 byte-identical・observed→proved 昇格・CI step）の**構築前の信頼性予備検査**である。

本成果は pre-flight であり全称証明ではない。生存は正本着手の必要条件であって十分条件ではない。
K1141 は本検査後も status: observed のまま（昇格は正本監査の全 PASS 後）。

## 検査の狙い

正本機械の構成要素が互いに整合し raw 再帰に錨で固められていることを、正本を書く前に確認する:

1. cand10 が選択肢分解 mex 恒等式 `cand10 == mex(opts)` を満たすこと（B子 = cand9〔K1138 y=9 全称〕・
   x=10 は (9,10)≡(10,9) 合流子）を主グリッド・深窓・x=10 エッジで検証
2. 選択肢分解そのものが raw エンジンの子供集合と一致すること（C3）
3. x=10 縫い目の子値 cand9(z,10,R-1) が raw 両エンジンの (9,10)/(10,9) マルチセットと一致すること（C1b）
4. 本検査が用いる cand9 転写（K1138 fit 出版 cand9.py から）が K1138 出版検証器
   verify_y9_universal.py 内の cand9 表と意味的に同一であること（C1c）
5. merge 系（x<=z-11）と tail 系（R>=x+z+11）の系命題が訪問領域で成り立つこと

## 方法・転写の正本（provenance）

- `preflight_y10.py` は自足型（import 依存なし・Python 3.12・pure Python・決定論的・clock なし）。
  転写はすべて出版正本から SHA-256 付きで取得して機械的に抽出:
  - cand10 表〔Y=10・q_odd・single_token_val・in_T10・_bk・in_P10・cand10〕: 逐語〔K1141 出版
    `cand10.py`（SHA-256 `7c08e065d1278e9e90e4f748a2f7a8a6406318618ac06d259659233387427163`）〕
    （fit self-check driver は持ち込まず・表定義のみ）
  - cand9 表〔Y9・q_odd9・in_T9・in_P9・cand9〕: 逐語〔K1138 fit 出版 `cand9.py`
    （SHA-256 `6c3e9242b5650db01b463545308e4ad9c48d06c52943f9258cb3fe176e6ad093`）〕に
    モジュール名の機械的置換 Y→Y9・q_odd→q_odd9 のみ適用（本体は不変）。
    出版の -99 overlap sentinel は保持（本検査では -99 子値は bad として可視化）
  - cand9V 表〔in_T9V・in_P9V〕: 逐語〔K1138 出版検証器 `verify_y9_universal.py`
    （SHA-256 `299acb6a70b9625310a3397a10f809879ba4a10a97e965115615d83f46c9171b`）内の
    cand9 表〕に置換 Y9→Y9V・in_T9→in_T9V・in_P9→in_P9V のみ適用
  - raw 両エンジン H_ordered / H_canonical: 逐語〔同 K1138 検証器の出版 census-line 転写〕
- 正本機械の実装時は、cand9 転写を K1138 出版検証器から採る規約（y=1..8 正本と同じ手続き）に従い、
  C1c の両コピーが意味一致することをもって fit 版との差がないことを機械的に前担保する。

## 結果（全 bad 0・全部 4 回実行で byte-identical・約 1.6 秒/回）

| check | spec | points | bad | overlap/sentinel |
|--|--|--|--|--|
| C2a | 恒等式グリッド z=0..40, x=10..56, R<=x+z+36 (+merge,tail) | 171,503 | 0 | 0 / 0 |
| C2b | 深z窓 z∈{60,72,84,96,108,120,240,400}, x=10..80, R∈[x+z+1,x+z+40] | 22,720 | 0 | 0 / 0 |
| C2c | 深x窓 x∈{70,80,100,150,240,400}, z=0..40, R∈[x+z+1,x+z+40] | 9,840 | 0 | 0 / 0 |
| C2d | x=10 エッジ z=0..60, R∈[x+z+1,x+z+70] (+merge,tail) | 4,270 | 0 | 0 / 0 |
| C3 | 閉形式子供集合 == raw 子供集合（生子列挙）, z=0..12, x=10..22, R<=30 | 5,070 | 0 | - / 0 |
| C1b | (9,10)=(10,9)=canonical == cand9(z,10,R), z=0..30, R<=55 | 1,705 | 0 | - / 0 |
| C1c | cand9 fit コピー == 検証器コピー（T/P 表・重複フラグ一致）, z=0..40, x=9..80, R<=x+z+40 | 308,484 | 0 | 0 |
| merge 系 | x<=z-11 ⇒ cand10 == single_token_val(x+10,R) | 41,300 | 0 | - |
| tail 系 | R>=x+z+11 ⇒ cand10 == (x+10)%2 | 78,182 | 0 | - |

`overall: PASS`（total_bad = 0）。実行出力の正本は `output/preflight_output.txt`。

## C1c の副産物（出版された cand9 の2コピーの意味同一性）

K1138 の2つの出版本文（fit 実験dir の `cand9.py` と検証器内の cand9 表）は、
奇z in_P9 の d=-7 行（fit: `b4 or R>=z+11` / 検証器: `b5 or R>=z+11`）と d=-5 行
（fit: `b5 or R>=z+12` / 検証器: `b6 or R>=z+12`）で接頭 b_k が1段違い、
かつ sentinel（fit: -99 / 検証器: fail-closed assert）が異なる**文本差**を持つ。
前者2つは行尾条件による吸収で意味同一（b5 の追加点 R=z+11 は R>=z+11 に含まれ、
b6 の追加点 R=z+13 は R>=z+12 に含まれる）。C1c が z=0..40・x=9..80・R<=x+z+40 の
308,484 点で T/P 表の完全一致（重複フラグ込み）を機械確認した。
正本 y=10 検証器の cand9 転写（検証器テキストから採る規約）に対し、
本 pre-flight で用いた fit 版転写がこの差を除いて同一であることがこれで担保される。

## 精度上の注意

- すべて有限 Box での不一致ゼロであり、全称証明ではない（正本監査が行う）。
- C2a〜C2d の恒等式は閉形式どうし（cand10 vs cand9）、C3/C1b が raw 錨、
  正本では C1（両エンジン全 box）・C1d（出版固定 z 切片アンカー）・C4（型機械）・
  C7〜C9（遠方・境界・シェル）・C11（raw census）が加わる。
- single_token_val の merge 使用は z>=S+1 分支のみ（x<=z-11 の行では z>=x+11>S が常に成立）。

## 再生

```
python3 preflight_y10.py    # 全チェック → overall: PASS（output/preflight_output.txt と同一出力）
```

- `preflight_y10.py`（SHA-256 `fbc86eaac8105768f9c2a325b7f37904ae4c41c2991ff31975f4b75d9ac2b20a`）
- `output/preflight_output.txt`（SHA-256 `33420c1243e8266b7ceb238c94957c3b5a61c2e9548834d69249cc139763fe68`）

## 次段階（正本出版・単一オーナー宣言の対象）

1. `verify_y10_universal.py` を y=8/y=9 正本と同一構造で構築（C1/C1b/C1d/C2/C2b/C3/C4/C7/C8/C9/C11/C12。
   C1d は出版 z=8/9/10〔y>=9 切片〕・z=15/16/17〔y>=6 切片〕の y=10 特殊化を再転写。
   cand9 は K1138 出版検証器から逐語〔C1c で差がないことを前担保済み〕。
   C4 型機械の clip 窓 ±22・番兵 ±23〔clip 窓族式候補 2y+2 の 6 族連続 tight 判定〕）。
   3回実行 byte-identical。
2. `census_rows.py`（y=10 版, z=0..79, x=10..70, R<=x+z+12, 両エンジン）を正本実験dir に作成し実行。
3. 全 PASS の場合 K1141 を observed→proved に昇格（family claim: H(R;(x,10);z) == cand10
   everywhere, + merge/tail 系）として出版し、CI audit step を追加。README・K1141 item・log 更新。
4. push 前の最新 main 再取得・並走レーンとの競合確認は不変の方針。
