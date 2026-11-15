# 2026-11-15 高速レーン: (4,5) m=21 surgery 完全列挙負 (sd≤6) ・class-split 掃引 IN FLIGHT・掃引 driver v2 bugfix

## 経緯と判断

- 起点で最新 main を確認: (4,5) m=21 は witness 帯 m=5..20 の直後の前線で
  未決着（def-mode OR 210s INDET 3,296,257・2クラス被覆 600s INDET
  合計 ~14.2M conflicts・rowY=0..3 full-lex INDET）。
  class2-lane・素数 census・five-row-q6-m23-longcap・vertical-fiber・8x29 は
  他レーン領域のため回避。11×11 等は UNKNOWN。
- (a) m=20 witness 近傍の完全列挙（surgery）と (b) absence-capable 完全分解
  掃引（class-split）を並行して準備した。surgery4.js は (4,5) への適用が
  census 検査 8/8 PASS のうち (4,10,5)/(4,20,5) で正当化済み
  （four-row-q4-m35-surgery-20261115 の census q≤w 修正）。
- surgery 実行: m=20 witness（rows [4,4,4,3]・15石・3系統検証済み）を
  4×21 に offX=0/1 で移植（未遮断は T′={(20,3)}/{(0,3)} の1点のみ）し、
  追加<=2・除去<=2・石数<=15 を完全列挙: 12,754/12,816 最終状態葉・
  すべて safe・0 witness（~370ms・決定的）。census 542 曲線は
  sat2.js (4,21,5) def-mode の記録曲線数と一致。
- さらに (3,3) 拡張（sd≤6）も完全列挙: 1,250,587/1,256,103 葉・
  0 maximal・0 witness（~8秒/埋め込み）。fail 内訳は unblocked_hole が主因
  で (2,2) と同構造。**m=20 witness 両埋め込みから sd≤6 以内の
  ≤15石 m=21 witness は存在しない（局所負・不在主張ではない）**。
  連続幅間の witness jump が大きい先行観察と整合。
- class-split 掃引: 4×21 の absence-capable 完全被覆を構成。
  9 正準欠損クラス mod V・単一クラス {0},{1} は正確な石数 k∈{0..3} と
  minpos p∈0..10（sound H-split: min(x₁,20−x_k)<=floor(20/2)=10・H は行を
  保存）で分解・multi クラス 7 個は直接、計 76 インスタンス
  （cap 600s・resumable・全インスタンス lex なし）。
  陽性対照 (4,20,5) class{0} k3 p1 は **SAT 20.0s/375,415 conflicts**。
  復号 witness（rows [3,4,4,4]）は m=20 witness の V 像そのもので、
  sat3.js decode verifyConfig + verify_witness.py（Python Fraction）の
  2系統検証 ok — decode 鎖とクラス論法が実地検証済み（pipeline 較正完了）。
- **掃引 driver v2 bugfix**: resume 時の skip 経路
  `done_key && grep -q SAT records` が records 全体から SAT を探すため、
  対照 SAT record の存在だけで最初の skip で SATFOUND=1 が立ち掃引が
  即誤終了する bug があった（q5 掃引の再開時に SWEEP_BATCH_DONE
  satfound=1 を実際に観測して発見）。同一 key の record に限定する判定
  （per-key）に修正し sweep21.sh/sweep35.sh 両方に適用・main 反映済み。
  q4 掃引は対照が INDET だったため同 bug は一度も顕在化していない。
  対照直後の SATFOUND=0 リセットだけでは不十分だった（v1 修正は不完全）。
  併せて conflicts 抽出 grep の CR 混入行 binary 判定（conflicts null 化）を
  grep -a で修正。両実験 README の erratum に正直に記録した。

## 成果

1. (4,5) m=21 bounded-edit surgery 完全列挙負 (2,2)+(3,3) sd≤6
   （four-row-q5-m21-surgery-20261115・main 反映済み）
2. (4,5) m=21 class-split 掃引の設計・対照較正・driver v2
   （four-row-q5-m21-class-split-20261115・IN FLIGHT・records 増分 push 中）
3. 掃引 driver v2 bugfix（skip 経路 per-key SAT 判定・grep -a）の両 driver
   適用と erratum 記録
4. K0833 追記（q5 m=21 系・artifacts 3件）・CSV (4,5) 行強化・
   workflow トリガー行

## 解釈境界

- surgery 負は m=20 seed 近傍のみの局所結果。4×21 全体の不在主張ではない。
- class-split 掃引は IN FLIGHT。76 インスタンスの判定が出揃うまで
  M_{4,5} は [21, 140] のまま。全 UNSAT なら M_{4,5}=21 or >=23・
  SAT なら M ∈ [22, 140]（K0821-audit 規約）。
- cap 600s INDET の conflicts は同一軌跡の壁時計打ち切りであり bit-exact
  ではない（README に明記済み）。
- 初記録 c0k3p0/c0k3p1 はともに cap 600s INDET（7,814,011/7,324,409
  conflicts）— 2クラス lex 掃引（~7M/クラス）と同水準の均質な前線抵抗。
  minpos ピンは (5,7) 帯のようには難度を下げない観察（未確定・掃引の
  進行で更新）。
- 11×11 等は UNKNOWN（別レーンの領域）。

## レジューム

- 掃引は resumable driver が継続実行中（対照→c0k3p0→c0k3p1→c0k3p2…の順・
  起動前にプロセス走査で二重起動防止）。records.jsonl は数件貯まったら
  実験 dir の output/records.jsonl へ増分 push。
- 環境リセットをまたぐ再開: main の scripts + sweep21.sh + records.jsonl を
  作業 dir に展開し kissat 4.0.4 を公式 rel-4.0.4 asset から再取得して
  nohup で launch。driver v2 は per-key skip 判定つき。
- 掃引完了時: 全 UNSAT なら M_{4,5}=21 or >=23 の確定記録（K0833・CSV・
  K 項目）・最難クラスへの lex=H 交叉確認。SAT なら witness の 2系統検証
  （driver が decode+verify_witness.py を自動実行）と M ∈ [22, 140] の更新。
- q4 掃引（four-row-q4-m35-class-split-20261115・一時停止中）は q5 掃引が
  一巡したら再 launch。二重起動防止と driver v2 適用済みの確認をすること。


## 追記: blocker円分割の独立監査 (2026-11-15)

- 4×21・q=5 の c0k3p0/p1 で、右端 (20,0) を空にする枝の blocker を円だけに絞れる理由を明記した。非水平直線は4行それぞれと高々1点で交わるため全点数≤4、水平行0は3石しかなく q−1=4 に届かない。
- 独立Python整数実装で全円census・固定石を含むピン集合・旧plain列挙を監査。538円、右端を通る19円 (17×6点・2×5点)、p1 adapted 81/p0 adapted 86、A枝込み82/87件。各円の三つ組数は C(k,3) と一致し、ケースピン集合の重複なし。
- 旧SA p1=83件のうち2件は、既に固定された (1,0) を含めず4点をピンしたため、固定石を加えると円上5石となる実行不能枝。fail:2と一致。厳密掃引にはadapted 81件を使う。
- 監査報告・検証器・JSONを four-row-q5-m21-class-split-20261115 に追加。2回の実行でJSONのSHA-256一致。
- **信頼境界**: これは円/直線censusと完全被覆の監査であり、Kissat判定ではない。solver全件未取得、M_{4,5}∈[21,140] は不変。
