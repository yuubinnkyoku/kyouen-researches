# (4,5) 4×21 class-split 掃引 — absence-capable 完全被覆 (2026-11-15 高速レーン・IN FLIGHT)

## 位置づけ

`M_{4,5} ∈ [21, 140]` (witness 帯 m=5..20、上界 K0318 U_{4,5}=140、K0833)。
前線 m=21 は def-mode OR 210s INDET (3,296,257 conflicts)・2クラス被覆
(lex=H rowY=0/1) 600s INDET (合計 ~14.2M conflicts) で未決着
(four-row-q4-q5-frontier-20261115)。近傍の完全列挙負は
[four-row-q5-m21-surgery-20261115](../four-row-q5-m21-surgery-20261115/)。
本掃引は (4,21,5) を absence-capable に完全分解して決着を目指す。

## 被覆の完全性

- 欠損クラス = 石数 ≤ q−2 = 3 の行の集合。safe な行は ≤ q−1 = 4 石なので、
  欠損行の補集合は exactly 4 石 (sat3.js --class は D 外の行を rowGe 単位で
  FULL 固定するため、この制約を課しても被覆は完全)。
- 行ミラー V (行 0↔3, 1↔2) で類別すると正準クラスは 9 個:
  {0},{1},{0,1},{0,2},{0,3},{1,2},{0,1,2},{0,1,3},{0,1,2,3}。
- 単一クラス {0},{1} は正確な石数 k∈{0,1,2,3} と minpos p∈0..10 で分解
  (sound H-split: min(x₁, 20−x_k) ≤ floor(20/2) = 10。H は行を保存するので
  クラス内で健全)。minpos と lex の併用は unsound なため全インスタンス
  lex なし (four-row-q4-m35-class-split-20261115 と同じ規約)。
- multi クラスは直接 (各欠損行 ≤3 石)。INDET が出たら krow ピンで追分解する。
- 計: 陽性対照 1 + k3 22 + multi 7 + k2 22 + k1 22 + k0 2 = 76 インスタンス。
  cap 600s・resumable (records.jsonl の key で済みスキップ・CNF 生成は決定的)。

## 較正 (陽性対照)

(4,20,5) class {0} --krow=0:3 --minpos=1 は m=20 witness (rows [4,4,4,3]) の
V 像を含み、**SAT 20.0s / 375,415 conflicts**。復号 witness (rows [3,4,4,4]・
15石、row 0 = (1,0),(4,0),(19,0)) は m=20 witness の V 像そのもので、
sat3.js decode の verifyConfig (census 不使用) ok +
verify_witness.py (Python Fraction) ok — decode 鎖とクラス論法の両方が実地検証された。

## 結果

IN FLIGHT (records.jsonl に増分追記)。

- **全 UNSAT ⟹ 4×21 欠損極大不在が確定し M_{4,5} = 21 or ≥ 23** (K0821-audit 規約)。
- **SAT ⟹ witness 帯は m=5..21 に拡大し M_{4,5} ∈ [22, 140]**。

## files / resume

- `sweep21.sh` — driver (対照後に SATFOUND=0 をリセットする bugfix つき。
  同種の bug (対照 SAT で掃引全体が誤終了) は four-row-q4-m35-class-split-20261115
  の sweep35.sh にもあったが、対照が INDET だったため顕在化せず、当該ファイルは
  同日修正済み)。
- `scripts/` — sat3.js (class-split 符号化) / sat2.js (K0810 core) /
  sat.js (検証器) / verify_witness.py (Fraction 検証)。
  md5 は four-row-q4-m35-class-split-20261115/scripts と同一 blob。
- `output/records.jsonl` — 1インスタンス1行・増分 push。
- resume: scripts + sweep21.sh + output/records.jsonl を作業 dir に展開し
  `nohup setsid bash sweep21.sh > output/sweep21.log 2>&1 < /dev/null &`
  (起動前にプロセス走査で二重起動防止のこと)。


## 追記: driver v2 (skip 経路の per-key SAT 判定)

初版 `sweep21.sh` の skip 経路 `done_key && { grep -q "\"result\":\"SAT\"" records … }`
は records 全体から SAT を探すため、**対照 (SAT) の record が存在する限り
最初の skip で SATFOUND=1 になり掃引が即終了する** bug があった
(初回起動時は全インスタンス未記録で skip が起きなかったため、
対照の decode までは正常に進んだ)。
v2 では skip 時の SAT 判定を **同一 key の record に限定**した
(`grep "\"key\":\"$key\"" | grep -q SAT`)。
対照直後の SATFOUND=0 リセットに加えて、resume 時の対照 skip でも
掃引が続行するようになった。
同 bug は four-row-q4-m35-class-split-20261115 の sweep35.sh にもあり、
同日 v2 修正済み (そちらは対照が INDET だったため未顕在化だった)。

