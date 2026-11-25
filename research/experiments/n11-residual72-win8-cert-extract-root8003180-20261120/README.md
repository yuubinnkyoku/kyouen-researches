# n11 残余72行 WIN8-D10 root `00000000000000003800000008003180` 証明書抽出・三重検証（2026-11-20）

## 目的

K1086（残余72行 add-two greedy 23根 depth-10 sweep、正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`）が
両AND順序 uncapped で WIN8-D10 candidate として確定した7根のうち、
**`00000000000000003800000008003180`（greedy計画順第一位・主張被覆4行）**
に対して、完全勝利戦略証明書（n11-terminal-strategy-v1 original_first_WIN8
second_to_move_LOSS）の盲抽出・独立検証を行った。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-win8-cert-extract-root8003180-single-owner-note.md`
（commit 0360f21a）の下で実施した。並走レーンが宣言済みの root
`00000000000200003800200008180000`（commit 4496c888）とは別根であり、
本実験は両rootの抽出が互いに独立のプロセス・実装で行われることの
「独立第二導出」でもある。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000003800000008003100` + bit 7 の両AND順序 depth-10 probeを
  計4回実行（各順序2回）。いずれも K1086出版値とnode-exact一致:
  andclose1 loss=true uncapped nodes 903,977・andclose0 loss=true uncapped
  nodes 1,146,417・terminal石数 [14,18]（output/probe-repro-both-orderings.jsonl）。
- **root初手の独立再導出**: 8石・quadruple-free・root loser mobility 53を
  純Python整数4×4行列式で再導出（output/root-legal-moves.txt）。
- **抽出器**: repo-verbatim WIN7 extractor
  `n11-residual78-seventeenth-win7-cert-extract-20261120/scripts/class4_child1_cert_extractor_exact_ms23.ts`
  （git blob `c267f260d1d6fcc49ed5367509e854c81822497e`）を基礎に、
  (1) fbtOR に runner v17 の saturated-chain 直接計算修復を適用
  （fbt_drops==0 は構成で保証され、修復-path回数は fbt_fallbacks で別計上）、
  (2) 戦略行書き込みを recordRow() に通して同一局面の選択手衝突をfatal化、
  (3) 8石root駆動バッチ（各root初手 m を extractW(root+m, 9, null) の盲抽出・
  自己検査付き）に改変した `scripts/cert_extractor_win8_root8003180.ts`。
  探索核（規則・順序・memoisation・extractW/extractL再帰）は基礎抽出器と同一。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス53本（cwd A・チャンクrowは逐次書き出し）、
  Run A2 = A1の完全再実行（同一cwd）、
  Run B = 全53初手を単一プロセスで一括（別cwd別プロセス）。
  **3実行とも証明書bytes完全一致**（SHA-256 `1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c`）。
  チャンク分割が戦略内容を変えないこと（memo状態非依存の位置事実のみをcacheする
  ため選択手は不変）も、A1とBの一致が実証した。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（seventeenth検証器 `verify_win7_certificate_bigint_independent.mjs`
  git blob `62b5d9413daafb172f6e10249976ee6808f7b454` のWIN8化・root 8石・
  終端域窓 12..20 + 正確域検査）: root+全53初手から全木走査・全winner行の消費・
  選択手合法性・全loser応手展開・終端はloser-stuckのみ・被覆union過不足0。
  (2) TS Bareiss 4×4整数行列式（`verify_bit7_win7_cert.ts` のWIN8化・sub-root 9石）:
  root-check + 53 sub-root全走査・consumed union。
  (3) 監査機械 `scripts/assemble_win8_audit_20261120.py`（Python stdlibのみ・
  engine/探索器importなし・第三実装として独自に全木を再走査し、
  K1086入力SHA pin・probe再現照合・root再導出・抽出summary整合・証明書形式を
  含む **18 gate をfail-closed**）。

## 結果（全18 gate PASS・3方法の全数値一致・証明書3実行byte-identical）

- **証明書**: `certs/win8-root-00000000000000003800000008003180-20261120.n11`
  ・1,251,923 bytes・34,529戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c`。
- **root**: 8石 [7,8,12,13,27,59,60,61]・quadruple-free・loser初手は53手。
  K1086の主張被覆4行
  （`…8001080`, `…8001100`, `…8002080`, `…8002100`）はfold時に別途扱う。
- **抽出費用**: Run A1（初手毎53プロセス）総nodes 3,394,332・最大初手 m=66 の
  250,205 nodes・fbt_drops 0（全53初手）・fatal/conflict 0。
  Run A2 は A1 と初手単位で nodes/terminalRange 完全一致。
  Run B（単一プロセス・memo温存）総nodes 2,608,236・戦略行34,529で内容不変
  （抽出のnode費用はmemo状態依存、戦略は非依存の実証）。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 76,955（sub-root単位）・winner-to-move 49,509・loser-to-move 14,082・
  loser応手辺 67,420・終端 13,364（全てloser-stuck）・終端石数 [14,18]・
  consumed union 34,529 == 証明書行34,529（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 53。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da`・
  18/18 gate PASS・別cwd別プロセス再実行でaudit JSON byte-identical・
  時刻・乱数入力なし）。

## 再現

```
# probe再現（pilot込み・K1086出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000000003800000008003100 \
  --bits 7 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000003800000008003100 \
  --bits 7 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txt）
node --experimental-strip-types scripts/cert_extractor_win8_root8003180.ts \
  --moves <m> --subtree-depth 9 --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 53 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
#           --cert certs/…n11 --root-check
#         node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts \
#           --cert certs/…n11 --subroots <csv> --consumed-out consumed.txt
# 監査（第三方法+全簿記gate）: python3 scripts/assemble_win8_audit_20261120.py \
#           --out output/win8-cert-extract-verification-20261120.json
```

入力SHA pin: K1086正本（`output/.input-k1086.json`・SHA-256 3045e152…）・
runner v17 git blob c132cc6425…。抽出 '*'は入力を読み取らない盲抽出で、
K1086との照合はgate側で行う。

## 解釈規約

1. 本証明書は「8石root 00000000000000003800000008003180 で手番側が
   深さ10以内に必敗する」ことの完全戦略証明であり、直前の着手を打った側の
   深いroot（S6親行・二石root・空盤）の勝敗ではない。
2. 8石receiptの被覆幾何・foldによるS6行閉鎖は別の宣言を要する別工程である
   （K1086も「fold意味論は本掃引では確定しない」と明記）。
3. REFUTED-D10・nodes数・solved数を勝敗として読まない。
4. **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
   すべて UNKNOWN のまま。** 残余72行の閉鎖行数は0のまま。

## 次の一手（着手時は単一オーナー宣言を要する）

- 残るWIN8-D10 candidate の証明書抽出（K1086の5根〔並走1根を除く〕と
  K1089/K1091の2群3+3根）。本実験の抽出器・検証器・監査機械はroot差し替えで
  再利用可能。
- 8石receipt被覆幾何（「8 D4像×2石除去」join）の設計と、証明書×receiptに
  よるfold機械（K1086主張の被覆4行の閉鎖に必須）。
- 抽出済み証明書は fold 時の署名入力となる（証明書SHAを正本にpin）。
