# 残余78行・39-root掃引の候補供給範囲監査

2026-11-20。K1059の39-root depth-10掃引が消費した候補範囲を、出版済み正本から再監査する。

## 再現

リポジトリのルートで実行する。

```sh
node research/experiments/n11-residual78-witness39-candidate-supply-scope-audit-20261120/audit_candidate_supply_scope_20261120.mjs
```

Node.js標準機能のみを使う。4入力のGit blob SHA-1を固定し、D4正準化・7石安全性（整数行列式）・削除後の行被覆・両順序probe・pilot制御を検査する。

## 結果

- 残余行: 78
- sweep前のfresh-safe候補: 4,728
- sweepした選択witness: 39（全てREFUTED-D10）
- この39本の外にあるfresh-safe候補: 4,689
- sweep前の異なるpair辺: 706（今回選ばれなかった辺: 667）
- singleton候補を持つ行: 78（今回の39本は全て2行pairなので、singleton候補はこの掃引では未使用）

したがって、消費されたのは**選択済み39-root計画**であり、add-one-stone候補集合全体ではない。4,689本の残り候補がK0863の8,964-root全体キャッシュで既知かどうかは、この監査では結合していない。667はsweep前の異なる行ペア数であり、sweep後の最大matching値ではない。

## 限界

- 39本のREFUTED-D10はLOSS証明ではない。
- 追加候補の勝敗・深さ・完全キャッシュ上の状態は未判定。
- post-sweep maximum matchingは再計算していない。
- receiptは作成せず、S6行も閉じていない。
- 標準11×11空盤・二石root・S2・class 1/2/4はUNKNOWNのまま。
