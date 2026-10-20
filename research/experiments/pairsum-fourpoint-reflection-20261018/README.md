# 4点の二点和復元：中心反射が唯一の曖昧性

`proof.md` に全称数学的証明を収録。4個の実数（重複可）の6つの二点和から、元の4点多重集合は中心反射を除いて一意に定まる。整数の場合、総和が奇数なら完全に一意。

独立の有限監査：

```sh
python3 research/experiments/pairsum-fourpoint-reflection-20261018/verify.py
c++ -std=c++17 -O2 -Wall -Wextra -pedantic research/experiments/pairsum-fourpoint-reflection-20261018/verify_independent.cpp -o /tmp/pairsum-fourpoint-audit
/tmp/pairsum-fourpoint-audit
```

これは以前の「2の冪で二点和復元が一般には一意でない」という観察を、4点の場合に完全分類する補強である。円の同一性やゲーム勝敗への直接の拡張は未証明。
