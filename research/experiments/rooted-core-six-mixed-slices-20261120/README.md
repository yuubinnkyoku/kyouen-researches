# 6点・二点辺を含む核の三点辺本数別完全族スライス: 尾部34周期の有限窓認証（j=0..4）

[K0684](../../knowledge/items/K0684-fixed-core-path-period-thirty-four-conjecture.md)（固定核＋長道の
最終34周期予想）の未開拓域「6点・二点辺を含む核」を、三点辺（サイズ3の禁止辺）本数jによる
完全族スライスで証明する。機械・認証規則・基礎表は
[K0682](../../knowledge/items/K0682-rooted-core-path-periodicity-certificate.md)
（`rooted-core-tail-periodicity-20261107`）の正本を再利用し、
6点純三点辺全型（`rooted-core-six-pure-triple-full-20261108`）と同じ方式を二点辺混在に拡張する。
単一オーナー宣言は
[このノート](../../log/2026-11-20-rooted-core-six-mixed-slices-single-owner-note.md)。

## 定義域

- 頂点6個（根0固定）、禁止辺はサイズ2（二点辺）または3（三点辺）の最小clutter。
  どの二点辺も選んだ三点辺に含まれない（包含除去済み）。
  ラベル付き宇宙は35ビット（15ペア+20トリプル）。
- **bucket j**: 三点辺ちょうどj本＋任意の両立二点辺部分。j≥1では二点辺部分は非空
  （三点辺のみの族は既に出版済みのため除外、いわゆる mixed proper）。
  j=0は二点辺のみの全グラフ族（空clutterを含む）。
- 型は根を固定した120頂点置換の軌道（Burnside）。Burnside代表数と根付き同型型数は一致し、
  engine.canonical の正準形を正本の鍵として使う。
- 結合条件: bucket j のどの核も、核内着手で根が残る子は全て5点以下になり、
  出版済み513型基礎表（le5監査 `audit.json`・各prefix 0..1069値)で閉じる。
  したがって各jは独立に全長認証できる。

## 認証規則（K0682有限窓定理の適用）

各bucketで全型について `f(n+34)==f(n)` を比較窓 `N..2N+35`（N=max(500, 最悪周期破綻+1)）
で有限確認する。必要値は `0..2N+69`。確認すれば同じ等式は全 n≥N で従う（同定理の
二重帰納）。j=4のみ最悪破綻が570でN=571・必要値1211（拡張パス）、他はN=500・必要値1069。
末尾400値の最小周期も全型で確認し、全バケットで最小末尾周期は**ちょうど34**
（34を割る真の周期を持つ型は存在しない）。path列 p_n にも同じ窓を確認した。

## 結果（各j完全族の定理を構成する証明書）

| j | ラベル付き | 型 | joint開始N | 必要値 |最大Grundy| 独立subset照合（型×長さ0..6） |
|---|---|---|---|---|---|---|
| 0 | 32768 | 544 | 500 | 1069 | 22 | 532条件・71618安全状態・76型 |
| 1 | 81900 | 1018 | 500 | 1069 | 24 | 476条件・69163安全状態・68型 |
| 2 | 143170 | 1663 | 500 | 1069 | 33 | 399条件・60590安全状態・57型 |
| 3 | 213900 | 2336 | 500 | 1069 | 30 | 357条件・54706安全状態・51型 |
| 4 | 286755 | 3045 | 571 | 1211 | 33 | 350条件・51993安全状態・50型 |

- **j=0 は6点の純二点辺核の完全族**（全グラフ・544型）で、開始500は5点以下の
  基礎表と同じ一様上界。j=0で出た最大Grundy 22は6点でも上昇しないことを示す標本。
  これにより「6点の二点辺のみの核はすべて最終的に34周期（開始500）」が有限族の全称定理として確定。
- j=4のjoint開始571・証人 `[6, [3, 13, 22, 28, 49]]`（最終周期破綻570）は、
  純三点辺6本以下族（`rooted-core-six-pure-triple-six-edges-20261107`の732型・開始571）と
  同じ571が出現。j≤3 mixed は全て500。
- 独立照合は `mixedlib.direct`（生subset占有ゲーム。正準化・残余cleanup・道分解・
  周期拡張を一切使わない別実装）で、各bucketから辺数階層ごとに標本抽出して
  solver再帰の値と全一致。

## 位置づけと限界

- j=0..4 は「三点辺が高々4本で二点辺を1本以上含む全6点核」の全称定理を与える。
  三点辺0本（純二点辺）全型・三点辺≥5本かつ二点辺非空の型がこの後のスライスに残る
  （j=5..20。単一オーナー宣言の下、続きとして再開可能）。三点辺純正の全型は出版済み。
  したがって6点核全体の認証には j=5..20 がまだ必要。
- 認証は候補周期の証明規則であり、任意核に周期が必ず存在することの証明ではない。
- 7点以上の核、misère版、標準全正方形格子盤への実現はこの実験の主張に含まない。

