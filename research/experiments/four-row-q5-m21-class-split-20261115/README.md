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
