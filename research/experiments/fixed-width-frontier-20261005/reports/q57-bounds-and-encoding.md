# 五行・7点版の境界証人と、有限排除の残り

2026-10-05（JST）。M5,8=16の決着後、隣接するw=5,q=7を調べた。
この版では行容量6、満容量30である。

今回確定した範囲は

\[
\boxed{19\le M_{5,7}\le200}.
\]

上界200は既存K0318の代入による全称上界で、新しい厳密閾値ではない。
新しい下界は5×18の次の29石安全極大証人による。

```text
y=0: 5,8,12,14,17
y=1: 1,3,6,7,8,10
y=2: 1,3,6,7,10,12
y=3: 2,4,7,9,11,14
y=4: 4,6,7,9,11,12
```

盤内90点の全三点組からprimitive整数円・直線を生成し、
各禁止曲線上の占有点が6個以下であること、全61空点に6既存点のblockerが
あることを独立確認した。各blockerはJSONに保存した。
従って安全性と極大性はSAT modelの自己申告によるものではない。

## 7点円を落とさない完全生成

M5,8の円生成は8点が全て盤内にある円だけを列挙するため、そのまま使えない。
五行内で7点以上ある円は、少なくとも二行に二点対を持つ。
根の和sは二行で等しい。行i,jの根の積をp_i,p_jとすると

```text
A=j-i
B=-s A
C=p_j-p_i-A(i+j)
D=A p_i-A i²-C i
```

が整数係数 `A(x²+y²)+Bx+Cy+D=0` を与える。
隣接行だけに限定せず、全行対の全同和二点対を走査する。
各行で二次方程式の整数根を個別に盤内判定し、重根も重複を除いて残す。
これで一つの根だけが盤内の円、接点、分母のある円も落とさない。

5×200では13,234,000点対割当から3,048個の7/8点円を得た。
小盤はその点集合をx<mに制限し、7点以上残る曲線だけを使う。
証人盤m=18の全84円は、独立の三点生成と完全一致した。

## CNFの二つの定式化

不足対象行≤5、外部行≤6、各円≤6の安全条件を課す。
初回は、空点pと既存6点集合ごとにblocker変数を作った。
再試行では、各円Cに「ちょうど6点占有」の変数を一つだけ作った。
その変数が真なら、Cの全 `(|C|-5)` 点部分集合に少なくとも一つ占有点が
あることを課す。既存の≤6条件と合わさり、ちょうど6点となる。
対象点は、占有済みか、そこを通る飽和円が一つあるかを要求する。

後者は変数数を減らし、m18の証人を5秒probe内で発見した。
これは統制した速度比較ではなく、一般的なsolver速度改善とは主張しない。

二つの短時間probeではm18〜40の外側・準外側行にUNKNOWNが残った。
一部の中央行UNSATは未DRAT監査の有限probeとして扱い、全盤の不存在にも
無界な閾値にも使わない。長さごとの単調性も仮定しない。
新しい決着方向を探す前に、同じ未完SATを長時間回すことは停止した。

## 再現

python-satはM5,8実験と同じ外部導入を使う。repoのlockfileは変更しない。

```sh
g++ -O3 -std=c++17 research/experiments/fixed-width-frontier-20261005/scripts/q57_geometry.cpp \
  -o /tmp/q57_geometry
/tmp/q57_geometry 200 > /tmp/q57_circles_200.txt
python research/experiments/fixed-width-frontier-20261005/scripts/q57_witness_check.py \
  --maximum-circles /tmp/q57_circles_200.txt
python research/experiments/fixed-width-frontier-20261005/scripts/q57_sat.py \
  --circles /tmp/q57_circles_200.txt --m 16 18 20 24 28 --seconds 5 \
  --encoding expanded --output /tmp/q57_expanded.json
python research/experiments/fixed-width-frontier-20261005/scripts/q57_sat.py \
  --circles /tmp/q57_circles_200.txt --m 17 18 20 24 28 40 --seconds 5 \
  --encoding aggregate --output /tmp/q57_aggregate.json
```

time limitの結果・model・solver統計は実行機で変わる。下界の再現は固定証人の
独立安全性・極大性検査による。次は対象行の6点blockerに共通する外部占有構造を
抽出し、単純CNFより強い必要条件へ圧縮することが価値の高い一手である。