## 追記: 環境リセット越しの決定性 (2026-11-15)

09:25Z に実行環境がリセットされ、ローカル作業 dir (kissat 含む) が消失した。
main の scripts/sweep21.sh (driver v2)/records.jsonl (3行: 対照 SAT +
c0k3p0/c0k3p1 INDET) から復元し、kissat 4.0.4 を公式 rel-4.0.4 asset から
再取得 (md5 3a5eba830aa6008a604fcc9bbe99a325) して掃引を再開した。
driver v2 の per-key skip が実働し、対照の SAT record を存在下で素通りして
c0k3p2 から再開した (v1 の bug ならここで誤終了していた箇所)。

**c0k3p2 (リセット前 09:20:59Z UNSAT/5,208,764 conflicts/401.5s) の再実行は
09:35:02Z に UNSAT/conflicts 5,208,764 bit-exact で再現** (壁時計のみ
391.0s)。CNF md5 (ce3bed0134103fa362aaef24edf18fbb) も同一。
K0835 lane と同じく「同一コード・同一分割が環境をまたいで一致再現する」
決定性傍証として記録する。

## 追記: class {0} k3 完了 (9/11 UNSAT) と minpos 難度曲線・クラス間非対称

- **class {0} k3 (c0k3p0..p10) 完了**: p2..p10 の 9 バケットはすべて UNSAT
  (conflicts 5,208,764 → 1,600,698 と minpos に対して単調減少・
  391s → 76s)。残る p0/p1 のみ cap 600s INDET
  (7,814,011 / 7,324,409)。
- **難度曲線は witness 幾何と相関**: m=20 witness の V 像 (row 0 =
  (1,0),(4,0),(19,0)) は minpos バケット p1 に属し、m=21 で最難の
  バケットはちょうど p0/p1 (左端寄り欠損行)。前線の抵抗は witness 帯の
  終端幾何の近傍に集中している観察 (未確定・深いキャップでの決着待ち)。
- **class {1} k3 は class {0} より大幅に易しい**: c1k3p0 UNSAT
  4,396,040/314.1s・c1k3p1 UNSAT 2,717,030/165.1s (同バケットの
  class {0} は 600s cap INDET)。m=20 witness の欠損行は row 3 (≡{0}) で、
  witness 近傍クラスが最難という非対称と整合。


## 追記: deep-cap 決着試験 (IN FLIGHT)

残る2バケット c0k3p0/c0k3p1 を cap 600s→2400s で決着する
`deepcap.sh` を追加した (12:41Z 起動・resumable: records に
SAT/UNSAT 済みの key は skip、INDET 行は再実行される)。
- 両方 UNSAT ⟹ 4×21 欠損極大不在が確定し M_{4,5} = 21 or ≥ 23 (K0821-audit 規約)。
- SAT ⟹ witness 帯は m=5..21 に拡大し M_{4,5} ∈ [22, 140]。
深キャップでも INDET の場合は minpos サブ分割 (row 0 の第2石位置) か
--lex=H 交叉検証に分解する。


## 追記: deep-cap その1 — c0k3p0 は cap 2400s でも INDET・driver v1 の minpos 解析 bug

- **c0k3p0 deep (cap 2400s): INDET / 13,113,901 conflicts** (cap 600s の
  7,814,011 から延伸)。CNF md5 9a6e40b4… は cap-600 行と同一 (インスタンス同一の再実行)。
- **driver v1 bug**: `${key:6}` は "c0k3p0" に対し空文字列になり、
  `--minpos=` (空) を渡していた。sat3.js は `Number("")=0` として minpos=0 に pin するため、
  結果的に (a) p0 の脚は偶然にも真の c0k3p0 インスタンスと完全一致 (md5 で確認済み・記録は正当)、
  (b) p1 の脚は c0k3p1 ではなく **c0k3p0 の重複** になっていた。
  重複を検出して p1 の kissat を ~3 分で kill (junk record の追記は deepcap.sh を先に kill して防止・
  records は 77 行のまま)。
