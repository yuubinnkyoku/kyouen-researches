# 2026-11-22 最小極大近傍フルネット・セッションログ (sit-at込み完備走査・K1206監査・s_11/s_12/s_13近傍陰性)

高速レーン (短〜中時間の厳密成果)。branch/PRなし・main直接反映。

## 開始時の確認 (05:0xZ 開始時点)

- 開始時 HEAD: d73bb0b8 → 途中 4fcee8eb (05:02Z)。push前の最終再取得では
  8abb69c0 (06:14Z, n8カタログ照合・別レーン)。
- 並走レーンの占用: 6×32 t2 (b1afb181)・class5473 batch6・(4,4) m=35 class-split
  (4fcee8eb) → いずれも本レーンのpathと非接触。class10324/2634系・K1215/K1218/
  K1219系も非接触を確認 (コミットメッセージで状況把握)。
- 未着手領域の特定: s_11 (8≤s_11≤10, K0312) の 8/9石 witness 近傍探索と
  K1206 (12×12 wall strict局所最適) の監査は既刊成果と重複しないと判断。

## 発見: sit-at 候補除外の穴

hunt.mjs (K1206レーンの正本機材) の localNets・doubleSwapComplete の追加候補
列挙は、c !== p 条件で未被覆セルへの直接石追加 (sit-at) を除外していた。
State 自体は sit-at を正当に受理する (K0031 7×7 witness 除去→add の単体検査)。
よってこれらの「完全走査」は sit-at 分だけ不完備だった。sit-at を含む
全セル走査器 ext_nets.mjs (full0/full1/full2 = remove-m/add-a, 追加候補は
「現在石でない全セル」) を作成した。

## 第一期の走査 (リセット前、05:1x〜05:5xZ)

K1206 監査 (n=12 K0320 r2a1 7,425走査・n=13 r2a1 10,494・wall r2a1 6,120/
r2a2 413,100・13×13 plateau r2a1 8,800/r2a2 699,600) と n=11 近傍
(r1a0/r2a0/r2a1/r3a1/r3a2/r4a1/r4a2)、n=12 両11石witnessの r3a1/r3a2、
n=13 の r3a1/r3a2、SLS honest negatives、SAT INDETログ (n11k8/9/10 default
280s+較正) を実施し、すべての走査が 0 witness・bestScore は seed 未満の状態なし
を確認した。

## 第二期: 構成数の独立恒等式確認

ext_nets の列挙数は
totalChecked = C(k0,m) × (a=0 ? 1 : C(n²−(k0−m), a))
(k0=seed石数) を全件で満たすことを確認した。これにより「列挙が洩れていない」
ことの第二の検証になった。構成数は有限列挙の実行経費ではなく、完備性の
証明の一部として記録する (checked数そのものを成果としない)。
n=13 r2a2 (12石seed) の found=66 は全て trivial 自己再構成 (=seed) と
分類され、found 経路・isSeed 排除機構の陽性対照となった。

## 第三期: s_11 上界探索の完全近傍陰性 (n=11 K0320 10石witness)

7走査計 2,192,440 構成で 9石 witness (r2a1/r3a2) も 8石 witness
(r2a0/r3a1/r4a2) も seed 近傍に存在しない。r4a1 (7石) found=0 は
K0312 (k≤7 極大不可) と整合する期待値制御。**s_11∈{8,9,10} 不変**
(本走査で決着はつかない)。n=12: 両11石 witness 周囲 r3a2-full 1,514,700×2 =
0 → s_12≤10 witness はこれらの近傍になし。n=13: r2a2 829,026 (66 trivial)/
r3a1 35,200/r3a2 2,798,400 = 非自明0 → s_13≤11 witness は近傍になし。

## 独立検証 (6 seed)

verify_witness.py (整数行列式・公開検証器): K0320-n11/n12/n13・W_c は
SAFE+MAXIMAL (111/133/157/133 blocked、全空点証人つき)。wall12 は SAFE・
uncovered [(4,11),(5,11),(8,11),(11,11)] (K1206記録と完全一致)。
plateau13 は SAFE・uncovered 6点。ext_nets 再実行の決定性 byte一致
(ms・argv フィールド除く) も確認。

