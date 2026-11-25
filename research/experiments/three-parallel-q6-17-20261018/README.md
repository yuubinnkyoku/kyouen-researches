# Three parallel lines, q=6: 17 candidates suffice

`proof.md` proves that for any three distinct parallel lines, with at least
17 distinct candidate points on each, every maximal safe configuration has
15 stones, so `g(S)=(15-|S|) mod 2`. The candidate points need not be
uniformly spaced or integral. The optimal uniform threshold remains unknown.

Two independent implementations audit the exact finite reductions:

```sh
python research/experiments/three-parallel-q6-17-20261018/verify.py
python research/experiments/three-parallel-q6-17-20261018/verify_e13.py
c++ -std=c++17 -O2 research/experiments/three-parallel-q6-17-20261018/audit_independent.cpp -o /tmp/q6_17_audit
/tmp/q6_17_audit
c++ -std=c++17 -O2 research/experiments/three-parallel-q6-17-20261018/audit_e13_independent.cpp -o /tmp/q6_17_e13_audit
/tmp/q6_17_e13_audit
```

The exact finite enumeration is part of a mathematical proof by reduction,
not a numerical extrapolation from bounded integer grids.
