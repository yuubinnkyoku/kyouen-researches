# 2026-11-18 N11 cost-16 parent sextet-era census — k=26/27/28のquint階打ち切りを機械確定で閉じた

##要点

31行のcost-16 parent `00000000000000003800000008001000` のquint時代I-E（`kill(k) = Σm − Σj2 + Σj3 − Σj4 + Σj5`・第六階項なし）の健全性を、size 6以上の**全数census**で機械確定した。k=26出版でj5項が登場して以来、size 6以上の構造的ゼロはどの publicationでも機械検証されておらず、今回が最初の確定である。

- **C(26,6) = 230,230 本 → オールゼロ**: 出版済み kill(26)（commit `3b68d6b4`）の第5階打ち切りを**遡及的に閉じた**
- **C(27,6) = 296,010 本 → オールゼロ**: 出版済み kill(27)（commit `9b804a9c`）の第5階打ち切りを**遡及的に閉じた**
- **C(28,6) = 376,740 本 → オールゼロ**: 次段のk=28計算はk27機構の拡張のままでよく、第六階項は不要
- 補助アンカー: **C(28,7) = 1,184,040 本・C(28,8) = 3,108,105 本 → オールゼロ**
- 二重独立分類器（Map重複カウント vs 行bitmask/popcount）で全6.2M組を再導出し**不一致0**

## hereditary closure（閉包の原理）

zero分類は**superset-closed**である（rootを追加しても行の多重度は下がらない。2回行が2本以上または3回行を持つsubsetの上位集合も同じ性質を持つ）。A-type最小cover（15本のdisjoint pair + 1本のdisjoint singleton: 全行ちょうど1回）もB-type（16 pair: ちょうど1行だけ2回）もzero subsetを含められないので、zero subsetのjointは厳密に0。よって「全C(n,6)がzero」なら size ≥ 6 の全subsetがzeroになり、I-Eは第五階で終わる。C(28,7)/C(28,8)の全ゼロはこの補題の実測アンカーである。

## blocking-set性質（なぜsextetが存在しないか）

b_only quintの9行unionは、上位k rootの**他の全rootを被覆する壁**になっている:

| 上位対象 | b_only quint数 | 外部root×quint組 | unionに触れる | 完全disjoint |
|---|---:|---:|---:|---:|
| top-26 | 1,872 | 39,312 | 39,312 | **0** |
| top-27 | 2,181 | 47,982 | 47,982 | **0** |
| top-28 | 2,512 | 57,776 | 57,776 | **0** |

つまりb_only quintに他のどんなrootを6本目として加えても、6本目の2行のうち少なくとも1行がquintの9行unionに触れ、即座に「2重行2本以上」または「3回行」のzeroになる。B-typeで拡張できる唯一の見込み（6本目がunionに完全disjoint）が top-28まで構造的に潰れている。この性質が崩れるkが quint時代の「sextet時代」の開始条件になる。

## 検証

- 固定入力: aggregate blob `31bdefdb2e2cc90b706cbb8090e98eb5eece4d87`・k26 result blob `1841a281ff604e7f677b8c7772a7312f6f9da5e1`・k27 result blob `3dc30ad6c51cc2d7678cc8777e4af2376267ddb8`
- 11 checks all PASS・実行30.5秒・出版スクリプトは固定blob SHA-1を検査してから同じ計算を行う
- 出版済みk26/k27 `ie_mechanism` 文言（`+ sum j5`）とquint census値（1,872/2,181）を文脈照合
- なお、この実行では公開スクリプト自体をリポジトリcheckout上で起動してはいない（repo-root引数付きで同一計算）

## 位置づけ・並走整理

- 並走レーンのrank-28 preread（commit `e6cc8e05`・13:22:30）のcensus値（pair 14/13・triple 214/99/38・quad 626/2,277/22・quint 331/17,219/0・二重行hist {15:38,18:255,19:38}・m28 = 120,361,466,461,719,625）は自レーンの独立導出と全値一致（第三の二重導出）。ただし同preread（およびk26/k27 publications）には size ≥ 6 censusが含まれず、本成果はそれを補完する独立成果である。
- k27出版JSON `structure.quints_jsonl_note` に「reclassifies all 65,730 5-subsets」であるべき箇所に**「65,780」（=C(26,5)）の文言が残存**している（cosmetic・k26→k27変換の取りこぼし・値系は全て正確）。quiet-window修正候補として記録する（k28 JSON生成時は自レーン分の文言を正しく更新する）。

これは包含排除打ち切りの健全性検証であり、探索コスト・WIN/LOSS verdict・ゲーム理論的値ではない。長時間探索やPm計算は今回起動していない（size ≥ 6 のPm joint値は全て構造的ゼロとして計算していない）。

**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。**
