# (4,22,5) class-split 掃引 — absence-capable 完全被覆 (2026-11-15 高速レーン・IN FLIGHT)

## 位置づけ

`M_{4,5} = 21 または ≥ 23` (K0857・4×21 witness-free 確定済み・上界
U_{4,5}=140 (K0318)・witness 帯 m=5..20 (K0833))。**前線は 4×22**。
本掃引は (4,22,5) を absence-capable に完全分解して決着を目指す。
完了して全 UNSAT なら witness-free 幅集合は {21,22}・鋭い形は
**M_{4,5} = 21 または ≥ 24**。SAT が出たら M ∈ [22,140] に戻り
witness を復号・検証する。

## 被覆の完全性 (4×21 lane と同一構造・幅だけ違い)

- 欠損クラス = 石数 ≤ q−2 = 3 の行の集合。safe な行は ≤ 4 石なので、
  欠損行の補集合は exactly 4 石 (sat3.js --class は D 外の行を rowGe 単位で
  FULL 固定するため、この制約を課しても被覆は完全)。
- 行ミラー V (行 0↔3, 1↔2) で類別すると正準クラスは 9 個。
- 単一クラス {0},{1} は正確な石数 k∈{0,1,2,3} と minpos p∈0..10 で分解
  (sound H-split: min(x1, 21−x_k) ≤ floor(21/2) = 10。H は行を保存する
  のでクラス内で健全)。minpos と lex の併用は unsound なため全インスタンス
  lex なし (four-row-q4-m35-class-split-20261115 規約)。
- multi クラスは直接。INDET が出たら krow ピン、それでも抵抗する
  {0}k3p0/p1 バケットは **第2石 x2 分割** (sweepp0x2.sh 方式・
  4×21 ではこれで 37バケット全 UNSAT・1枚 ≤185s に決着) で追分解する。
- 計: 陽性対照 1 + k3 22 + multi 7 + k2 22 + k1 22 + k0 2 = 76 インスタンス。
  cap 600s・resumable (records.jsonl key skip・CNF 生成は決定的・
  comma-anchored key 照合)。

## 陽性対照

(4,20,5) class {0} --krow=0:3 --minpos=1: m=20 witness (rows [4,4,4,3]) の
V 像を含み、4×21 lane では SAT 20.0s / 375,415 conflicts で V 像を再発見
(js+py 検証)。本 lane でも同一対照を最初に実行する
(cross-lane bit-exact 再現が較正になる)。

## 運用

- 2コア制約: ge20_cuts (n10 lane) と排他・kissat は常時1プロセスのみ。
- IN FLIGHT claim: output/inflight-claim-20261115.json。
- driver: sweep22.sh (sweep21.sh の m=21→22 版・minpos 0..10 不変)。
- records.jsonl は driver 実行中 append のみ (m21 lane の修復事故の教訓)。

## 結果

IN FLIGHT — 実行中 (2026-11-15 17:12Z 起動)。決着後に本 README を更新し
K 項目へ昇格する。

## 追記 (2026-11-15 17:25Z: 掃引開始直後の状況と道具の整備)

- **陽性対照 bit-exact 再現**: ctrl_4x20_c0k3p1 = SAT 39.3s / 375,415
  conflicts (4×21 lane の 20.0s / 375,415 と conflicts が完全一致 —
  同一 CNF・同一軌跡の cross-lane 較正として機能。秒数差は CPU 配分差)。
- **c0k3p0 = INDET** (cap 600s / 3,852,260 conflicts)。m21 では直接
  決着したバケット群だが m22 では x2 分割が必要になる可能性が高い
  (m21 の最難 x2 サブバケット 1,969,663 conflicts の約2倍を費やして
  未決着)。
- **CPU 割り当ての判明**: 本 sandbox の cgroup は `cpu.max 100000 100000`
  = **実効 1.0 CPU** (nproc=2 は表示上)。driver の cap 600s は壁時計
  なので、並走プロセス (n10 ge20_cuts) との共存中は実効 cap が目減り
  する。ge20 側を renice +5 して本掃引に ~75% を優先配分した。
  INDET 判定は cap 到達打ち切りであり bit-exact でない旨は m21 lane
  と同様に記録する。
- **sat4.js の --x2 上限を k-aware 化**: 従来の無条件 `B ≤ m−2` は
  k=2 バケットで正当な B=m−1 (=21) ケースを落としていた不完全な
  上限だった。`--krow=y:2` のとき `B ≤ m−1`、k≥3 のとき従来通り
  `m−2`。k≥3 に対する既存インスタンスは一切不変 (4×21 lane の
  37 サブバケットの md5 に影響なし)。k=2 分割の完全性に必要。
- **汎用分割 driver 追加**: `sweepp0x2gen.sh` (c{0,1}k{2,3}p{p} 任意
  バケット対応・CAP 環境変数・resumable・comma-anchored key 照合・
  SAT 時の js+py 二系統 witness 検証)。INDET バケットが出次第
  `bash sweepp0x2gen.sh <bucket>` で追分解する。


## 追記 (2026-11-15 17:55Z: k3 直接試行の連続 INDET と driver 並べ替え)

- **c0k3p0/p1/p2 が全て 600s INDET** (3,852,260 / 6,854,166 / 6,939,580 conflicts)。
  m21 では p2 以降は 76〜400s で直接決着していた一方、m22 は p2 も抵抗
  → **m22 の k3 バケットは広く 600s cap を超える** (m21 比 ~1.5〜2倍で
  一貫した難化。multi c01 は 451s/5,022,943 conflicts UNSAT・m21 310.8s/
  3,957,766 と同じ比率)。
