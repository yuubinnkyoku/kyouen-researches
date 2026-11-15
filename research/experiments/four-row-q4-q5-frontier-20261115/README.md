# four-row-q4-q5-frontier-20261115

IN FLIGHT (claim) — 高速レーン。`four-six-row-q4-q5-band-extension-20261115`
（最終push 2026-11-15T00:28Z・セッション終了形）が残した前線を takeover して進める:

- **(4,4) m=35** — def-mode 260s INDET / 317,151 conflicts（同レーン・honest negative）。
- **(4,5) m=21** — rowY=0..3 が 55s cap で INDET、rowY=3 200s 再実行 2,714,555 conflicts
  （前レーン `four-six-row-q4-q5-witness-search-20261114`）。加えて
  `w4-w5-q5-surgery-20261115` の bounded-edit 局所ネガティブ（(3,4) 近傍 0 witness・不在主張ではない）。
- (6,4) m=41・(5,4) m=40 — 同 band-extension レーンの前線（前例: m=40 rowY=0 SAT 5,864 conflicts/172.9s、
  m=39 rowY=1 SAT 21,147/197.1s）。1歩延伸を本レーンで先行する。

(5,5) m=26+ は対象外: `five-row-q5-m24-class-split-20261115` が自動延伸中で
M_{5,5} ∈ [26, 336] に更新済み（cross-lane convergence は surgery レーン README 参照）。

collision protocol: push前に必ず最新mainを取り直す。他レーンが同一 (w,m,q) に
着手済み（IN FLIGHT claim または結果push）の場合、本レーンが譲って対象を外す。

## 着手時点の境界（main 04a781f5 時点・CSV `results/fixed-width/mwq_stabilization.csv`）

| family | 現在 | 前線 | 上界 |
|---|---|---|---|
| (4,4) | witness 帯 m=4..34・M ∈ [35, 237] | m=35 | K0068 T_4=237 |
| (4,5) | witness 帯 m=5..20・M ∈ [21, 140] | m=21 | K0318 U=140 |
| (5,4) | witness 帯 m=5..39・M ∈ [40, 567] | m=40 | K0068 T_5=567 |
| (6,4) | witness 帯 m=6..40・M ∈ [41, 1113] | m=41 | K0068 T_6=1113 |

## 手法

- 生成器: sat3.js streaming census（md5 18ab1e432bf85f293015922898bb765d・
  `seven-row-q4-extension-band-sat3-20261115/scripts/` から再利用・commit しない）。
- ソルバ: kissat 4.0.4 official prebuilt linux-amd64
  （md5 3a5eba830aa6008a604fcc9bbe99a325・不変）。
- runner: band-extension レーンの `scripts/lean5.sh` を **verbatim 再利用**
  （`four-six-row-q4-q5-band-extension-20261115/scripts/lean5.sh`・commit しない。
  kissat は同スクリプトの既定パス `/home/user/krwork/kissat-4.0.4-linux-amd64`
  に同一 md5 バイナリを配置して実行）。sat3 生成 + kissat + JSONL record +
  SAT 時 decode + js/sat.js verifyConfig と verify_witness.py Python Fraction の
  2系統検証・CNF は実行後削除し cnf_md5 を記録。

### w=4 rowfixed 2クラス被覆補題（UNSAT 完全性の根拠）

sat3/sat2 の rowfixed モードは「行 rowY が ≤ q-2 石」を固定し、lex 制約は
`lexLeader` により「行優先辞書順で最初の相違位置において config ≤ σ(config)」
を課す（σ ∈ SIG={H,V,HV}、H=左右反転・V=上下反転）。

**補題**: w=4 の固定幅 m において
`rowfixed(0) ∧ lex=H` と `rowfixed(1) ∧ lex=H` がともに UNSAT なら、
その幅に欠損（ある行 ≤ q-2 石）極大安全配置は存在しない（witness-free）。

**証明**: 基本制約 Base（全曲線 at-most-(q-1) + 各空点の極大性）は H と V の
両方で不変である（H,V は w×m 格子点集合の幾何対称で、直線→直線・円→円を
誘導し、H は行を保存、V は行 y ↔ 3−y を送る）。D を欠損行 r を持つ
Base-解とする。r ≥ 2 なら V(D)（欠損行 3−r ≤ 1）に置き換えてよい。
D′ の H-軌道 {D′, H(D′)} の行優先辞書式最小元 E は E ≤ H(E) を満たし、
H が行を保存するので E の欠損行は 3−r ≤ 1 のままである。
よって E は Base ∧ rowfixed(3−r) ∧ lex=H を満たす。∎

**注記**: lex=V / lex=HV は行を動かすため、full-lex (H,V,HV) では
{rowY=0,1} の2クラスでは被覆しない（4クラス必要）。したがって
前レーンの rowY=0..3 full-lex INDET は absence には使えず、本レーンの
lex=H 単独の2クラスが absence 可能な初の走査である。
逆に SAT の場合はどの lex・クラスでも witness として有効（lex 制約は
制約の追加のみで、充足解は常に真の witness）。

## 較正（着手時に実施済み・全 PASS）

- 生成器 byte-exact: (4,35,4) def lex=H,V,HV の CNF md5
  `989d302b9383c9d8f86ce5d78a09657d`、(6,32,4) def lex=H,V,HV の
  `3091b70f7925641c4a9c428b0f688dd3` — ともに band-extension レーン記録と一致。
- ソルバ bit-exact: (6,32,4) SAT **782 conflicts**（レーン記録 782・一致）。
  lean5.sh 端 to 端再現も PASS（同一 witness・js+py 2系統検証 ok）。
- kissat 4.0.4 binary md5 一致（上記）。

## スコープ

有限機械検証まで。各幅の SAT はその幅の欠損極大安全配置の存在証明
（witness 有限証拠）。2クラス UNSAT は上の補題により witness-free の
完全証明（M の確定）。INDET は cap 到達であり不在を意味しない。
上界（K0068 parity / K0318 substitution）は不変。

## 結果（2026-11-15・バッチ1〜6）

1. **(6,4) m=41 SAT**（rowY=0・lex=H,V,HV・245.2s・8,226 conflicts・17石
   rows [2,3,3,3,3,3]）— **witness 帯 m=6..41・M_{6,4} ∈ [42, 1113]**。
   js+py 2系統検証 + 第3系統（純TS/BigInt・陽性/陰性対照つき）PASS
   （output/ts-verify-frontier.json）。前線 m=42。
2. **(4,4) m=35**: 2クラス被覆掃引（rowY=0/1・lex=H）ともに 600s INDET
   （324,870 / 230,642 conflicts）— honest negative。不在主張ではない。
   M_{4,4} ∈ [35, 237] は不変。
3. **(4,5) m=21**: 2クラス被覆掃引ともに 600s INDET（6,924,496 / 7,286,846
   conflicts・合計 ~14.2M）— honest negative。M_{4,5} ∈ [21, 140] は不変。
4. **(5,4) m=40**: rowY=1 600s INDET 191,445 conflicts — honest negative。
   M_{5,4} ∈ [40, 567] は不変・前線は m=40 のまま。
5. 運用: wrapper (lean5.sh) が cap 到達時に環境側で殺されることがあったため、
   records.jsonl の一部は kissat.txt 最終 stats からの復元（各 record の note
   に明記・conflicts は決定性により bit-exact）。
