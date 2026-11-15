# (6,4) 6×47 rowY=0 — kissat RAM 壁の記録 (2026-11-15 高速レーン)

## 位置づけ

`M_{6,4} ∈ [47, 1113]` (witness 帯 m=6..46・上界 K0068 T_6=1113、K0833)。
前線 m=47。m=41..46 の witness はすべて rows [2,3,3,3,3,3] 型
(欠損行 = row 0・2石) で、free-column append は m=47 で cell (46,0) が
未遮断になり停止 (four-row-q4-q5-frontier-20261115)。よって rowY=0 固定分割
(V は 0↔5・1↔4・2↔3 で rowY クラスは 0,1,2 の3類) が最有力の試行順。

## status

**INDET/OOM (方法論的負記録。6×47 witness の不在主張ではない)**

## 記録

sat3.js streaming census (rowY 固定分割版・7r) で 6×47 q=4 rowY=0
lex=H,V,HV の CNF 生成に成功したが:

- vars 2,701,853 / clauses 8,965,702 / curves 259,412
- CNF md5 `e2c7ab7255893ea4e974a479bd04c8f3` (生成は決定的)
- kissat 4.0.4 (公式静的バイナリ md5 3a5eba830aa6008a604fcc9bbe99a325) が
  **rc=137 (SIGKILL/OOM) で 14.3s で死亡** (cap 900s に遠く届かない)
- sandbox RAM ~2.1GB が制約。frontier レーンの m=41..45 (最大 581s・
  cap 1200s で完走) と同じ符号化・ソルバでここだけ即死するのは
  CNF 規模の増大 (vars 2.7M) による RSS 増大が RAM 上限を超えるため。

## 解釈と含意

1. これは**判定ではなく環境障害の記録**である。6×47 の witness 有無は未解決。
2. (6,4) rowY 固定分割の frontier は m=46 (構成的 witness) まで。
   m=47 の決着にはメモリ効率の符号化 (census 前の曲線剪定・変数削減・
   DIMACS 圧縮オプション) か、より大きい RAM の実行環境が必要。
3. rowY 実例の lex=H,V,HV 併用は witness 探索用の制限であり、
   仮に UNSAT が出ても単独では不在証明にならない
   (frontier レーンの用法と同一)。

## files

- `scripts/sat3.js` — rowY 固定分割 streaming census 符号化 (7r 版・
  md5 18ab1e432bf85f293015922898bb765d)
- `scripts/sat.js` — K0810 census・検証器 (依存)
- `output/records.jsonl` — 上記1行の生記録 (meta: vars/clauses/curves/cnf_md5)
- `output/s6x47q4_rowY0_HVHV.meta.json` — CNF 生成 meta
- `output/s6x47q4_rowY0_HVHV.kissat.txt` — rc=137 の生ログ