- **driver v2**: `${key:5}` に修正し、resume guard を cap-aware にした
  (SAT/UNSAT 済み OR 同 cap の行あり → skip)。再起動で p0 は skip、
  **p1 は正しく minpos=1 で起動** (CNF md5 059fc19d… は cap-600 行と同一)。
- c0k3p0 の次の分解案: row 0 の第2石位置 b∈{1..19} による完全ケース分割
  (各バケットに unit pin を追加した符号化)。p1 が決着しても p0 は残るため、
  並行して準備する。


## 追記: 第2石位置 x2 サブ分割の道具 (sat4.js) — c0k3p0 INDET 受けの次段階

c0k3p0 が cap 2400s でも INDET になったため、bucket 内の完全ケース分割として
row 0 の第2石位置 b を pin する `sat4.js` を追加した
(`--minpos=p --x2=B`: cells (0, p+1..B-1) false・(0,B) true の unit 追加。
b∈{p+1..19} の全ケースで完全・素直な場合分解で、対称性は不要)。
検証済み:

- **句スーパーセット検査**: 対照 (4,20,5) class{0} krow0:3 minpos1 (md5 362034b2…
  = records の ctrl 行と同一) に --x2=4 を付けた CNF は base の句集合を
  全含み、差分はちょうど3個の unit (¬cell(2), ¬cell(3), cell(4))。
  m=20 witness の V 像 (row 0 = (1,0),(4,0),(19,0)) は x2=4 バケットに属する
  ため、この対照インスタンスは SAT であるべき (kissat での実証は
  CPU が空き次第実施・記録する)。
- `sweepp0x2.sh`: bucket c0k3p0 (b=1..19) / c0k3p1 (b=2..19) の
  resumable driver (key=<bucket>b<b>・cap 900s・SAT/UNSAT/同cap行で skip)。


## 追記: 13:41Z 実行環境全面停止 — バックグラウンド2本の消失と再開手順

13:41Z 頃に bash・file_system を含む実行環境が全面停止した (GitHub API のみ生存)。
この時点で走行中・準備中だった次の2点は結果未記録のまま消失した
(プロセスは再起動で消滅。いずれも決定的実行なので再実行は同一軌道を辿る):

1. **c0k3p1 deep (deepcap.sh v2・正しい minpos=1・CNF md5 059fc19d…)** —
   cap 2400s での決着が未記録のまま消失 (~40分走行後)。
   再開は deepcap.sh v2 の再実行だけでよい (p0 は cap-2400 INDET 行で skip・
   p1 のみ正しく再実行される)。
2. **x2=4 対照の kissat SAT 実証** — 停止により未実施のまま。
   sweepp0x2.sh 起動前の必須較定として残っている
   (期待: SAT。m=20 witness の V 像 row 0 = (1,0),(4,0),(19,0) が b=4 バケットに属する)。


## 追記: SA pin-sweep (sandbox) — c0k3p0/p1 のヒューリスティック負と blocker 円ケース分割提案 (2026-11-15)

13:41Z 停止後、GitHub API + TS sandbox のみで実行した SA ヒューリスティック掃引を
[four-row-q5-m21-sa-pinsweep-20261115](../four-row-q5-m21-sa-pinsweep-20261115/) に新設した
(run 表・構造事実・厳密/ヒューリスティック区別つき)。要点:

- c0k3p1 相当 (p1: (0,0) 空・(1,0) 石) と c0k3p0 相当 (p0: (0,0) 石) を
  safeSwap SA (合計 ~11.3M iters) + g20-blocker ピン掃引 (p1 83 / p0 86 ケース) で探索し、
  witness (U=0) には未到達 (全称主張なし・ヒューリスティック)。
- (4,21) で (20,0) を通る >=5点円は19本・(0,0) を通るのも19本・両方を通るのは
  g* = {(0,0),(4,2),(9,3),(11,3),(16,2),(20,0)} の1本のみ (第二実装で再検証)。
- **次段階の具体提案 (x2 分割と直交する完全分解)**: バケットを
  「(20,0) が石」(unit 1本) と「(20,0) が空」(= 何らかの count-4 円 g∋(20,0) が存在する
  ため (g, 4-subset) でピン分割: p1 83 / p0 86 インスタンス) に完全分解する (計 84/87)。
  sat4.js 方式の unit pin で符号化可能。被覆の完全性の論証・静的フィルタは実験 README 参照。
