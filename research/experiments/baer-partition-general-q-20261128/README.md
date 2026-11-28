# Baer partition (Bruck) general-q — 独立機械検証 q=2..9 と disjoint Baer 対 witness

- 宣言: `862293aa` (HEAD pin d2d3c398・publish-then-execute)
- Amendment 1 (実行前出版): `f359c5c5` — witness size 算術誤りの訂正
  (PG(2,64) <= 146 (134は誤り), PG(2,81) <= 182 (166は誤り))
- 種別: 高速レーン (K1373 「次の接続」の一般 q での disjoint Baer 対存在・Baer partition 文献接続)

## 主張の区別

1. **引用定理 (Bruck)**: PG(2,q^2) の Singer 群 <g> に対し <g^(q^2-q+1)> の点軌道は
   q^2-q+1 枚の disjoint Baer 部分平面 (各 PG(2,q)) の分割をなす。
   (Nagy et al. 2024, arXiv:2403.13734v2 Lemma 2.4 / J. Combin. Des. 2024,
   DOI 10.1002/jcd.21956; Bruck による古典的結果として参照)
2. **自前の有限機械検証 (定義直接・全数)**: q = 2,3,4,5,7,8,9 の各 q で
   GF(q^2) を2方式で独立構成し、Singer 部分群軌道分割が
   (a) q^2-q+1 軌道 × サイズ q^2+q+1・disjoint・総和 q^4+q^2+1、
   (b) 各軌道が Baer 性 (全直線との交差 1 または q+1 点・(q+1)-secant が
       ちょうど q^2+q+1 本) を満たす、ことを検証。
3. **結果 (有限・witness)**: 軌道0,1の union = 2(q^2+q+1) 点の t=2 ブロッキング
   witness。PG(2,9) <= 26・PG(2,16) <= 42 (K1373 再現) に加え
   **PG(2,25) <= 62, PG(2,49) <= 114, PG(2,64) <= 146, PG(2,81) <= 182
   (いずれも 3q^2 未満)** が新規。
4. **系 (証明つき)**: 分割の k クラスの union は k 重ブロッキング
   (k <= q^2-q+1) — 各直線は各 Baer クラスと >=1 点で交わり、クラスは disjoint。
   機械検証: k=2 全 q・k=3 (q=4, min 交差 3)。
5. K1373 の条件付き補題「disjoint Baer 対が存在する PG(2,q^2) では
   min <= 2(q^2+q+1) < 3q^2 (q>=3)」の存在条件は、Bruck の定理により
   **すべての素体冪 q で充足される** (文献接続。自前の全称証明ではない)。
   min の下界は主張しない (PG(2,9) は [19,26] のまま)。

## 検証バッテリ (各 q・両実装)

- design 検査: 点数 = 直線数 = q^4+q^2+1、各直線 q^2+1 点、各点 q^2+1 直線、
  2直線はちょうど1点で交わる (N<=400 は全数、それ以外は seed 固定 2,000 サンプル)。
- 生成元の位数完全検証 (gamma: E* の位数 Q^3-1、K* 内での Singer 商の位数
  がちょうど N: gamma^N ∈ K* かつ gamma^{N/d} ∉ K* for all prime d | N)。
- Baer 性・witness 判定は全直線に対する全数判定 (bitmask popcount)。

## 実装

- `scripts/baer_partition_impl1.py`: GF(p^{2m}) → K[t]/(3次既約多項式) の塔。
  点 = E*/K* の剰余類 {gamma^i K*}、Singer 部分群軌道 = Z_N の step q^2-q+1 剰余類。
- `scripts/baer_partition_impl2.py` (独立): GF(p^{6m}) を GF(p) 上直接構成、
  部分体 K' = <gamma^{(Q^3-1)/(Q-1)}> を内部から列挙 (Frobenius 不動点で全数確認)、
  beta ∉ K' による基底 {1,beta,beta^2}・GF(p) 線形代数で座標復元。
- 出力: `out/impl1_all.json`, `out/impl2_all.json` (両者の不変量は完全一致)。

## 較正

- q=2: 各軌道 = Fano 型 Baer、直線プロファイル {1:14, 3:7} (K1372 PG(2,4)
  census の 360 Fano プロファイルと一致)。
- q=3: 軌道プロファイル {1:78, 4:13}・t=2 witness 26 点の直線プロファイル
  **{2:65, 5:26} = K1373 の PG(2,9) 26 点 witness と完全一致**
  (Singer 分割由来の別の disjoint Baer 対で同じプロファイル)。
- q=4: witness 42 点 = K1373 の PG(2,16) sampling witness と同サイズ・同構成原理。

## 開示 (バグ・障害)

1. 初回スクラッチで「点 = μ-代表 (ker N の元)」のパラメータ化に理論誤り
   (K* 剰余類が μ-元を含むとは限らない・q ≡ ±1 mod 3 で失敗)。結果を出す前に
   自律検査で発見し、剰余類直接パラメータ化に修正。
2. 環境リセット 1 回 (既知の file-loss モード) で作業 tree 消滅。宣言の方法記述から
   両実装を再実装し再実行。
3. 多項式剰余の符号誤り (+v*pp[j] / 正しくは -v*pp[j]): 標数 2 でのみ偶然一致。
   再実装中に impl2 q=5 の fail-closed assert (gK^{Q-1} == 1) が捕捉 → 符号修正。
   併せて polygcd の正規化漏れ (定数 gcd を 1 と判定できず GF(5) で
   find_irreducible が全部拒否) を修正。修正後は生成元位数の完全検証を追加。
   **標数 2 の全結果は符号修正の前後で不変** (両バージョンで同一の多項式・同一結果)。
4. p odd の旧実装の結果 (修正前の q=3,5,7,9 のみ电池通過) は、モジュラス多項式が
   f でなく h = x^k - s に置き換わる混合だったが、-design 検査と Baer 电池の
   全数通過により実質 h が既約だった幸運ケース。修正後コードで全 q を再実行し、
   本キットの数値は全て修正後コードによる。

## 再現

```sh
python3 scripts/baer_partition_impl1.py 2,3,4,5,7,8,9 out/impl1_all.json   # ~59s
python3 scripts/baer_partition_impl2.py 2,3,4,5,7,8,9 out/impl2_all.json   # ~123s
```

- 実行環境: Python 3.12 (純 Python・依存なし)。出力は決定的 (seed 固定)。
- 標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・
  S2・全 closure class は全時点 UNKNOWN・verdict 不消費。
