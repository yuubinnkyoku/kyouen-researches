# 安全な子D4同値の低石数例外を完全分類

K0421を補完する全nの必要十分分類・正確なBurnside補正・例外数公式。
数学的証明は [proof.md](proof.md)、既存実装をimportしない独立有限照合は
[audit.cpp](audit.cpp)、保存出力は [audit.json](audit.json) にある。

```sh
g++ -std=c++17 -O3 -Wall -Wextra -Werror \
  research/experiments/safe-child-quotient-exceptions-20261013/audit.cpp \
  -o /tmp/safe-child-quotient-exceptions-audit
/tmp/safe-child-quotient-exceptions-audit 11 \
  > /tmp/safe-child-quotient-exceptions-audit.json
```

保存出力のJSON整形は意味に影響しない。n=1〜11のサイズ0〜3全親を直接検査し、
形による分類だけから検査対象を生成する方法は用いていない。
一般位置の四分回転軌道から一点または隣接二点を選び、中心を任意に加えた親だけが
例外となる。例外では安定化群が自明で、二つの合法手が一組だけ余分に合併する。
11盤では例外親がサイズ1・2・3に80・160・80個、D4類では10・20・10個ある。
