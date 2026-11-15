# 2026-11-15 高速レーン: (4,4) m=35 surgery 完全列挙負・class-split 掃引 IN FLIGHT・(6,4) m=47 RAM 壁

## 経緯と判断

- 起点で最新 main を確認: (4,4) m=35 と (6,4) m=47 はいずれも未着手の前線
  （frontier レーンは m=35 2クラス被覆 600s INDET・m=46 free-append で停止）。
  class2-lane（cost-77b）・素数 census・five-row-q6-m23-longcap・vertical-fiber・
  8x29 は他レーンの IN FLIGHT 領域なので回避した。
- (6,4) m=47 rowY=0 を最初に試行: sat3 streaming 7r 版の CNF 生成は成功したが
  （2,701,853 vars / 8,965,702 clauses / 259,412 curves・
  md5 e2c7ab7255893ea4e974a479bd04c8f3）、kissat 4.0.4 が SIGKILL/OOM
  （rc=137・14.3s・sandbox RAM ~2.1GB）。m=45 まで動作していた rowY 分割の
  RAM 境界は m=47 と確定。方法論的負として記録
  （six-row-q4-m47-rowY0-oom-20261115）。M_{6,4} ∈ [47, 1113] は不変。
- (4,4) m=35 に転換し、(a) m=34 seed 近傍の完全列挙（surgery）と
  (b) absence-capable な完全分解掃引（class-split）を並行して準備した。
- surgery 準備中に surgery.js の chord-pair census が q>w でしか完全でない
  ことが判明（q<=w では非行の直線と (1点,1点,1点)/(2点,1点) 行分布の円が
  抜ける。m=35, q=4 は q=w でちょうど該当）。surgery4.js は列挙コアを
  verbatim のまま census だけ buildCensus4 に差し替え、buildCensus4 が
  sat.js 全三つ組 buildCensus と点集合族として完全一致することを 8/8 対照で
  検査（(4,8,4) 485 / (4,20,4) 7,689 / (4,35,4) 41,607 / (5,12,4) 2,875 /
  (6,10,4) 2,735 / (3,24,4) 6,413 / (4,10,5) 89 / (4,20,5) 491）。
  併せて列挙コアの空白正規化一致も機械検証した。
- surgery 実行: m=34 witness（rows [3,3,2,3]・11石）を 4×35 に offX=0/1 で
  移植し、追加<=2・除去<=2・石数<=11 の全編集を完全列挙。
  offX=0 は 20,277・offX=1 は 21,824 最終状態葉で、すべて safe・
  **0 witness**。m=34 witness の両埋め込みから 2+2 石編集以内に
  4×35 witness は存在しない（局所負・不在主張ではない）。
  連続幅間の witness jump が大きいという先行観察
  （(5,6) sd>=7・(7,5) 2石移動）と整合。
- class-split 掃引: 4×35 の absence-capable 完全被覆を構成。
  9 正準欠損クラス mod V（{0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},
  {0,1,2,3}）・単一クラス {0},{1} は正確な石数 k∈{0,1,2} と
  minpos p∈0..17（sound H-split: min(x₁,34−x_k)<=17）で分解・
  multi クラスは直接、計 82 インスタンス（cap 700s・resumable・
  全インスタンス lex なし — minpos と lex=H の併用は unsound なため）。
  陽性対照 (4,34,4) class{1} k2 p7 は m=34 witness の V∘H 像を含む。
  全 UNSAT なら M_{4,4}=35 or >=37（K0821-audit 規約）・
  SAT なら M ∈ [36, 237]。
- 運用事故の記録: 掃引 driver を 2 重起動してしまい（既存プロセスの生存確認
  前に再 launch）、対照インスタンスの kissat ログに重複分の行が一時混入
  （08:36:15-28Z）。重複側を kill して単一化した。records への影響はないが
  ここに明記する。
- さらにその後、実行環境リセットで掃引プロセスとローカル records.jsonl が
  消失（対照の着地前。main への反映は実験 dir と README のみで
  records.jsonl は未push だったため、失ったのは対照の未記録経過のみ）。
  掃引は main の scripts から再起動する（下記レジューム）。

## 成果

1. (4,4) m=35 bounded-edit surgery 完全列挙負・census 修正 + 8/8 検査
   （four-row-q4-m35-surgery-20261115・commit 7458be68）
2. (4,4) m=35 class-split 掃引の設計と 82 インスタンス driver
   （four-row-q4-m35-class-split-20261115・commit 55bc34d4・IN FLIGHT）
3. (6,4) m=47 rowY=0 kissat RAM 壁の記録
   （six-row-q4-m47-rowY0-oom-20261115・commit 2cac39cc）
4. K0833 追記・CSV (4,4)/(6,4) 行更新・workflow トリガー行（本 commit）

## 解釈境界

- surgery 負は m=34 seed 近傍のみの局所結果。4×35 全体の不在主張ではない。
- class-split 掃引は IN FLIGHT。82 インスタンスの判定が出揃うまで
  M_{4,4} は更新しない。対照が cap 700s で INDET の場合は
  pipeline 較正としては成立（README に明記済み）。
- m=47 OOM は判定ではなく環境上限。M_{6,4} ∈ [47, 1113] は不変。
- 11×11 等は UNKNOWN（別レーンの領域）。

## レジューム

- 掃引の再起動: main の four-row-q4-m35-class-split-20261115/scripts +
  sweep35.sh を作業 dir に展開し、kissat 4.0.4 を公式 rel-4.0.4 asset から
  再取得して nohup で launch。起動前にプロセス走査で二重起動を防止すること
  （前回の事故参照）。records.jsonl の key で済みスキップするため、
  環境リセットをまたいで再開できる。
- 対照 (4,34,4) class{1}k2p7 は cap 700s。INDET の場合は
  (4,20,4) class{0}/{1} の速い対照を追加して decode 鎖を検証する。
- 掃引完了時: 最難 multi クラスへの lex=H 交叉確認・CSV/K 項目の完成版更新・
  M_{4,4}=35 or >=37 の確定記録。
- (4,5) m=21 surgery は census 検査済み（(4,10,5)/(4,20,5) PASS）で
  実施可能。frontier レーンの (4,5) m=21 INDET との重複に注意。

## (4,5) m=21 class-split 掃引 — 残り2バケットの deep cap 2400s 判定（2026-11-15・高速レーン）

- deepcap.sh v2（p1 の minpos パース bug 修正・cap-aware resume つき）で
  残り INDET バケット class {0} k3 p0/p1 を cap 2400s で再判定。
- **c0k3p0: INDET・13,113,901 conflicts。c0k3p1: INDET・12,619,361 conflicts**
  （正規 CNF md5 059fc19d・v1 ではパース bug で p0 と同一 CNF だった）。
- 掃引全体: 対照 SAT（較正済み）+ 73 UNSAT + 2 INDET で完了。
  4×21 の不在・存在ともに未確定（両バケット open・7200s 級の長時間 cap か
  SA pin 系絞り込みが次手段）。M_{4,5} ∈ [21, 140] 不変。11×11 等は UNKNOWN。
- 運用: 環境リセットで deepcap 進行中のソルバが1回全滅したが、deepcap.sh は
  cap-aware resume で決定的再実行可能（CNF 再生成も決定的）なため
  同一キャップで再実行して判定を取得した。