## 実行環境障害と再構成（再現性に関する注記）

2026-11-20 13:20Z頃、実行環境がリセットされ、bucket機械（`mixedlib.py`・`run_bucket.py`）と
j=0..5の実行中資産が失われた（出版済みだったのは単一オーナー宣言ノートのみ）。
本実験は出版済み資産（`rooted-core-tail-periodicity-20261107` の `engine.py`・`proof.md`・
`verify.py`・`output/audit.json` をbyte-exactに再取得）から機械をスクラッチ再構築し、
失われた実行の認証済み数値（j=0..4の型数・joint開始・最大Grundy・最悪証人）をすべて再現した上で
出版した。すなわち本証明書は、独立に二度書かれた実装が同一の完全族値まで一致した
交叉検証込みの成果である。j=0..4は再構築後の実行が出した値そのものを出版する。

コードは純Python（numpyは型列挙の軌道最小化のみに使用）。乱数・時刻依存なし。
出力は決定的（keys sort・型順序固定）。各レコードは `n, forbidden, prefix_start, prefix(0..必要値)`
を持つ。型ごとの513型基礎表の値は周期拡張（500+(L-500)%34・K0682定理）で参照する。

## ファイル

- `mixedlib.py`: 35ビット宇宙・バケツ列挙・Burnside軌道型・単状態正確再帰・生subset照合。
- `run_bucket.py`: バケット実行・有限窓認証・resume機能・head/records証明書出力。
  `python run_bucket.py J [budget] [minlimit]` を繰り返し実行するとbucket Jが完全認証される
  （必要値>1069のときは拡張パスを自動で挟む）。
- `output/bucket_j{J}_head.json`: 各bucketの認証証明書（joint開始・必要値・最小末尾周期
  ヒストグラム・開始分布・標本照合件数）。
- `output/bucket_j{J}_witnesses.json`: 各bucketの結合状態（prefix_start==joint開始の全型）と
  上位worst_starts証人の全prefix（0..必要値）。全型分のrecordsは決定的再生成可能で
  SHA-256を下記にpinする。

全型recordsの再生成: 上記機械は乱数・時刻非依存の決定的整数計算なので、
`types_j*` キャッシュを空にした隔離cwdでの再実行はrecordsまでbyte-exactに再現する
（j=0で実測・SHA-256同一）。再生成コマンドはj=0..4の合計約10分。

records SHA-256（ローカル監査資産・再生成検証用pin・repoには未格納）:

- `bucket_j0_records.jsonl` … `c207ce1176f2aed131b0b5a4a4786b4198c050fcf8fdfb45d29baf0e8eef7ad3`
- `bucket_j1_records.jsonl` … `5aa12595921ce2ca37bdeaf59f24e7cac84d99843e776f0f6ce401239d8485b7`
- `bucket_j2_records.jsonl` … `6485f97599b8d135c3cec1c537944c73f7497acbe56aa776eb6c2edb54e416ad`
- `bucket_j3_records.jsonl` … `a2c32c8abc9a731de1092cee474de24dcebf30f113c00204c75d618aa664a8f3`
- `bucket_j4_records.jsonl` … `d710831c82607b2d50b14424dd319a9fadd5bcf78f9a6df70ca52d78d5310817`


witnesses SHA-256（repo格納分・証明書の実体）:

- `bucket_j0_witnesses.json` … `d44db02e3a3e3c829b1502baf65188fdad7736fecca4249cb25c964bbe28dfcd`
- `bucket_j1_witnesses.json` … `78d44978f8ae040cc62430a3ff1f1e824c2bc9b5a993d654fef1a82f258ce84d`
- `bucket_j2_witnesses.json` … `5c91d853eefaf00f8fd1ba35deeabe0a71aac6a5364ea19e1c01241ddb0f4012`
- `bucket_j3_witnesses.json` … `9e7a9c9be6ccf98d5b5a946c0d7ac2877e156a3852d1d4a3762930b37e320318`
- `bucket_j4_witnesses.json` … `85dc64b26df14647691cf46572901220bf6c86885662423567e69792ba7ba85b`

head SHA-256:

- `bucket_j0_head.json` … `b96a1dd55f82d9b1d37f5ffb1e39b5d2d1656f147f7f822dc9acd5f7ebc586bf`
- `bucket_j1_head.json` … `b0c3f80ec77a97f885425dba5fdba6eec27f36d251c86180113e4eaccb6e156d`
- `bucket_j2_head.json` … `948e905dfb6986f7e621645f5c4efa9cfb6c047f85129041c1070a47b6418571`
- `bucket_j3_head.json` … `8d715c137d2c4a6a80a51e99bb69d93a61459eb5a74c9bf349acacc5d0559e58`
- `bucket_j4_head.json` … `ea1a2491f9f088f841241a0df54ac11f9545d652ab52af3b728991ca0ee8004e`

決定性: j=0は隔離cwd再実行でrecords・headともbyte-identical（同一ハッシュ）。
全実行はseed・時刻依存なしの決定的整数計算。