- x2=4 対照の SAT 実証・c0k3p1 deep 再開と並行して、この blocker 分割の実装
  (sat5.js 相当) が決着への最短経路候補。


## 追記: blocker 円ケース分割の道具 (sat5.js + sweepp0gpin.sh)

SA pin-sweep の構造観察を厳密化した完全ケース分割を実装した
(設計・被覆論証: [four-row-q5-m21-sa-pinsweep-20261115](../four-row-q5-m21-sa-pinsweep-20261115/) の
「次段階提案」と sat5.js ヘッダ)。欠損行 y0=0 の右端セル (m-1, 0) について:

- **A: 右端セルが石** — unit 1 本 (key <bucket>gA)。対照 (4,20,5) では
  m=20 witness V 像 (row 0 = (1,0),(4,0),(19,0)) が右端 (19,0) を石として持つため、
  minpos1 + gpin=19:0 は SAT であるべき (較正用)。
- **B: 右端セルが空** — 極大性より (m-1,0) を通る count-4 円 g が存在し、
  安全性より g 上の石数はちょうど4。(g, S) でピン分割。
  sat5.js listcases (standalone census・計数法・C(k,3) sanity check) が列挙:
  - adapted (既定): minpos 石 (0,p) が g 上なら S は3セル (残り1石は minpos unit で
    既に固定)。**p1 81 / p0 86 ケース** (sandbox 検証済み)。
  - plain: |S|=4 固定 — SA 掃引記録 (p1 83 / p0 86) との 1:1 対照用
    (sandbox で 83/86 再現確認・g* のケースは pins 4:2,9:3,11:3,16:2 の1個)。
  - 幾何補題: 円と行の交点は <=2 → S 中の行0セルは右端を除き高々1個で、
    追加フィルタ不要。

A ∪ B の全 UNSAT ⟹ バケット UNSAT (完全被覆)。sat4.js --x2 とは直交
(x2 は素朴な第2石分割で「(20,0) が石」側も含む、gpin は右端セル基準の分割)。
sweepp0gpin.sh: resumable driver (key <bucket>gA / <bucket>g<i>・cap 900s)。

**較正 (実行環境復旧時・sweepp0gpin.sh 起動前に必須)**:
1. A の陽性対照: (4,20,5) class{0} krow0:3 minpos1 --gpin=19:0 → SAT 期待。
2. 句スーパーセット検査: 対照 CNF + --gpin / + --emptytail --gpin=... は
   base の句集合を全含み、差分はピンの unit のみ。
3. listcases の plain モードが p1=83 / p0=86、adapted が p1=81 / p0=86 を出すこと。


## 追記: blocker円分割の独立整数監査 (2026-11-15)

独立Python実装 [verify_blocker_split.py](scripts/verify_blocker_split.py) を追加し、
[sat5.js の adapted ケース列挙](blocker-split-independent-audit.md)を再検査した。
84点から全非共線三つ組を列挙する整数係数実装で、538円・右端 (20,0) を通る19円
(6点円17・5点円2) を再現し、各円の三つ組数が C(k,3) と一致することを確認した。

重要な補足として、**このバケットでは blocker は円に限られる**。
非水平直線は4行それぞれと高々1点で交わるため、右端点を含めても盤上点は高々4点。
水平線 y=0 は21点を含むが、対象バケットの行0はちょうど3石で q-1=4 に届かない。
したがって sat5.js の円だけの列挙で完全被覆になる。これは w=4, q=5, 欠損行の石数 k<=3
という範囲の補題であり、他の幅・q・行占有数にはそのまま拡張しない。

独立監査の結果:
- p1: 固定石 (1,0) も通る円が2本あり、adapted blocker は81件。A枝を加え82件。
- p0: 固定石 (0,0) も通る円が1本あり、adapted blocker は86件。A枝を加え87件。
- 旧SAのplain p1=83件には、固定石 (1,0) をピン集合から落とした実行不能枝が2件含まれる。
  いずれも同一円上に固定石を加えると5石になり、安全性に反する。SA記録の fail:2 と一致する。
- p1/p0 の正準ケース列SHA-256は監査JSONに保存。2回の監査実行でJSONはバイト一致。

再現:
```sh
python scripts/verify_blocker_split.py
```
出力: [blocker_split_independent_audit.json](output/blocker_split_independent_audit.json)。
**これは分割の独立監査であり、KissatのSAT/UNSAT判定ではない。**
82/87件のsolver結果は未取得で、M_{4,5} は [21,140] のまま。
