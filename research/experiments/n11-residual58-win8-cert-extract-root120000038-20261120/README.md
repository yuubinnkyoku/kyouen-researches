# n11 残余58行 WIN8-D10 root `00000000012000003800080009000000` 証明書抽出・三重検証（2026-11-20）

## 目的

K1086（残余72行 add-two greedy 23根 depth-10 sweep、正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`・本実験dir内
`output/.input-k1086.json` にSHA pin）が両AND順序 uncapped で WIN8-D10 candidate
として確定した7根のうち、**残余58行レーンで未宣言の次安価候補
`00000000012000003800080009000000`（主張被覆3行・探査nodes 657,152/825,127）**
に対して、完全勝利戦略証明書（n11-terminal-strategy-v1
original_first_WIN8 second_to_move_LOSS）の盲抽出・独立検証を行った。

単一オーナー宣言ノート
`research/log/2026-11-20-n11-win8-cert-extract-root00000000012000003800080009000000-single-owner-note.md`
（commit `26c88746b24dc510cb42f3cd64ec0ee746f6da06`）の下で実施した。
並走レーンが宣言済みの root `00000000000200003800200008180000`
（commit 4496c888）・`…0810000a`・`00000000010000889002000080100000`
（commit 60e2940cf0）とは別根であり、K1096（root `…8003180`・fold11/K1105）・
K1106（root `…8005021`・fold12/K1107）・K1108（root `…9840004`・fold13/K1110）・
K1109（root `…9090022`・fold14/K1111）で抽出・fold 済みの4根とも独立の
プロセス・機材による抽出である（複数root抽出の独立導出の体）。

**本証明書は当該8石rootのゲーム木だけを証明する**。S6親行の閉鎖に必要な
8石receiptの被覆幾何・fold意味論は別工程であり、本実験では確定しない。
REFUTED-D10 は LOSS 証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**

## プロトコル（K1096/K1106/K1108/K1109と同一・全機材は本dirに同梱）

- **verdict基盤の再現**: runner v17 repo原本固定コピー（git blob
  `c132cc6425eee3feaeef1d697dd74f968cfedb59`・pilot_d6制御 nodes 3,402）で
  child=`00000000012000003800080008000000`（root − 最小セットビット bit 24）+ bit 24 の
  両AND順序 depth-10 probeを計4回実行（各順序2回）。いずれも K1086出版値と
  node-exact一致: andclose1 loss=true nodes 657,152・andclose0 loss=true
  nodes 825,127・terminal石数 [14,18]
  （output/probe-repro-both-orderings.jsonl）。
- **root初手の独立再導出**: 8石 [24,27,43,59,60,61,85,88]・quadruple-free・
  root loser mobility **53**（K1096/K1106/K1108/K1109の50と異なる本root固有値）を
  純Python整数4×4 Bareiss行列式で再導出（output/root-legal-moves.txt）。
- **抽出器**: K1109出版 `cert_extractor_win8_root9090022.ts` を
  root引数・filename guard・表題コメントのみ差し替えた
  `scripts/cert_extractor_win8_root120000038.ts`（探索核・修復はすべて同一bytes・
  diffは6行）。各root初手 m を extractW(root+m, 9) の盲抽出・自己検査付き。
  fbtOR 修復込みで fbt_drops==0。
- **抽出3実行**（いずれも決定的・乱数・時刻依存なし）:
  Run A1 = 初手ごと新規プロセス53本・4並列で実行、Run A2 = A1の完全再実行
  （同一cwd・初手単位でrowsファイルもbyte一致）、Run B = 全53初手を
  単一プロセスで一括（別cwd）。
  **3実行とも証明書行集合完全一致**（32,470行）。
  A1/A2は初手単位で nodes/nRows/fbt/terminalRange 完全一致。
  B（単一プロセス・memo温存）は総nodes 2,141,807 と A1 chunk合計 2,723,200
  より小さく（9840004型の会計差）、行集合は同一。
  実行中に誤root引数での起動を1回行ったが抽出器は fatal=0 で行出力を
  拒絶した（fail-closed作動の追加実例・rows/summaryは一切出力されず）。
- **独立検証3方法**:
  (1) TS BigInt 3×3余因子展開（K1096/K1106/K1108/K1109出版検証器の同一bytes・
  `scripts/verify_win8_certificate_bigint_independent.mjs`・期待mobility 53・
  期待終端石数 [14,18] をCLI pin）:
  root+全53初手から全木走査・全winner行の消費・選択手合法性・全loser応手展開・
  終端はloser-stuckのみ・被覆union過不足0。
  (2) TS Bareiss 4×4整数行列式（`scripts/verify_win8_cert_bareiss.ts`・同一bytes）:
  root-check（stones 8・loserMobility 53）+ 53 sub-root全走査・consumed union。
  (3) 監査機械 `scripts/assemble_win8_audit_root120000038.py`（Python stdlibのみ・
  engine importなし・第三実装として独自に全木を再走査）。K1109機械の
  root定数・期待値のみを差し替え（g05 mobility 53・g07 主張3行・g08 bit 24・
  probe nodes 657,152/825,127・g17 loserMobility 53・g19 len(claimed)==3）、
  K1097 refsolve正本（SHA-256 `2896deb0…`・`output/.input-k1097.json` にpin）の
  win16 footprint 照合 g19 を継承（K1086 greedy被覆行 == K1097 claimed ==
  intrinsic の三点一致）。

 19 gate（g01〜g19）は K1109 と同構成: g01 K1086正本SHA pin・g02/g03 runner v17
 git blob c132cc64…の記録と原本一致・g04 root shape safe（8石・quadruple-free）・
 g05 mobility 53・g06 K1086 probes win uncapped・g07 主張3行・g08 probe再現
 node-exact・g09 root初手リスト==独立再導出・g10A1/A2 clean・g11 A1==A2
 per-move node-exact・g12 B clean・g13 chunk vs 単一プロセスのnode会計・g14 証明書
 sorted-unique・末尾改行・行format・g15 B nRows==証明書行・g16 第三方法全木
 再走査PASS・g17 BigInt/Bareiss/python三者の全集計値一致・g18 解釈guard文言
 存在・g19 K1097 footprint三点一致。

## 結果（全19 gate PASS・3方法の全数値一致・監査正本3実行byte-identical）

- **証明書**: `certs/win8-root-00000000012000003800080009000000-20261120.n11`
  ・1,171,958 bytes・32,470戦略行 + root行 + header行（行は昇順・一意）。
  SHA-256 `5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c`。
- **root**: 8石 [24,27,43,59,60,61,85,88]・quadruple-free・loser初手は53手。
  K1086 greedy主張被覆3行 `00000000000000003800000248000000`・
  `00000000000000801202000001000100`・`00000000000080003800000048000000` は
  K1097 win16 footprint（intrinsic == claimed）とも一致（g19）し、
  fold14正本の residual_row_hex_after に3行とも含まれる（現時点で open）。
  fold時は別工程。
- **抽出費用**: Run A1（初手毎53プロセス）総nodes 2,723,200・最大初手
  nodes 223,518（bit 110）・fbt_drops 0（全53初手）・fatal/conflict 0。
  Run B総nodes 2,141,807・戦略行32,470で行集合不変。
- **三重検証の全数値一致**: BigInt / Bareiss / python第三方法が
  visited 69,115（sub-root単位）・winner-to-move 44,580・loser-to-move 13,197・
  loser応手辺 61,058・終端 11,338（全てloser-stuck）・終端石数 [14,18]・
  consumed union 32,470 == 証明書行32,470（missing 0 / extra 0）で完全一致。
  Bareiss root-check: stones 8・loserMobility 53。
- **監査正本**: `output/win8-cert-extract-verification-20261120.json`
  （SHA-256 `ab8cd535c14637c150c02ceeb688b335eb2da9dc1c5778b6a7c05a1a0906f67e`・
  19/19 gate PASS・同一cwd 2回＋別cwd別プロセス1回（EXPERIMENT_ROOT）で
  audit JSON byte-identical・時刻・乱数入力なし）。
- 実装上の注記: 移行時のfail-closed確認として、K1109機械の
  `brc == {"stones": 8, "loserMobility": 50}` 定数を 53 へ差し替えるまで
  g17 が PASS せず監査機が期待値不一致を正しく拒否した（K1109 の
  g19 len(claimed) 教訓と同型）。