## 環境リセット事故と復旧 (正直記録)

〜06:00Z、SLS 再実行中に実行環境の infra failure が発生
(Arifact 保存エラー → /home/user/work 全滅)。第一期の全出力
(kissat ログ7本・SLS 出力・ext 出力 jsonl) を喪失した。knowledge mount の
kit は無傷。そこで:

1. 知見を踏まえ ext_nets.mjs を再作成 (最終版: bestScore 追跡・cp 再開・
   isSeed 分類つき)。
2. 全走査をやり直した (決定的。構成数は初回観測値・組合せ恒等式と全件一致。
   witness 数も全件 0 で一致)。
3. SLS・SAT も再実行した。CNF は enc_sat2.mjs (決定的) の再生成で
   7件全ての sha256 が初回記録接頭辞と一致 (n7k6 は 0aecb030… complete一致)。
   kissat の conflicts 数は機械速度・cap 依存のため初回の数値
   (280s: n11k8 577,502 など) は再現せず、**再実行側 (240s:
   n11k8 386,330・n11k9 184,869・n11k10 198,812) を正本として刊行した**。
   較正 n7k6 UNSAT の conflicts 174,155 は初回と完全一致。
4. 教訓 (前レーンと同一): **成果物は実行と同時に knowledge mount へ退避する**。
   今回の再実行では network mount への出力直書きをやめ、ローカル出力→
   完了毎に kit へ copy する手順に切替えた (ext 出力の network mount 直書きが 0.2s/write の
   I/O 待ちを作り、初回の r3a1 が約4分もかかる一因でもあった)。

## SAT・SLS honest negatives (単一オーナー規約の継承・値主張なし)

SAT: s12-s13 SATレーンの単一オーナー (71408dda54) の受入条件を継承し、
本レーンは値主張をしない。較正 (n7k6 UNSAT reproduction) のみ照合として
使用。n11k8/k9/k10 (v2.1) の default 240s 3ショットは INDET。n11k10 は
K0320 10石 witness で充足可能が既知のため「既知SATでも 240秒未達」という
最も強い honest negative。SLS v2 (60s・transplant seeding): k=10 seed7
bestScore 5 (既知 witness 再発見不能 = 陰性対照で探索力不足と分離不能)・
k=9 seed11 bestScore 7・k=8 seed23 bestScore 15。

## 10×10 五類の pairwise shape 距離

K1220 の5類 (K0038/K0034-another/draft/draft-sh7/v2.1) の2類間対称差を
bounding-box 原点揃え + D4 8像最小で計算: 全10組 ∈ {14,16}、最小14。
v2.1 witness は再生成 CNF (95a5c4c9…) の SAT モデルから決定的復号し
K1220 公刊座標と一致 (kissat 4.0.4 決定性の追加対照)。

## 出版 (06:4xZ)

- research/experiments/minimal-maximal-neighborhood-full-nets-20261122/
  (README・scripts・seeds・records 58ファイル・MANIFEST)
- session log (本ファイル) と K1222 (method: sit-at穴+ext_nets+監査)・
  K1223 (computation: 近傍陰性+honest negatives) を作成。
- push 直前に最新 main を再取得した (8abb69c0)。
- 残債務: r4a3 (remove-4/add-3, 約34分 chunked)・n12/13のより深い近傍・
  s_11 8/9石の全域探索は heavy lane。n8 witness×K0032 408カタログ照合は
  06:14Z 別レーンが完了済み (本レーンでは不実施)。

## 解釈規約 (standard な定型)

陰性はすべて有界近傍の探索不成功であり非存在証明ではない。
bestScore・checked数・conflicts数は勝敗ではない。標準 11×11 空盤・二石root・
S2・class 1/2/4 は本レーン非接触で UNKNOWN のまま。s_11・s_12・s_13 の
値は本レーンで一切更新していない。
