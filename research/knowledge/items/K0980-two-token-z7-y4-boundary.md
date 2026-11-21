---
id: K0980
title: "2トークン残余ゲーム z=7, y=4 境界切片の全Grundy分類"
kind: proposition
status: proved
topics: [grundy, residual-games]
aliases: []
relations:
- type: depends_on
  target: K0832
  note: "残余ゲームHの定義・A/B/C再帰・Theorem T・単一トークン閉形式・高さだけの縮約・高R tail定理（R>=x+12）を使用する"
- type: depends_on
  target: K0979
  note: "B子の評価にz=7,y=3境界切片の全Grundy公式を使用する"
- type: depends_on
  target: K0880
  note: "C子の評価にz=6,y=4境界切片の全Grundy公式を使用する"
- type: supports
  target: K0976
  note: "z=7のy>=4候補式の全称証明（S=x+y強帰納）に必要な境界切片のうちy=4を供給する"
artifacts:
- path: research/experiments/vertical-fiber-two-token-z7-y4-boundary-20261118/report.md
  role: proof
  note: "固定z=7,y=4・全x>=4,R>=0のGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明"
- path: research/experiments/vertical-fiber-two-token-z7-y4-boundary-20261118/verify_z7_y4.py
  role: verifier
  note: "直接多重集合再帰とA/B/C再構成（B=K0979・C=K0880アンカー）の照合・署名帯表・K0832 tail定理照合・Theorem T偶奇検査を行う独立有限監査器（2回実行byte-identical必須）"
created: 2026-11-18
tags: [two-token, vertical-fiber, z7, y4, grundy, universal, infinite-family]
---

# K0980: 2トークン残余ゲーム z=7, y=4 境界切片の全Grundy分類

抽象残余ゲーム \\(H(R;(x,y);z)\\)（\\(x\\ge y\\ge1\\)、\\(R\\ge0\\)、降下禁止）の固定 \\(z=7,y=4\\) 切片について、全 \\(x\\ge4\\)・全 \\(R\\ge0\\) のGrundy値を確定した。

## 主張

偶奇区間記法 \\(E,O,I\\) を本来の定義どおり用いると:

- 値2位置 \\(T_7^{(4)}(x)\\): \\(x\\in\\{4,5,6,8,9,10\\}\\) で \\(\\{1,3,5,7\\}\\)、\\(x=7\\) で \\(\\{1,3,5,7,13\\}\\)、\\(x=11\\) で \\(\\{1,3,5,7,15\\}\\)、\\(x=12\\) で \\(\\{1,3,5,7,15\\}\\cup O[17,23]\\)、\\(x\\ge13\\) で \\(\\{1,3,5,7,15\\}\\)。
- 値1位置 \\(P_7^{(4)}(x)\\): \\(x=4\\) で \\(\\{8,10\\}\\)、\\(x=5\\) で \\(\\{8,10\\}\\cup I[12,\\infty)\\)、\\(x\\in\\{6,8\\}\\) で \\(\\{8,10,12\\}\\)、\\(x\\in\\{7,9\\}\\) で \\(\\{8,10,12\\}\\cup I[14,\\infty)\\)、\\(x\\in\\{10,12\\}\\) で \\(\\{8,10,12,14\\}\\)、\\(x=11\\) で \\(\\{8,10,12,14\\}\\cup I[16,\\infty)\\)、\\(x\\ge13\\) 偶数で \\(\\{8,10,12,14\\}\\cup O[17,x+11]\\)、\\(x\\ge13\\) 奇数で \\(\\{8,10,12,14\\}\\cup O[17,x+10]\\cup I[x+12,\\infty)\\)。
- tail: \\(R\\ge x+12\\) で \\(H=(x+4)\\bmod2\\)。

## 証明構造

\\(R\\) に関する強帰納。\\(x=4\\) では2つの減少手が同一子 \\((4,3)\\) に合流し、子は \\(\\{\\)K0979の \\(x=4\\) 行\\(,\\ 1\\oplus\\)K0880の \\(x=4\\) 行\\(\\}\\)。\\(x\\ge5\\) ではA手（\\(x\\to x-1\\)、族内帰納）・B手（\\(4\\to3\\)、K0979）・C手（\\(z\\to6\\)、K0880の \\(1\\oplus\\) 値）にK0832のTheorem T・偶奇規則・高R縮約tail定理 \\(R\\ge S+|X|+z-1=x+12\\) を組み合わせ、全 \\(x\\ge4\\) の \\(1\\le R\\le x+11\\) を覆う選択肢署名表（\\(x=4..13\\) 個別行 + \\(x\\ge14\\) 統合行）で確定する。

独立有限監査: 10種4,142,990照合点・不一致0・二回実行byte-identical。SHA-256は実験dirのreport.md・audit.jsonに記録。

## 意義

- \\(z=7\\) の境界 \\(y=1..4\\) が全て全称証明済みとなった。K0976予想の \\(y=4\\) 行を全称で確定した。
- K0977〜K0980の比較から、\\(y\\) 増分ごとの構造シフト（低域2拡張、特異伸長位置 \\(x=y+8\\)、tail境界 \\(x+y+8\\)）的一般的リズムが読み取れる。\\(y=5\\) はA/B/C子が揃っており、同一構造で開放される。
- \\(z\\ge8\\)、および全高さ \\(y\\) を統一する閉形式は残課題。

詳細: `research/experiments/vertical-fiber-two-token-z7-y4-boundary-20261118/report.md`
