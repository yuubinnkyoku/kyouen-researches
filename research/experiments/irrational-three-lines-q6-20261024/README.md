# 無理数間隔の三線q6：有理高さ13候補定理と全長を解ける二次無理数帯

[全証明](proof.md)。

* 有理数高さ・無理数間隔比なら、各線13候補で全終局15石、全安全局面の偶奇Grundy値。
* x={0,1,(1±√17)/2}、整数高さ0..m−1なら、全長m≥1で終局石数3min(m,5)。
  全局面の偶奇式、P長はm=2,4のみ。安定化開始値は厳密に5。
* さらにα²−α−c=0でc=1、素数p≥5、または素数平方p²の無限族も同じ全長強解決となる。

```sh
uv run --locked python research/experiments/irrational-three-lines-q6-20261024/run.py --cxx g++
```

Windowsで必要なら `--cxx C:/msys64/ucrt64/bin/g++.exe`。
一時バイナリをコンパイルし、Q(α)の全六点組判定と公式をm1..10で照合。
m1..7の全1977032安全局面を二方式のmexで点ごとに比較し、`audit.json` に保存する。
無理数を浮動小数点で近似しない。未知盤の長時間探索ではない。

無限族の有限監査6例を再現する場合：

```sh
uv run --locked python research/experiments/irrational-three-lines-q6-20261024/family.py --cxx g++
```

c=1,4,5,7,9,11の計6619338六点組・12036931安全局面を `family-audit.json` に保存する。

除外したc=3も別途解決した。満容量安定化値は厳密に7、P長はm2,4,5だけ。
m6は終局14・15が混在しSG最大3なので、偶奇式の代わりに全局面DPを独立照合する。

```sh
uv run --locked python research/experiments/irrational-three-lines-q6-20261024/exception.py --cxx g++
```