- このまま残り19個の k3 直接試行に各 600s を焼くのは非効率なため、
  driver を **sweep22fast.sh** (multi → k2 → k1 → k0 を先に、k3 直接試行
  を最後) に並べ替えた。既知 INDET の c0k3p0/p1/p2 は sweepp0x2gen.sh
  (x2 分割・cap 900s) で追分解する。multi の INDET が出たら krow ピン
  (欠損行の正確な石数 0..3 で分割・sweep35 規約) で追分解する。
- cap 600s 到達の INDET の conflicts は壁時計打ち切り (同一 CNF の
  再実行は同一軌跡を辿るが、打ち切り点は bit-exact ではない)。

## 追記 (2026-11-20 高速レーン: takeover — 掃引再開・較正PASS・batchAB 実行中)

- 前オーナーセッションの最終pushは 2026-11-15 17:55Z（records 5行: 陽性対照 SAT・
  k3 直接INDET 3幅・c01 UNSAT で停止・以後5日間更新なし）。collision protocol に従い
  着手前に最新mainを再取得した上で本掃引をtakeoverした（他レーンの同一 (w,m,q)=(4,22,5)
  着手なしを確認済み）。
- **較正 (takeover環境)**: 陽性対照 ctrl_4x20_c0k3p1 のCNFが byte-exact 再現
  （md5 362034b210d89ed3a25d34072995f3a6・vars 9510/clauses 32976）し、
  kissat 4.0.4（公式静的バイナリ・md5 3a5eba830aa6008a604fcc9bbe99a325）が
  SAT / **375,415 conflicts bit-exact**（19.4s）。生成器・ソルバの決定性が本環境でも
  同一軌跡であることを確認。
- **sat4 k-aware x2上限の検証**: (4,21,5) c0k3p0 --x2=1 のCNFが旧sat4と k-aware版で
  byte-identical（md5 13749780ebd7467aca0a7b2e3ea7e163・k=3では m-2 上限のまま）。
  k=2 の --x2=21 (=m-1) は k-aware版でのみ生成可能（旧版はreject）を確認。
  x2符号器の後方互換性と k=2 完全性修正が実働することを検証。
- **実行方針 (takeoverセッション)**: 単一オーナー宣言
  （inflight-claim-20261120-takeover.json）。1インスタンスずつ逐次・CAP=900s（壁時計）。
  INDET は cap 到達の honest negative・不在主張ではない。既記録の c0k3p0/p1/p2 の
  600s INDET は直接再試行せず x2 分割へ直行（m21 で同バケットが 2400s でも未決着
  だった実績を尊重・無駄な cap 焼きを避ける）。batchAB（multi 6 + k2 22 + k1 22 +
  k0 2・sweep22fast と同じ「安価なクラスを先に」順序）から着手し、決着順にbatch push・
  records は append-only。

## 追記 (2026-11-20 batchAB 進行: 環境リセットと bit-exact 再現・multi 4/6 決着)

- 12:05Z に実行環境がハードリセットされ作業ディレクトリが消滅した（takeover較正・claim push は
  11:52Z に先に完了済みで無事。ローカルの c02/c03 第1回結果は records push 前に喪失）。
  セッション間で揮発しない永続域は repo のみのため、以降の運用は「決着レコードのこまめな増分push」に切替。
- **c02/c03 はリセット後の新環境で再実行して conflicts bit-exact を再現**
  （c02: 4,655,713・第1回 388.1s → 再実行 397.2s。c03: 3,768,211・283.2s → 292.2s。
  同一 CNF md5・kissat 決定性の環境またぎ検証として機能）。
- **multi クラス 4/6 決着・全 UNSAT**: c02 4,655,713/397.2s・c03 3,768,211/292.2s・
  c12 4,305,322/358.5s・c012 1,246,738/90.5s（cap 900s）。
  m21 比は c02 1.23x・c03 0.99x・c12 1.23x・c012 1.18x で予測難化と整合。
- c01（前レーン UNSAT 451.0s/5,022,943）と合わせ multi は残り c013・c0123 の2クラス。
  k2/k1/k0 46枚と k3 直接（c1k3p0..10・c0k3p3..10）19枚を同じ投入キューに入れて逐次実行中
  （CAP=900s・runner22.sh・resumable・records append-only）。

## 追記 (2026-11-20 batchAB 完了: multi 7/7・k2/k1/k0 46枚 全 UNSAT・records 58行)

- **multi 直接解が全正準クラス UNSAT で完結** (前レーン c01 と合わせ 7/7):
  c02 4,655,713/397.2s・c03 3,768,211/292.2s・c12 4,305,322/358.5s・
  c012 1,246,738/90.5s・c013 1,343,681/94.8s・c0123 580,425/39.5s
  (cap 900s・秒数は壁時計)。
- **k2 22枚・k1 22枚・k0 2枚も全 UNSAT**。k2 の最難は c0k2p1
  823,300/37.7s・k1/k0 は全て ≤2s 級 (石数制約の枝刈りが m22 でも決定的)。
- **c1k3p0 = UNSAT 5,324,074/442.6s** (direct・cap 900s 内で決着)。
  m21 の c1k3p0 (220.9s) 比は 2.0x で k3 難化予測 (×1.5〜2) と整合。
- records.jsonl は 58 行 (増分49行・2026-11-20 12:27:50Z〜12:42:41Z を
  12:50Z 頃 push)。既知 INDET c0k3p0/p1/p2 (600s・前レーン) は
  直接再試行せず x2 分割へ直行する方針は維持。
- **残り**: k3 直接 c1k3p1..10・c0k3p3..10 の 18 枚 (runner 実行中) と
  INDET 3 バケットの x2 分割 (sat4ka.js・各 ≤300s 予測)。
  全 UNSAT なら witness-free 幅集合 {21,22} = **M_{4,5} = 21 or ≥24**。
