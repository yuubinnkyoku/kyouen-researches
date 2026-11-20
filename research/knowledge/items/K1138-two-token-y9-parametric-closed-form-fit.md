---
id: K1138
title: 2トークン残余ゲーム y=9族の閉形式候補cand9の有限fittingとbox外spot検証（全称証明は次段階）
kind: proposition
status: observed
topics: [grundy, residual-games]
aliases: [two-token y=9 parametric closed-form candidate fitting, cand9 fit]
relations:
- type: depends_on
  target: K0832
  note: 残余ゲームHの定義・単一トークン閉形式のraw anchorに使用する
- type: depends_on
  target: K1135
  note: テンプレート系列y=1..8の直前の全称証明。y=9族の次段階の全称監査ではB子（y=8子）の評価にcand8を使用する
artifacts:
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/report.md
  role: data
  note: cand9のz偶奇別T/P集合表全文（pin統一式・偶z対角行の値1全欠如・偶z pin行d範囲の+2シフト〔y=8の[-y+2,y-2]→y=9の[-y+4,y+2]〕・奇z d=y行の値1追加点z+19=2y+z+1を含む）と検証規模の記録
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/cand9.py
  role: verifier
  note: 閉形式候補cand9（in_T9値2表・in_P9値1表）とprobe_rows.txt全点照合（73,811点・mismatch 0・T/P重複 0）
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/probe_y9.py
  role: data
  note: 生二重再帰probeエンジン（順序保持・降順正準形メモ化・z=0..30・x=9..z+27・R<=x+z+26・1,054行RLE生成）
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/spot9.py
  role: verifier
  note: box外spot照合25,376点（深R<=130・z=31..40・x=y=9エッジz=9..40・d<=52・bad 0）
- path: research/experiments/vertical-fiber-two-token-y9-parametric-allz-fit-20261120/output/audit.json
  role: data
  note: fitting段階の実行監査（統計・SHA-256・再生コマンド・probe_rows.txtは公開せず決定論的再生可能の注記）
- path: research/log/2026-11-20-two-token-y9-parametric-fit.md
  role: log
  note: 宣言の確認・導出経緯・出版記録（K1137競合検出とK1138への再採番を含む）・次に開くもの（12チェック監査）
- path: research/log/2026-11-20-two-token-y9-parametric-allz-single-owner-note.md
  role: log
  note: 単一オーナー宣言ノート（宣言2026-11-20T08:41:00Z・先行出版済み）
scope: >-
  κ=1残余ゲームH(R;X;z)の2トークン族X=(x,9)。宣言noteの手続き第1段階として、
  z偶奇別パラメトリックT/P集合表候補cand9を生probeから導出し、有限範囲
  （probe box 73,811点＋box外spot 25,376点＝合計99,187点）で生エンジンとの
  完全一致を確認した。全z>=0・全x>=9・全R>=0の全称証明は本項に含まない
  （次段階の選択肢分解・mex恒等式・型機械・12チェック監査による。
  x=9合流子は(9,8)≡(8,9))。
evidence: >-
  生二重再帰（順序保持・降順正準形）によるprobe z=0..30・x=9..z+27・R<=x+z+26
  （1,054行・73,811点）でcand9と全点一致（mismatch 0・T/P重複0）。うち
  マージ行x<=z-10は78行・5,070点全点が単一トークン閉形式single_token(x+9,z,R)
  に一致（値0/1/2すべて）、tail領域R>=x+z+10は17,918点でx+z+y+1開始式・
  (x+9) mod 2 tail値とも一致。box外spot 25,376点（深R<=130の7行・z=31..40
  代表14d・x=y=9エッジz=9..40・d∈{30,41,52}×6 z値）も全一致。cand9の
  構造はy=5..8と同じ族式（tail x+z+y+1・マージx<=z-y-1・基底点y点
  {z+1,..,z+2y-1}=9点・定常pin 2y+z/2y+z+1・対角行上端格子規則
  r=z+y-[2(z-y)≡0 mod 4]）のy=9値で、pin統一式（奇z pin=z+2y+(d-y)/2
  〔d≡y mod4, d∈[-y+2,y]〕・偶z pin=z+(d+3y)/2〔d≡y+2 mod4, d∈[-y+4,y+2]〕）
  がy=8と同じ式形で成立する。ただし偶z pin行のd範囲がy=8の[-y+2,y-2]から
  y=9の[-y+4,y+2]へ+2シフトしてpin行5行に増える点・偶z対角行（d=-9）が
  値1を一切持たない点（y=8のd=-8 P=Falseと同型）・奇z d=y行の値1追加点
  z+19=2y+z+1（y=8のd=8行z+17と同型）がy=9で新たに実測された有限事実。
  本項は有限fittingとspot検査であり全称主張ではない（trust境界は
  K0003のobserved段階）。
---

## 命題候補（observed・全称は未証明）

すべての z>=0・x>=9・R>=0 に対して H(R;(x,9);z)=cand9(z,x,R) が成り立つと予想する。
cand9 は report.md 全文掲載の z 偶奇別 T/P 集合表（`cand9.py` が正本）であり、
合計 99,187 点（probe box 73,811 点＋box 外 spot 25,376 点）で生エンジンと
完全一致を確認した。マージ行・tail 領域の回帰（各 5,070・17,918 点）も不一致 0。

## y=1..8 全称表からの横断予想の y=9 での判定（有限範囲）

- tail 開始式 x+z+y+1（y=2..8 全称確定）: y=9 で一致（9 族連続を支持）
- マージ命題 x<=z-(y+1)（y=1..8 全称確定）: y=9 の x<=z-10 で回帰（5,070 点）
- 基底点 y 点仮説 {z+1,..,z+2y-1}（y=1..8 全称確定）: y=9 の 9 点で一致
- 対角行上端格子規則・定常 pin 2y+z/2y+z+1・掃引帯 O[2y+z, x+z+y]: y=9 値で一致
- pin 格子（y=5..8 統一）: y=9 で pin 統一式は成立するが、偶 z pin 行の d 範囲が
  y=8 から +2 シフト（[-y+2,y-2]→[-y+4,y+2]・4行→5行）。y=7 の偶 z は
  [-y+4,y-2]・3行であったので、偶 z pin 行の右端は y ごとに異なる
  （y=7:y-2・y=8:y-2・y=9:y+2）。
- 型機械の clip 窓 2y+2=20（±20/番兵±21）tight の検証: 次段階（未実施）

## 限界

本項の根拠は有限 probe・spot 照合のみで、選択肢分解の健全性・mex 恒等式の
機械照合・型 confluence・独立 census は次段階（y=1..8 出版系列と同一手続き）。
有限事実の全称への昇格を含意しない。3トークン以上・y>=10 族・固定幅・
q点版安定化長・標準 11×11 の空盤勝敗は範囲外。

## 採番記録

作業中仮番号 K1137 で出版を試みたが、push 直前の README 実ファイル再取得で
並走の n11 residual29 レーンが items/K1137-n11-residual29-win8-cert-extract-root00000000000200003800200008180000.md
を先行出版済みであることを検出し、AGENTS.md 再採番規約により次の空き番号
K1138 へ再採番した（K1135〔仮番号K1133〕と同じ手続き・first-published-priority）。
