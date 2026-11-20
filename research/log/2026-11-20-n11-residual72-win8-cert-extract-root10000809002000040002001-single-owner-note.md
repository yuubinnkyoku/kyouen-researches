# n11 残余23行 WIN8-D10 root 10000809002000040002001 証明書抽出の単一オーナー宣言（2026-11-20）

宣言時点の main: `e9ea153bc469aa551689a5d275773553852f3342`。
対象K項目: K1146（残余23行の代替9根depth-10掃引）。

## 着手する課題

K1146で新たに得られたWIN8-D10 candidate
`00000000010000809002000040002001`（8石・両AND順序uncapped loss=true・
nodes 608,293 / 691,784・主張3行）について、既存のn11-terminal-strategy-v1
WIN8抽出器を再利用し、完全戦略証明書を盲抽出する。抽出後は、探索器から独立した
BigInt 3×3余因子展開、Bareiss 4×4整数行列式、Python標準ライブラリ第三走査で
独立検証する。

## 方法と受入条件

- K1146掃引正本SHA-256
  `e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`、
  runner v17 Git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59` を固定する。
- rootの8石・quadruple-free・合法初手集合を整数幾何で独立再導出する。
- 既存WIN8抽出器の探索核を保ち、全合法初手を盲抽出する。初手ごとのfresh process
  2回と全初手一括1回の計3実行で証明書bytesが一致することを要求する。
- fbt_drops=0、fatal/conflict=0、capped=0、全初手成功、行重複の選択手衝突0を要求する。
- BigInt / Bareiss / Python第三方法で、合法手、winner/loser局面、全loser応手辺、
  終端（loser-stuckのみ）、終端石数範囲、消費戦略行unionが全数一致し、
  missing=extra=0であることを要求する。
- 監査正本を別作業場所で再実行しbyte-identicalを確認する。

## 範囲外・非主張

- 本宣言は当該8石rootの証明書抽出と独立検証のみ。S6行のreceipt被覆・fold、
  行閉鎖、他のWIN8 root抽出は含まない。
- K1146のWIN8-D10 probe事実を証明書に変換する作業であり、新たな勝敗判定ではない。
- REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

本課題の抽出・独立検証・成果出版の単一オーナーは本宣言の著者とする。
