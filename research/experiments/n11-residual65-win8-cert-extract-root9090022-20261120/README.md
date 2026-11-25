# n11 残余65行 WIN8-D10 root `00000000000000909002200080100000` 証明書抽出・三重検証（2026-11-20）

## 目的

K1086（残余72行 add-two greedy 23根 depth-10 sweep、正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`・本実験dir内
`output/.input-k1086.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した7根のうち、**残余65行レーンで次安価の未着手候補
`00000000000000909002200080100000`（主張被覆4行・探査nodes 512,590/614,246）**
に対して、完全勝利戦略証明書（n11-terminal-strategy-v1
original_first_WIN8 second_to_move_LOSS）の盲抽出・独立検証を行った。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root9090022-single-owner-note.md`
（commit `0202057295a20f3c3c3e99036014697f34eecb58`）の下で実施した。
並走レーンが宣言済みの root `00000000000000202020008180000`
（commit 4496c888）・`…0810000a` とは別根であり、K1096（root `…8003180`・
fold11/K1105でfold済み）・K1106（root `…8005021`・fold12/K1107でfold済み）・
K1108（root `…9840004`・fold13候補・本実行の前段で抽出）とも独立の
プロセス・機材による抽出である（複数root抽出の独立導出の体）。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000000000909002200080000000`（root − 最小セットビット bit 20）+ bit 0 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1086出版値と
  node-exact一致: andclose1 loss=true nodes 512,590・andclose0 loss=true
  nodes 614,246・terminal石数 [14,18]
  （output/probe-repro-both-orderings.jsonl）。
- **root初手の独立再導出**: 8石 [20,31,45,49,60,63,68,71]・quadruple-free・
  root loser mobility 50を純Python整数4×4行列式で再導出
  （output/root-legal-moves.txt）。
- **抽出器**: K1096出版 `cert_extractor_win8_root8003180.ts` を
  root引数・filename guardのみ差し替えた `scripts/cert_extractor_win8_root9090022.ts`
  （探索核・修復はすべて同一bytes）。各root初手 m を extractW(root+m, 9) の
  盲抽出・自己検査付き。fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス50本、Run A2 = A1の完全再実行（同一cwd）、
  Run B = 全50初手を単一プロセスで一括（別cwd）。
  **3実行とも証明書bytes完全一致**（SHA-256
  `b8a15f9aac5e5f802f85459318247cb20bc983e3b2372167917ba8138cbc7a54`）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致。B（単一プロセス・memo温存）も
  総nodes 6,102,650でA1と同一（9840004ではBの方が小さかったが本rootでは
  chunk/単一プロセスのnode会計が一致。戦略行29,942は不変な点が本質）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（K1096/K1106/K1108出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`）:
  root+全50初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過不足0。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 50 sub-root全走査・consumed union。
  (3) 監査機械 `scripts/assemble_win8_audit_root9090022.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1108機械の
  root定数・期待値のみを差し替え（g05 mobility 50・g07 主張4行・g08 bit 20・
  probe nodes 512,590/614,246・g19 len(claimed)==4）、K1097 refsolve正本
  （SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の win16 footprint
  照合 g19を継承（K1086 greedy被覆行 == K1097 claimed == intrinsic の三点一致）。

 19 gate（g01〜g19）は K1108 と同構成: g01 K1086正本SHA pin・g02/g03 runner v17
 git blob c132cc64…の記録と原本一致・g04 root shape safe・g05 mobility 50・
 g06 K1086 probes win uncapped・g07 主張4行・g08 probe再現 node-exact・
 g09 root初手リスト==独立再導出・g10 A1/A2 clean・g11 A1==A2 per-move
 node-exact・g12 B clean・g13 chunk vs 単一プロセスのnode会計・g14 証明書
 sorted-unique・末尾改行・行format・g15 B nRows==証明書行・g16 第三方法全木
 再走査PASS・g17 BigInt/Bareiss/python三者の全集計値一致・g18 解釈guard文言
 存在・g19 K1097 footprint三点一致。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行byte-identical)

- **証明書**: `certs/win8-root-00000000000000909002200080100000-20261120.n11`
  ・1,082,873 bytes・29,942戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `b8a15f9aac5e5f802f85459318247cb20bc983e3b2372167917ba8138cbc7a54`。
- **root**: 8石 [20,31,45,49,60,63,68,71]・quadruple-free・loser初手は50手。
  K1086 greedy主張被覆4行 `…80122200000010000`・`…801222000000800000`・
  `…909002000000100000`・`…909002000080000000` はK1097
  win16 footprint（intrinsic == claimed）とも一致（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎50プロセス）総nodes 6,102,650・最大初手
  nodes 476,446（bit 10）・fbt_drops 0（全50初手）・fatal/conflict 0。
  Run B総nodes 6,102,650・戦略行29,942で内容不変。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 65,134（sub-root単位）・winner-to-move 42,115・loser-to-move 12,780・
  loser応手辺 58,084・終端 10,239（全てloser-stuck）・終端石数 [14,18]・
  consumed union 29,942 == 証明書行29,942（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 50。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `00836a6e859c780e2204b1aea427eefc044f0d4c5a6b8e8c33505a57fa950bb4`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回（EXPERIMENT_ROOT）で
  audit JSON byte-identical・時刻・乱数入力なし）。
- 実装上の注記: 移行時のfail-closed確認として、g19の `len(fp["claimed"]) == 3`
  （9840004の主張3行の定数）を `== 4` に修正するまで g19 が PASS しなかった。
  監査機は期待値の不一致を正しく拒否した（fail-closed作動の実証）。

## 再現

```
# probe再現（pilot込み・K1086出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000000000909002200080000000 \
  --bits 20 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000000000909002200080000000 \
  --bits 20 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root9090022.ts \
  --root 00000000000000909002200080100000 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 50 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000000000909002200080100000 --root-check
# 検証3: python3 scripts/assemble_win8_audit_root9090022.py --out output/….json
```
