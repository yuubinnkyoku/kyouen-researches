# n11 残余58行 WIN8-D10 root `00000000010000889002000080100000` 証明書抽出・三重検証（2026-11-20）

## 目的

K1086（残余72行 add-two greedy 23根 depth-10 sweep、正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`・本実験dir内
`output/.input-k1086.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した根のうち、**fold13/K1110・fold14/K1111（残余62→58行）後の
残余58行レーンで最安価の未抽出・未宣言候補
`00000000010000889002000080100000`（主張被覆4行・探査nodes 409,407/575,570）**
に対して、完全勝利戦略証明書（n11-terminal-strategy-v1
original_first_WIN8 second_to_move_LOSS）の盲抽出・独立検証を行った。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00010000889002000080100000-single-owner-note.md`
（commit `60e2940cf079c8e98efc9c0e72150835b87e5184`）の下で実施した。
並走レーンが宣言済みの root `…8180000`（commit 4496c888）・`…0810000a`
とは別根であり、K1096（root `…8003180`・fold11/K1105）・K1106（root `…8005021`・
fold12/K1107）・K1108（root `…9840004`・fold13/K1110）・K1109（root `…9090022`・
fold14/K1111）で抽出・fold済みの4根とも独立のプロセス・機材による抽出である
（複数root抽出の独立導出の体）。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論（「8 D4像×2石除去」join）は別工程であり、
本実験では確定しない。REFUTED-D10 は LOSS 証明ではない。
nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108/K1109と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000010000889002000080000000`（root − 最小セットビット bit 20）+ bit 20 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1086出版値と
  node-exact一致: andclose1 loss=true nodes 409,407・andclose0 loss=true
  nodes 575,570・terminal石数 [14,18]
  （output/probe-repro-both-orderings.jsonl）。
- **root初手の独立再導出**: 8石 [20,31,49,60,63,67,71,88]・quadruple-free・
  D4正準（8対称像中最小hexがroot自身）・root loser mobility 50を
  純Python整数4×4行列式で再導出（output/root-legal-moves.txt）。
- **抽出器**: K1109出版 `cert_extractor_win8_root9090022.ts` を
  root引数・filename guardのみ差し替えた `scripts/cert_extractor_win8_root8890020.ts`
  （探索核・修復はすべて同一bytes）。各root初手 m を extractW(root+m, 9) の
  盲抽出・自己検査付き。fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス50本、Run A2 = A1の完全再実行（同一cwd）、
  Run B = 全50初手を単一プロセスで一括。
  **3実行とも証明書bytes完全一致**（SHA-256
  `105e1e2ad59f4f6baa85f37dde7306b98fc96d2164edf5b5d12205b1c71e2bc4`）。
  A1/A2は初手単位で nodes/nRows/fbt 完全一致。B（単一プロセス・memo温存）も
  総nodes 4,424,758でA1と同一（9090022と同じくchunk/単一プロセスのnode会計が
  一致。戦略行21,446は不変な点が本質）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（K1096/K1106/K1108/K1109出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`）:
  root+全50初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過不足0。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check + 50 sub-root全走査・consumed union。
  (3) 監査機械 `scripts/assemble_win8_audit_root8890020.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1109機械の
  root定数・期待値のみを差し替え（ROOT_HEX・CERT_RELPATH・
  probe nodes 409,407/575,570・実験名。g05 mobility 50・g07主張4行・g08 bit 20・
  g19 len(claimed)==4 は9090022と同じ4行構成のため不変）、K1097 refsolve正本
  （SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の win16 footprint
  照合 g19を継承（K1086 greedy被覆行 == K1097 claimed == intrinsic の三点一致）。

19 gate（g01〜g19）は K1109 と同構成: g01 K1086正本SHA pin・g02/g03 runner v17
git blob c132cc64…の記録と原本一致・g04 root shape safe・g05 mobility 50・
g06 K1086 probes win uncapped・g07 主張4行・g08 probe再現 node-exact・
g09 root初手リスト==独立再導出・g10 A1/A2 clean・g11 A1==A2 per-move
node-exact・g12 B clean・g13 chunk vs 単一プロセスのnode会計・g14 証明書
sorted-unique・末尾改行・行format・g15 B nRows==証明書行・g16 第三方法全木
再走査PASS・g17 BigInt/Bareiss/python三者の全集計値一致・g18 解釈guard文言
存在・g19 K1097 footprint三点一致。

