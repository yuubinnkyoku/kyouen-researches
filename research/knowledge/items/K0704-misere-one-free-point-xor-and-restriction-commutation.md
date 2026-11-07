---
id: K0704
title: 任意有限不偏ゲームの終局1補助mexは一自由点でxor1となり、低h制限ゲームとも直和が可換
kind: proposition
status: proved
topics: [grundy, residual-games, variants]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 通常ゲームのmexと独立な一回手との直和
artifacts:
- path: research/experiments/misere-one-free-point-xor-20261108/proof.md
  role: proof
  note: mex恒等式と高さ帰納、低h制限との可換性、以前の否定文の訂正
- path: research/experiments/misere-one-free-point-xor-20261108/verify.py
  role: verifier
  note: 全birthday四以下の子集合形式と自由点追加再帰、既存純三点全自由点対を照合
- path: research/experiments/misere-one-free-point-xor-20261108/output/audit.json
  role: certificate
  note: 全65536ゲーム形式と純三点58146核の自由点対の独立検査
- path: research/log/2026-11-08-one-free-point-xor-correction.md
  role: log
  note: hの非加法性と一自由点xorを混同していた否定文の訂正記録
scope: 有限非巡回不偏ゲーム。hは終局1、非終局mex。Fは独立な一回だけの手。低h制限通常ゲームDとそのSG tはh根が0/1の場合。任意直和におけるh同士のxor加法性は含まない。
evidence: r=mex Aならmex({r}∪(A xor1))=r xor1という恒等式を用い、終局基底とゲームの高さで帰納。低h所属が自由点付加で保存されることからDの直積同型を導く。全小型ゲーム形式と既存純三点全核でも確認。
---

任意の有限不偏ゲームGについて、終局で1・非終局で子補助値のmexとするhは、
独立した一回手Fを加えると

\[
\boxed{h(G+F)=h(G)\mathbin{\mathrm{xor}}1.}
\]

従ってf個の自由点はhにf mod2をxorする。
これは任意直和でのh同士のxor則とは異なる。
実際h(F)=0なのにh(F+F)=1であるため、h(G+H)=h(G) xor h(H)は一般には成立しない。

証明は、r=mex Aに対するmex({r}∪(A xor1))=r xor1と、ゲームの高さの帰納で閉じる。
終局Gのh=1、一自由点付きh=0を基底とし、非終局の自由点手と元のゲーム手を分ける。
禁止辺rankや点数、hの大小、特定の構成族の仮定は不要。

さらに、h≤1の局面だけを残す通常ゲームD(G)について、h(G)≤1なら
D(G+F)はD(G)+Fと同型で、通常値tにも **t(G+F)=t(G) xor1** が成り立つ。
全残余Hでh(H)≤1とh(H+F)≤1が同値なので、制限と直和が可換になる。
K0696で性質Rと呼んだ低/高h所属保存は、全有限ゲームで成立する一般補題である。

K0694の元のproof資料の「h_1=h_0 xor1とは限らない」は誤り。
同資料の二個周期証明・pivot変換・数値結果はこの否定文に依存せず有効であり、
当時の一次資料を保持して[本証明の訂正節](../../experiments/misere-one-free-point-xor-20261108/proof.md)を正本として参照する。
全birthday≤4の65,536ゲーム形式と、既存純三点58,146核の自由点対も全件一致した。
