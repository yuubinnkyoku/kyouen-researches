---
id: K1034
title: 2トークン残余ゲーム z=15・y=3境界切片の全Grundy分類
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: [two-token z15 y3 boundary slice]
relations:
- type: depends_on
  target: K0832
  note: A/B/C再帰、高さのみ縮約、一般tail、Theorem Tを使用する
- type: depends_on
  target: K1032
  note: B子の評価とx=3帰納基底にz=15・y=2全称定理を使用する
- type: depends_on
  target: K1030
  note: C子の評価にz=14・y=3全称定理を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-z15-y3-boundary-20261119/report.md
  role: proof
  note: x外帰納と全Rを覆うA/B/C署名帯表による全称証明
- path: research/experiments/vertical-fiber-two-token-z15-y3-boundary-20261119/verify_z15_y3.py
  role: verifier
  note: 二つの直接mex再帰、K1032/K1030子アンカー、署名帯・mex・低R・tailの監査
- path: research/experiments/vertical-fiber-two-token-z15-y3-boundary-20261119/output/audit.json
  role: data
  note: 13,825,925照合・不一致0・二回実行byte-identicalの決定論的監査結果
- path: research/experiments/vertical-fiber-two-token-z15-y3-boundary-20261119/census_z15_y3.py
  role: verifier
  note: x=3..45・R=0..x+45の生二再帰センサス（二エンジン一致・閉形式一致・tail）で行表を第三導出から照合する
- path: research/experiments/vertical-fiber-two-token-z15-y3-boundary-20261119/output/census.txt
  role: data
  note: センサスの決定論的出力（二回実行byte-identical）
- path: research/log/2026-11-19-vertical-fiber-two-token-z15-y3-boundary.md
  role: log
  note: 最新main確認、切片選定、全称化、監査、次の未解決範囲
scope: >-
  κ=1残余ゲームH(R;(x,y);z)の2トークン族における固定高さz=15、y=3、
  全x>=3・全R>=0。Grundy値0/1/2を完全分類する。
evidence: >-
  xに関する外帰納。A子は同じz=15,y=3切片のx-1行、B子はK1032(z=15,y=2)、
  C子は1 xor K1030(z=14,y=3)で評価する。x=3では二つのトークン減少手が
  同じ(3,2);15多重集合子に合流し、K1032のx=3行を基底とする。
  x=3..20の過渡署名帯表とx>=21奇数/x>=22偶数の定常署名帯表が全R>=1を
  互いに素に被覆し、各帯のmexが本文のT/Pを与える。K0832からR<=16の
  高さのみ縮約、R>=x+19の一般tailも従う。二直接再帰・子アンカー・署名帯・mex・
  Theorem T・縮約・tail・固定seed散点の監査は13,825,925点で不一致0。
  全称性の根拠はx外帰納と全R署名帯表であり、有限監査はその転写・実装照合である。
---