## 環境リセットを跨いだ決定的再現（今回独自の記録）

初回抽出（同一プロトコル・A1/A2/B完了・BigInt/Bareiss/監査19 gate PASS
まで到達）の直後に実行環境（Koyeb sandbox・503 upstream reset）が消失し、
ローカル作業dirを喪失した。本実験dirの機材はすべてrepo出版正本
（commit `9ca77ca60a` の K1109 実験dir・SHA pin照合済み）から再取得し、
全工程（probe再現 → A1/A2/B → 証明書化 → BigInt/Bareiss/監査）を再実行した。
結果: **証明書SHA-256・総nodes 4,424,758・全行集合21,446・三重検証の全数値が
初回記録と完全一致**（抽出パイプライン全体が環境を跨いでbyte-exact再現した
2例目。K1036の証明書再現に続き、監査JSONの再構成まで含む初の例）。

## 結果（全19 gate PASS・3方法の全数値一致・証明書3実行byte-identical）

- **証明書**: `certs/win8-root-00000000010000889002000080100000-20261120.n11`
  ・775,317 bytes・21,446戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `105e1e2ad59f4f6baa85f37dde7306b98fc96d2164edf5b5d12205b1c71e2bc4`。
- **root**: 8石 [20,31,49,60,63,67,71,88]・quadruple-free・D4正準・loser初手は50手。
  K1086 greedy主張被覆4行 `00000000000000889002000000100000`・
  `00000000000000889002000080000000`・`00000000010000809002000000100000`・
  `00000000010000809002000080000000` はK1097
  win16 footprint（intrinsic == claimed）とも一致（g19）。fold時は別工程。
- **抽出費用**: Run A1（初手毎50プロセス）総nodes 4,424,758・最大初手
  nodes 937,490（bit 14）・fbt_drops 0（全50初手）・fatal/conflict 0。
  Run B総nodes 4,424,758・戦略行21,446で内容不変。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 48,855（sub-root単位）・winner-to-move 31,320・loser-to-move 9,882・
  loser応手辺 43,837・終端 7,653（全てloser-stuck）・終端石数 [14,18]・
  consumed union 21,446 == 証明書行21,446（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 50。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `b8c264e671b9e26fa9caf8cd2454f75b13c992d548e2d5ed0b02f2bec75c5236`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回（EXPERIMENT_ROOT）で
  audit JSON byte-identical・時刻・乱数入力なし）。

## 再現

```
# probe再現（pilot込み・K1086出版値とnode-exact一致を確認）
node --experimental-strip-types runner_v17.ts --child 00000000010000889002000080000000 \
  --bits 20 --depth 10 --cap 30000000 --andclose 1 --out repro.jsonl
node --experimental-strip-types runner_v17.ts --child 00000000010000889002000080000000 \
  --bits 20 --depth 10 --cap 30000000 --andclose 0 --out repro.jsonl
# 抽出（初手ごとに1プロセス。movesはoutput/root-legal-moves.txtのカンマCSV）
node --experimental-strip-types scripts/cert_extractor_win8_root8890020.ts \
  --root 00000000010000889002000080100000 --moves <m> --subtree-depth 9 \
  --summary-out s.jsonl --rows-out rows-m<m>.txt
cat rows-m*.txt | sort -u   # → header+root行を前置して証明書化
# 検証1: node scripts/verify_win8_certificate_bigint_independent.mjs certs/…n11 50 14,18
# 検証2: node --experimental-strip-types scripts/verify_win8_cert_bareiss.ts --cert … \
#   --root 00000000010000889002000080100000 --root-check
# 検証3: python3 scripts/assemble_win8_audit_root8890020.py --out output/….json
```
