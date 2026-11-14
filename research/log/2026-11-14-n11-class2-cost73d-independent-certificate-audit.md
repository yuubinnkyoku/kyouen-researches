# 2026-11-14 n11 class2 cost-73d WIN7証明書の独立監査

監査入力のmain snapshot: `32fdcac33d9f06d15c0c85ab66409d5745526cac`。`AGENTS.md`、`research/knowledge/README.md`、K0023、K0783、cost-73dのsweep記録・証明書README・frontier再計算結果を確認した。

## 対象

- 6石親S6: `00000000000000809082000000004000`
- 追加手: bit 48
- 7石root: `00000000000000809083000000004000`
- 証明書: `output/class2-lane-cost73d-certificates/bit48-root-00000000000000809083000000004000.cert.part1of2` と `...part2of2`
- Git blob SHA-1: part1 `653d4a1f8cb7a75feedea626caafc448b953f17f`、part2 `b43ecb8d7f0ab8a82824a09540c5e22d99c3a7ec`

両blobを取得して連結した内容は2,408,961 bytes、非空66,682行（ヘッダー2行・戦略行66,680行）。行の昇順、重複なし、32桁hex、盤外bitなし、着手番号0..120を確認した。

## 別実装による検査

既存の `verify_bit7_win7_cert.ts` は4点の4×4 Bareiss行列式で幾何を判定する。今回追加した `scripts/verify_cost73d_win7_certificate_independent.mjs` は、3×3整数行列式から円の方程式を作り、3点が一直線の場合は直線の行列式を使う別実装である。浮動小数点は使わず、整数の安全範囲も検査する。

- 親S6は6石・安全。合法手は73手で、bit 48は合法。
- rootは親にbit 48を加えたものとbit単位で一致。7石・安全。
- rootの合法な相手初手は59手。
- 59個すべての8石sub-rootを検査し、勝者手は存在・合法、相手手番では全合法応手を展開、終局は敗者手番に限られることを確認。
- sub-rootごとの探索で訪れた勝者局面の和集合は証明書の66,680行と完全一致。欠落0・余分0。
- sub-rootをまたいだ訪問数の合計144,275、終局23,616、相手応手辺129,362。終局石数は全て13〜17。
- sub-rootごとの訪問数624〜4,659、終局数86〜806。全59件PASS。

実行結果の要点: `parentLegalMoves=73`, `addedMoveLegal=true`, `rootLoserMobility=59`, `subroots=59`, `consumedWinnerStates=66680`, `missing=0`, `extra=0`, `terminalStoneRange=[13,17]`。

## frontierへの対応

rootから1石を除いた7親をD4正規化すると、次の7軌道は相異なる。

- `00000000000000809083000000000000`
- `00000000000000809082000000004000`
- `00000000000000809081000000004000`
- `00000000000000801206000000040000`
- `00000000000000808083000000004000`
- `00000000000000003801000400000020`
- `00000000000000009083000000004000`

公表されたcost-73d frontier JSONの `marginal_manifest_hexes` 3件は、上の7軌道のうち `00000000000000809082000000004000`、`00000000000000801206000000040000`、`00000000000000003801000400000020` と一致した。公表frontierはこのrootについて7 covers・6 marginal・3 in-manifestと記録している。今回独立に照合したのは7親軌道と3 manifest keyであり、全worklistの再計算や6 marginalの判定までは再実行していない。

公表されたafter-cost73d frontierは、manifest内解消S6 920、残りS6軌道6,927、残合法七石手コスト545,068、open classが必要とするS6 5,196・コスト408,718、最良class-2候補11軌道・コスト771、最良class-4候補18軌道・コスト1,460。これらは公表再計算結果の引用であり、本監査が全件を再計算した数値ではない。

## 限界

- この検査が確認するのは上記7石rootのWIN7戦略証明書だけ。cost-73d sweepの残り72候補のREFUTED-D10記録、抽出節点25,261,945、`fbt_drops=0` は再実行していない。
- REFUTED-D10は深さ10以内のWIN7が見つからなかったという意味であり、S6のLOSS証明ではない。
- 7石rootとそのS6親の被覆は、S5親やblocker全体、二石root、空盤の勝敗を決めない。
- K0783の条件付き閉鎖はK0675のオラクル前提を引き継ぐ。標準11×11空盤、二石root `{49,60}`、S2 `{59,60}` は引き続きUNKNOWN。

再実行例（実験ディレクトリを作業場所にする）:

```sh
node scripts/verify_cost73d_win7_certificate_independent.mjs \
  output/class2-lane-cost73d-certificates/bit48-root-00000000000000809083000000004000.cert.part1of2 \
  output/class2-lane-cost73d-certificates/bit48-root-00000000000000809083000000004000.cert.part2of2
```

この監査は証明書本体の検査と局所親子対応の照合であり、S2または空盤の勝敗主張ではない。